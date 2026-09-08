import asyncio
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from database import async_session
from models import User, Submission

router = APIRouter(tags=["WebSocket"])


class ConnectionManager:
    """Manages WebSocket connections for leaderboard updates."""
    
    def __init__(self):
        self.active_connections: list[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
    
    async def broadcast_leaderboard(self):
        """Fetch and broadcast the current leaderboard to all connections."""
        async with async_session() as db:
            result = await db.execute(
                select(User).where(User.role == "participant").order_by(User.total_points.desc()).limit(50)
            )
            users = result.scalars().all()
            
            leaderboard = []
            for rank, user in enumerate(users, 1):
                solved_result = await db.execute(
                    select(func.count(func.distinct(Submission.task_id))).where(
                        Submission.user_id == user.id,
                        Submission.is_correct == True
                    )
                )
                solved_count = solved_result.scalar() or 0
                
                parts = user.username.split()
                if len(parts) >= 2:
                    avatar = parts[0][0] + parts[1][0]
                else:
                    avatar = user.username[:2]
                
                leaderboard.append({
                    "rank": rank,
                    "username": user.username,
                    "total_points": user.total_points,
                    "solved_tasks": solved_count,
                    "avatar": avatar.upper()
                })
        
        message = json.dumps({
            "type": "leaderboard_update",
            "data": leaderboard
        })
        
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                disconnected.append(connection)
        
        for conn in disconnected:
            self.disconnect(conn)


manager = ConnectionManager()


@router.websocket("/ws/leaderboard")
async def leaderboard_websocket(websocket: WebSocket):
    """WebSocket endpoint for real-time leaderboard updates."""
    await manager.connect(websocket)
    
    # Send initial leaderboard
    await manager.broadcast_leaderboard()
    
    try:
        while True:
            # Keep connection alive, listen for pings
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text(json.dumps({"type": "pong"}))
    except WebSocketDisconnect:
        manager.disconnect(websocket)


async def periodic_leaderboard_broadcast():
    """Background task to broadcast leaderboard every 5 seconds."""
    while True:
        await asyncio.sleep(5)
        if manager.active_connections:
            await manager.broadcast_leaderboard()


async def broadcast_leaderboard_update():
    """Call this after a successful submission to immediately update the leaderboard."""
    if manager.active_connections:
        await manager.broadcast_leaderboard()
