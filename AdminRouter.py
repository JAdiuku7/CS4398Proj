from fastapi import APIRouter

from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

from pydantic import BaseModel

class TrainerResponse(BaseModel):
    id: int
    name: str
    email: str

router = APIRouter(prefix="/api/admin", tags=["admin"])

# USERS
@router.get("/users", response_model=list[UserResponse])
def get_users():
    pass

@router.get("/users/{id}", response_model=UserResponse)
def get_user(id: int):
    pass

@router.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate):
    pass

@router.put("/users/{id}", response_model=UserResponse)
def update_user(id: int, user: UserUpdate):
    pass

@router.delete("/users/{id}", status_code=204)
def delete_user(id: int):
    pass

@router.patch("/users/{id}/access", response_model=UserResponse)
def update_user_access(id: int):
    pass


# TRAINERS
@router.get("/trainers", response_model=list[TrainerResponse])
def get_trainers():
    pass

@router.get("/trainers/{id}", response_model=TrainerResponse)
def get_trainer(id: int):
    pass

@router.post("/trainers", response_model=TrainerResponse, status_code=201)
def create_trainer(trainer: TrainerCreate):
    pass

@router.put("/trainers/{id}", response_model=TrainerResponse)
def update_trainer(id: int, trainer: TrainerUpdate):
    pass

@router.delete("/trainers/{id}", status_code=204)
def delete_trainer(id: int):
    pass

@router.patch("/trainers/{id}/access", response_model=TrainerResponse)
def update_trainer_access(id: int):
    pass