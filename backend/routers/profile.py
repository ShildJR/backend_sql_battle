from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from database import get_db
from models import User, Submission
from schemas import ProfileResponse
from auth import get_current_user

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("", response_model=ProfileResponse)
async def get_profile(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current user's profile."""
    # Get solved tasks
    solved_result = await db.execute(
        select(Submission.task_id).where(
            Submission.user_id == current_user.id,
            Submission.is_correct == True
        ).distinct()
    )
    solved_tasks = list(solved_result.scalars().all())
    
    # Calculate rank
    rank_result = await db.execute(
        select(func.count(User.id)).where(User.total_points > current_user.total_points)
    )
    rank = rank_result.scalar() + 1
    
    return ProfileResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        rating=current_user.rating,
        total_points=current_user.total_points,
        rank=rank,
        solved_tasks=solved_tasks,
        role=current_user.role
    )
