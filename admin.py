from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
 
from app.core.deps import require_admin
from app.src.session import get_db
from app.model.user import User
from app.schemas.admin import (
    AccessToggle,
    ApiResponse,
    TrainerCreate,
    TrainerResponse,
    TrainerUpdate,
    UserCreate,
    UserResponse,
    UserUpdate,
)
from app.services.AdminService import AdminService
 
router = APIRouter(
    prefix="/api/admin",
    tags=["admin"],
    dependencies=[Depends(require_admin)],   # every route requires ADMIN role
)
 
 
# ══════════════════════════════════════════════════════════════════════════════
# USER ENDPOINTS
# ══════════════════════════════════════════════════════════════════════════════
 
@router.get(
    "/users",
    response_model=list[UserResponse],
    summary="List all users",
)
async def list_users(db: AsyncSession = Depends(get_db)):
    return await AdminService(db).get_all_users()
 
 
@router.get(
    "/users/{user_id}",
    response_model=UserResponse,
    summary="Get a single user",
)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await AdminService(db).get_user_by_id(user_id)
 
 
@router.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
)
async def create_user(data: UserCreate, db: AsyncSession = Depends(get_db)):
    return await AdminService(db).create_user(data)
 
 
@router.put(
    "/users/{user_id}",
    response_model=UserResponse,
    summary="Update a user",
)
async def update_user(
    user_id: int,
    data: UserUpdate,
    db: AsyncSession = Depends(get_db),
):
    return await AdminService(db).update_user(user_id, data)
 
 
@router.delete(
    "/users/{user_id}",
    response_model=ApiResponse,
    summary="Delete a user",
)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    await AdminService(db).delete_user(user_id)
    return ApiResponse(message=f"User {user_id} deleted successfully")
 
 
@router.patch(
    "/users/{user_id}/access",
    response_model=UserResponse,
    summary="Enable or disable user login",
)
async def set_user_access(
    user_id: int,
    data: AccessToggle,
    db: AsyncSession = Depends(get_db),
):
    return await AdminService(db).set_user_access(user_id, data.is_active)
 
 
# ══════════════════════════════════════════════════════════════════════════════
# TRAINER ENDPOINTS
# ══════════════════════════════════════════════════════════════════════════════
 
@router.get(
    "/trainers",
    response_model=list[TrainerResponse],
    summary="List all trainers",
)
async def list_trainers(db: AsyncSession = Depends(get_db)):
    return await AdminService(db).get_all_trainers()
 
 
@router.get(
    "/trainers/{trainer_id}",
    response_model=TrainerResponse,
    summary="Get a single trainer",
)
async def get_trainer(trainer_id: int, db: AsyncSession = Depends(get_db)):
    return await AdminService(db).get_trainer_by_id(trainer_id)
 
 
@router.post(
    "/trainers",
    response_model=TrainerResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a trainer account",
)
async def create_trainer(data: TrainerCreate, db: AsyncSession = Depends(get_db)):
    return await AdminService(db).create_trainer(data)
 
 
@router.put(
    "/trainers/{trainer_id}",
    response_model=TrainerResponse,
    summary="Update a trainer",
)
async def update_trainer(
    trainer_id: int,
    data: TrainerUpdate,
    db: AsyncSession = Depends(get_db),
):
    return await AdminService(db).update_trainer(trainer_id, data)
 
 
@router.delete(
    "/trainers/{trainer_id}",
    response_model=ApiResponse,
    summary="Delete a trainer account",
)
async def delete_trainer(trainer_id: int, db: AsyncSession = Depends(get_db)):
    await AdminService(db).delete_trainer(trainer_id)
    return ApiResponse(message=f"Trainer {trainer_id} deleted successfully")
 
 
@router.patch(
    "/trainers/{trainer_id}/access",
    response_model=TrainerResponse,
    summary="Enable or disable trainer login",
)
async def set_trainer_access(
    trainer_id: int,
    data: AccessToggle,
    db: AsyncSession = Depends(get_db),
):
    return await AdminService(db).set_trainer_access(trainer_id, data.is_active)
 