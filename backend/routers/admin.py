from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from models import User, Task, TaskAssignment
from schemas import (
    AdminUser, TaskFull, TaskCreate, TaskCreateResponse,
    AssignTaskRequest, SuccessResponse, AssignedTaskResponse,
    SettingsResponse, SettingsUpdate
)
from auth import get_current_admin, get_current_user
from datetime import datetime

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/users", response_model=list[AdminUser])
async def get_all_users(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Get all users (admin only)."""
    result = await db.execute(select(User))
    users = result.scalars().all()
    
    admin_users = []
    for user in users:
        # Get assigned task
        assignment_result = await db.execute(
            select(TaskAssignment).where(TaskAssignment.user_id == user.id)
        )
        assignment = assignment_result.scalar_one_or_none()
        
        admin_users.append(AdminUser(
            id=user.id,
            username=user.username,
            email=user.email,
            rating=user.rating,
            total_points=user.total_points,
            assigned_task_id=assignment.task_id if assignment else None
        ))
    
    return admin_users


@router.post("/users/{user_id}/assign", response_model=SuccessResponse)
async def assign_task(
    user_id: int,
    data: AssignTaskRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Assign a task to a user."""
    # Check user exists
    user_result = await db.execute(select(User).where(User.id == user_id))
    if not user_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check task exists
    task_result = await db.execute(select(Task).where(Task.id == data.taskId))
    if not task_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Check if assignment already exists
    existing_result = await db.execute(
        select(TaskAssignment).where(TaskAssignment.user_id == user_id)
    )
    existing = existing_result.scalar_one_or_none()
    
    if existing:
        existing.task_id = data.taskId
        existing.assigned_at = datetime.utcnow()
        existing.started_at = None
        existing.completed_at = None
    else:
        assignment = TaskAssignment(
            user_id=user_id,
            task_id=data.taskId
        )
        db.add(assignment)
    
    await db.flush()
    
    return SuccessResponse(success=True, message="Задача назначена")


@router.post("/users/{user_id}/clear", response_model=SuccessResponse)
async def clear_assignment(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Clear task assignment for a user."""
    result = await db.execute(
        select(TaskAssignment).where(TaskAssignment.user_id == user_id)
    )
    assignment = result.scalar_one_or_none()
    
    if assignment:
        await db.delete(assignment)
        await db.flush()
    
    return SuccessResponse(success=True, message="Назначение снято")


@router.get("/tasks", response_model=list[TaskFull])
async def get_admin_tasks(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Get all tasks for admin (full details)."""
    result = await db.execute(select(Task))
    tasks = result.scalars().all()
    
    return [
        TaskFull(
            id=task.id,
            title=task.title,
            description=task.description,
            difficulty=task.difficulty,
            points=task.points,
            schema=task.schema,
            tables=task.tables,
            expected_result=task.expected_result
        )
        for task in tasks
    ]


@router.post("/tasks", response_model=TaskCreateResponse, status_code=201)
async def create_task(
    data: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Create a new task."""
    task = Task(
        title=data.title,
        description=data.description,
        difficulty=data.difficulty,
        points=data.points,
        schema=data.schema,
        tables=data.tables,
        expected_result=data.expected_result
    )
    db.add(task)
    await db.flush()
    await db.refresh(task)
    
    return TaskCreateResponse(
        id=task.id,
        title=task.title,
        success=True
    )


@router.get("/settings", response_model=SettingsResponse)
async def get_settings(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Get battle settings."""
    from models import Settings as SettingsModel
    result = await db.execute(select(SettingsModel).limit(1))
    settings_obj = result.scalar_one_or_none()
    
    if not settings_obj:
        return SettingsResponse()
    
    return SettingsResponse(
        battle_start=settings_obj.battle_start.isoformat() if settings_obj.battle_start else None,
        round_duration_minutes=settings_obj.round_duration_minutes
    )


@router.put("/settings", response_model=SettingsResponse)
async def update_settings(
    data: SettingsUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Update battle settings."""
    from models import Settings as SettingsModel
    result = await db.execute(select(SettingsModel).limit(1))
    settings_obj = result.scalar_one_or_none()
    
    if not settings_obj:
        settings_obj = SettingsModel()
        db.add(settings_obj)
    
    if data.battle_start is not None:
        settings_obj.battle_start = datetime.fromisoformat(data.battle_start.replace('Z', '+00:00'))
    if data.round_duration_minutes is not None:
        settings_obj.round_duration_minutes = data.round_duration_minutes
    
    await db.flush()
    
    return SettingsResponse(
        battle_start=settings_obj.battle_start.isoformat() if settings_obj.battle_start else None,
        round_duration_minutes=settings_obj.round_duration_minutes
    )


# User assigned task endpoint (not under /admin prefix)
user_router = APIRouter(tags=["User"])


@user_router.get("/user/assigned-task")
async def get_assigned_task(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get the task assigned to the current user."""
    result = await db.execute(
        select(TaskAssignment).where(TaskAssignment.user_id == current_user.id)
    )
    assignment = result.scalar_one_or_none()
    
    if not assignment:
        raise HTTPException(status_code=404, detail={"error": "Task not assigned"})
    
    # Get the task
    task_result = await db.execute(select(Task).where(Task.id == assignment.task_id))
    task = task_result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(status_code=404, detail={"error": "Task not found"})
    
    # Update started_at if not set
    if not assignment.started_at:
        assignment.started_at = datetime.utcnow()
        await db.flush()
    
    return AssignedTaskResponse(
        id=task.id,
        title=task.title,
        difficulty=task.difficulty,
        points=task.points
    )
