from enum import Enum
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

class UserRole(str, Enum):
    ADMIN = "admin"
    BROKER = "broker"
    UNDERWRITER = "underwriter"
    CLAIMS_ADJUSTER = "claims_adjuster"
    CUSTOMER_SERVICE = "customer_service"
    VIEWER = "viewer"

class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    SUSPENDED = "suspended"

class UserBase(BaseModel):
    username: str
    email: str
    full_name: str
    role: UserRole
    status: UserStatus = UserStatus.ACTIVE

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    status: Optional[UserStatus] = None

class UserInDB(UserBase):
    id: int
    hashed_password: str
    is_two_factor_enabled: bool = False
    two_factor_secret: Optional[str] = None
    last_login: Optional[datetime] = None
    failed_login_attempts: int = 0
    locked_until: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

class User(UserBase):
    id: int
    is_two_factor_enabled: bool = False
    last_login: Optional[datetime] = None
    failed_login_attempts: int = 0
    locked_until: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str
    role: UserRole

class TwoFactorRequest(BaseModel):
    username: str
    password: str

class TwoFactorVerify(BaseModel):
    username: str
    token: str

class Permission(BaseModel):
    id: int
    name: str
    description: str

class RolePermission(BaseModel):
    role: UserRole
    permissions: List[str]