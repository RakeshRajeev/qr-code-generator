from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class QRCodeRequest(BaseModel):
    data: str
    expiration_hours: Optional[int] = None

class QRCodeResponse(BaseModel):
    qr_id: str
    expires_at: Optional[datetime] = None

class QRCodeInDB(BaseModel):
    id: str
    file_path: str
    original_data: str
    created_at: datetime
    expires_at: Optional[datetime] = None

    class Config:
        orm_mode = True
