from pydantic import BaseModel, EmailStr
from typing import Optional, List, Any
from datetime import datetime


# ============ Auth Schemas ============

class RegisterRequest(BaseModel):
    username: str
    email: Optional[str] = None
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    rating: int = 0
    total_points: int = 0
    role: str = "participant"


class AuthResponse(BaseModel):
    token: str
    user: UserResponse


# ============ Profile Schemas ============

class ProfileResponse(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    rating: int = 0
    total_points: int = 0
    rank: int = 0
    solved_tasks: List[int] = []
    role: str = "participant"


# ============ Task Schemas ============

class TaskSummary(BaseModel):
    id: int
    title: str
    difficulty: str
    points: int
    status: Optional[str] = "unsolved"


class TableColumn(BaseModel):
    name: str
    type: str


class TableSchema(BaseModel):
    name: str
    columns: List[TableColumn]
    sampleData: List[dict] = []


class TaskDetail(BaseModel):
    id: int
    title: str
    description: str
    difficulty: str
    points: int
    schema: str
    tables: List[dict]
    expectedResult: Optional[List[dict]] = None


class TaskFull(BaseModel):
    id: int
    title: str
    description: str
    difficulty: str
    points: int
    schema: str
    tables: List[dict]
    expected_result: List[dict]


class TaskCreate(BaseModel):
    title: str
    description: str
    difficulty: str
    points: int
    schema: str
    tables: List[dict]
    expected_result: List[dict]


class TaskCreateResponse(BaseModel):
    id: int
    title: str
    success: bool = True


# ============ Execution Schemas ============

class ExecuteRequest(BaseModel):
    query: str


class ExecuteResponse(BaseModel):
    status: str  # "success" or "error"
    data: Optional[List[dict]] = None
    message: Optional[str] = None
    execution_time: Optional[float] = None


class SubmitResponse(BaseModel):
    is_correct: bool
    points_earned: int
    new_total_points: int
    expected_result: List[dict]


# ============ Leaderboard Schemas ============

class LeaderboardEntry(BaseModel):
    rank: int
    username: str
    total_points: int
    solved_tasks: int
    avg_time: float
    avatar: str


# ============ Admin Schemas ============

class AdminUser(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    rating: int = 0
    total_points: int = 0
    assigned_task_id: Optional[int] = None


class AssignTaskRequest(BaseModel):
    taskId: int


class SuccessResponse(BaseModel):
    success: bool = True
    message: str = ""


class AssignedTaskResponse(BaseModel):
    id: int
    title: str
    difficulty: str
    points: int


# ============ Settings Schemas ============

class SettingsResponse(BaseModel):
    battle_start: Optional[str] = None
    round_duration_minutes: int = 120


class SettingsUpdate(BaseModel):
    battle_start: Optional[str] = None
    round_duration_minutes: Optional[int] = None
