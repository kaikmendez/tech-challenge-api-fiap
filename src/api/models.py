from pydantic import BaseModel

class HealthStatus(BaseModel):
    api_status: str
    db_status: str