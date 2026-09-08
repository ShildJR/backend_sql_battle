from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from database import get_db
from models import User, Task, Submission, TaskAssignment
from schemas import (
    TaskSummary, TaskDetail, ExecuteRequest, ExecuteResponse,
    SubmitResponse
)
from auth import get_current_user
from services import execute_sql_in_sandbox, compare_results
from routers.websocket import broadcast_leaderboard_update

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("", response_model=list[TaskSummary])
async def get_tasks(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get list of all tasks."""
    result = await db.execute(select(Task))
    tasks = result.scalars().all()
    
    # Get user's solved tasks
    solved_result = await db.execute(
        select(Submission.task_id).where(
            Submission.user_id == current_user.id,
            Submission.is_correct == True
        ).distinct()
    )
    solved_task_ids = set(solved_result.scalars().all())
    
    return [
        TaskSummary(
            id=task.id,
            title=task.title,
            difficulty=task.difficulty,
            points=task.points,
            status="solved" if task.id in solved_task_ids else "unsolved"
        )
        for task in tasks
    ]


@router.get("/{task_id}", response_model=TaskDetail)
async def get_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get task details."""
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return TaskDetail(
        id=task.id,
        title=task.title,
        description=task.description,
        difficulty=task.difficulty,
        points=task.points,
        schema=task.schema,
        tables=task.tables,
        expectedResult=task.expected_result
    )


@router.post("/{task_id}/execute", response_model=ExecuteResponse)
async def execute_query(
    task_id: int,
    data: ExecuteRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Execute SQL query in sandbox (Run button)."""
    # Get task
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Execute in sandbox
    sandbox_result = execute_sql_in_sandbox(
        query=data.query,
        schema=task.schema,
        tables_data=task.tables
    )
    
    return ExecuteResponse(**sandbox_result)


@router.post("/{task_id}/submit", response_model=SubmitResponse)
async def submit_solution(
    task_id: int,
    data: ExecuteRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Submit solution for verification."""
    # Get task
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Execute user's query in sandbox
    sandbox_result = execute_sql_in_sandbox(
        query=data.query,
        schema=task.schema,
        tables_data=task.tables
    )
    
    if sandbox_result["status"] == "error":
        # Save failed submission
        submission = Submission(
            user_id=current_user.id,
            task_id=task_id,
            query=data.query,
            is_correct=False,
            points_earned=0
        )
        db.add(submission)
        
        return SubmitResponse(
            is_correct=False,
            points_earned=0,
            new_total_points=current_user.total_points,
            expected_result=task.expected_result
        )
    
    # Compare results
    is_correct = compare_results(
        sandbox_result["data"],
        task.expected_result
    )
    
    points_earned = task.points if is_correct else 0
    
    # Save submission
    submission = Submission(
        user_id=current_user.id,
        task_id=task_id,
        query=data.query,
        is_correct=is_correct,
        points_earned=points_earned,
        execution_time_ms=int(sandbox_result.get("execution_time", 0) * 1000)
    )
    db.add(submission)
    
    # Update user points if correct
    if is_correct:
        current_user.total_points += points_earned
        current_user.rating += points_earned
        
        # Update task assignment if exists
        assignment_result = await db.execute(
            select(TaskAssignment).where(TaskAssignment.user_id == current_user.id)
        )
        assignment = assignment_result.scalar_one_or_none()
        if assignment:
            from datetime import datetime
            assignment.completed_at = datetime.utcnow()
    
    await db.flush()
    
    # Broadcast leaderboard update via WebSocket
    await broadcast_leaderboard_update()
    
    return SubmitResponse(
        is_correct=is_correct,
        points_earned=points_earned,
        new_total_points=current_user.total_points,
        expected_result=task.expected_result
    )
