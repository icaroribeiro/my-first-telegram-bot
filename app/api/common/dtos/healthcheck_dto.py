from pydantic import BaseModel, Field


class HealthcheckDTO(BaseModel):
    message: str = Field(default="Healthy")
