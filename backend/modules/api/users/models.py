from pydantic import BaseModel, EmailStr, constr


# Modèle Pydantic pour validation
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


# Modèle de réponse avec un email anonymisé, en utilisant constr(min_length=1)
class UserResponse(BaseModel):
    id: int
    name: str
    email: constr(min_length=1)  # type: ignore
    is_active: bool
    role: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
