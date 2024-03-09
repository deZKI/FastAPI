from pydantic import BaseModel, Field, validator, SecretStr


class SUser(BaseModel):
    """Schema for users"""
    name: str = Field(..., min_length=2, max_length=50)
    surname: str = Field(..., min_length=2, max_length=50)
    telegram_id: str = Field(..., min_length=5, max_length=20)
    has_know_from: str = Field(..., max_length=100)
    church: str = Field(..., max_length=100)
    is_admin: bool = False


class SUserAuth(BaseModel):
    """Schema for user authentication"""
    telegram_id: str = Field(..., min_length=5, max_length=20)
    password: SecretStr = Field(..., min_length=6)


class SUserRegistration(SUserAuth):
    """Schema for user registration"""
    name: str = Field(..., min_length=2, max_length=50)
    surname: str = Field(..., min_length=2, max_length=50)
    has_know_from: str = Field(..., max_length=100)
    church: str = Field(..., max_length=100)
    age: int
    model_config = {
        "json_schema_extra": {
            "examples": [{
                "name": "Kirill",
                "surname": "Lee",
                "password": "Paswrodderef",
                "telegram_id": "@derzki123",
                "has_know_from": "from_friend",
                "church": "LocalChurch",
                "age": 20,
            }]
        }
    }

    @validator('password')
    def password_strength_check(cls, value):
        if len(value) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return value
