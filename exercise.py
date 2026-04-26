from datetime import date
from typing import Optional
 
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
 
from app.core.deps import get_current_user
from app.src.session import get_db
from app.model.exercise import MuscleGroup
from app.model.user import User
from app.schemas.exercise import (
    ApiResponse,
    ExerciseLogCreate,
    ExerciseLogResponse,
    ExerciseLogUpdate,
    WorkoutHistoryResponse,
)
from app.services.ExerciseService import ExerciseService
 
router = APIRouter(
    prefix="/api/exercises",
    tags=["exercises"],
    dependencies=[Depends(get_current_user)],
)
 
 
# ── Log a new exercise ────────────────────────────────────────────────────────
 
@router.post(
    "",
    response_model=ExerciseLogResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Log an exercise",
    description=(
        "Record one exercise with sets, reps, and weight. "
        "All fields are validated before saving. "
        "Returns the saved log entry on success."
    ),
)
async def log_exercise(
    data: ExerciseLogCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await ExerciseService(db).log_exercise(current_user.id, data)
 
 
# ── Get workout history ───────────────────────────────────────────────────────
 
@router.get(
    "/history",
    response_model=WorkoutHistoryResponse,
    summary="Get workout history",
    description=(
        "Returns the user's full workout history with optional filters. "
        "Includes aggregate totals (sets, reps) across the filtered result."
    ),
)
async def get_history(
    exercise_name: Optional[str]          = Query(None, description="Filter by exercise name (partial match)"),
    muscle_group:  Optional[MuscleGroup]  = Query(None, description="Filter by muscle group"),
    from_date:     Optional[date]         = Query(None, description="Start date (YYYY-MM-DD)"),
    to_date:       Optional[date]         = Query(None, description="End date (YYYY-MM-DD)"),
    limit:         int                    = Query(50, ge=1, le=200, description="Max results per page"),
    offset:        int                    = Query(0,  ge=0,        description="Pagination offset"),
    current_user:  User                   = Depends(get_current_user),
    db:            AsyncSession           = Depends(get_db),
):
    return await ExerciseService(db).get_history(
        user_id       = current_user.id,
        exercise_name = exercise_name,
        muscle_group  = muscle_group,
        from_date     = from_date,
        to_date       = to_date,
        limit         = limit,
        offset        = offset,
    )
 
 
# ── Get a single log entry ────────────────────────────────────────────────────
 
@router.get(
    "/{log_id}",
    response_model=ExerciseLogResponse,
    summary="Get a single exercise log",
)
async def get_log(
    log_id:       int,
    current_user: User = Depends(get_current_user),
    db:           AsyncSession = Depends(get_db),
):
    return await ExerciseService(db).get_log_by_id(current_user.id, log_id)
 
 
# ── Update a log entry ────────────────────────────────────────────────────────
 
@router.put(
    "/{log_id}",
    response_model=ExerciseLogResponse,
    summary="Update an exercise log",
    description="Partial update — only the fields you provide are changed.",
)
async def update_log(
    log_id:       int,
    data:         ExerciseLogUpdate,
    current_user: User = Depends(get_current_user),
    db:           AsyncSession = Depends(get_db),
):
    return await ExerciseService(db).update_log(current_user.id, log_id, data)
 
 
# ── Delete a log entry ────────────────────────────────────────────────────────
 
@router.delete(
    "/{log_id}",
    response_model=ApiResponse,
    summary="Delete an exercise log",
)
async def delete_log(
    log_id:       int,
    current_user: User = Depends(get_current_user),
    db:           AsyncSession = Depends(get_db),
):
    await ExerciseService(db).delete_log(current_user.id, log_id)
    return ApiResponse(message=f"Exercise log {log_id} deleted successfully")
 