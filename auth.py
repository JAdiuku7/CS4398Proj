from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
 
from app.src.session import get_db
from app.schemas.admin import LoginRequest, TokenResponse
from app.services.AdminService import AdminService
 
router = APIRouter(prefix="/api/auth", tags=["auth"])
 
 
@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Admin login",
    description="Authenticate with admin credentials and receive a JWT bearer token.",
)
async def login(
    data: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    - Returns JWT on success
    - 401 if username or password is wrong
    - 403 if account is disabled
    - 401 if the account is not an admin
    """
    return await AdminService(db).login(data)
 