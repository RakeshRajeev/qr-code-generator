from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class QRCodeRequest(BaseModel):
    data: str
    expiration_hours: Optional[int] = None

class QRCodeResponse(BaseModel):
    qr_id: str
    expires_at: Optional[datetime] = None
    image_url: str  # Add this field

class QRCodeInDB(BaseModel):
    id: str
    file_path: str
    original_data: str
    created_at: datetime
    expires_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
