from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
from qr_generator.generator import generate_qr_code
from storage.storage import QRCodeStorage
from celery_tasks.tasks import cleanup_expired_codes

app = FastAPI()
storage = QRCodeStorage()

class QRCodeRequest(BaseModel):
    data: str
    expiration_hours: int | None = None

class QRCodeResponse(BaseModel):
    qr_id: str
    expires_at: datetime | None = None

@app.post("/generate", response_model=QRCodeResponse)
async def generate(request: QRCodeRequest):
    expires_at = None
    if request.expiration_hours:
        expires_at = datetime.utcnow() + timedelta(hours=request.expiration_hours)
    
    qr_code_path, qr_id = generate_qr_code(request.data)
    await storage.save_qr_code(qr_id, qr_code_path, request.data, expires_at)
    
    return QRCodeResponse(qr_id=qr_id, expires_at=expires_at)

@app.get("/retrieve/{qr_id}")
async def retrieve(qr_id: str):
    qr_code = await storage.get_qr_code(qr_id)
    if not qr_code:
        raise HTTPException(status_code=404, detail="QR code not found")
    return qr_code
