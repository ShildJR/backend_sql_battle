from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from database import get_db
from models import User, Submission
from schemas import LeaderboardEntry

router = APIRouter(prefix="/leaderboard", tags=["Leaderboard"])


@router.get("", response_model=list[LeaderboardEntry])
async def get_leaderboard(db: AsyncSession = Depends(get_db)):
    """Get leaderboard - top participants."""
    # Get all users ordered by total_points
    result = await db.execute(
        select(User).where(User.role == "participant").order_by(User.total_points.desc()).limit(50)
    )
    users = result.scalars().all()
    
    leaderboard = []
    for rank, user in enumerate(users, 1):
        # Count solved tasks
        solved_result = await db.execute(
            select(func.count(func.distinct(Submission.task_id))).where(
                Submission.user_id == user.id,
                Submission.is_correct == True
            )
        )
        solved_count = solved_result.scalar() or 0
        
        # Calculate average time
        avg_time_result = await db.execute(
            select(func.avg(Submission.execution_time_ms)).where(
                Submission.user_id == user.id,
                Submission.is_correct == True,
                Submission.execution_time_ms.isnot(None)
            )
        )
        avg_time_ms = avg_time_result.scalar()
        avg_time = round(avg_time_ms / 1000, 2) if avg_time_ms else 0.0
        
        # Generate avatar initials
        parts = user.username.split()
        if len(parts) >= 2:
            avatar = parts[0][0] + parts[1][0]
        else:
            avatar = user.username[:2]
        avatar = avatar.upper()
        
        leaderboard.append(LeaderboardEntry(
            rank=rank,
            username=user.username,
            total_points=user.total_points,
            solved_tasks=solved_count,
            avg_time=avg_time,
            avatar=avatar
        ))
    
    return leaderboard
