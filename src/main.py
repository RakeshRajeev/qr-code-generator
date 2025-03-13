from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from .schemas.qr import QRCodeRequest, QRCodeResponse
from .db.session import get_db
from .services.qr_service import QRCodeService
from .qr_generator.generator import generate_qr_code
import socket
import psutil
import platform
from .db.migrations.create_tables import create_tables

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    create_tables()

@app.get("/health")
async def health_check():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    
    return {
        "status": "healthy",
        "hostname": hostname,
        "ip_address": ip_address,
        "platform": platform.platform(),
        "cpu_count": psutil.cpu_count(),
        "memory_available": f"{psutil.virtual_memory().available / (1024 * 1024):.2f} MB"
    }

@app.get("/test")
async def test_endpoint():
    return {"message": "QR Code Generator is working!"}

@app.post("/qr/generate", response_model=QRCodeResponse)
async def generate(request: QRCodeRequest, db: Session = Depends(get_db)):
    expires_at = None
    if request.expiration_hours:
        expires_at = datetime.utcnow() + timedelta(hours=request.expiration_hours)
    
    qr_code_path, qr_id = generate_qr_code(request.data)
    qr_service = QRCodeService(db)
    await qr_service.create_qr_code(qr_id, qr_code_path, request.data, expires_at)
    
    # Create image URL using the retrieve endpoint
    image_url = f"/qr/retrieve/{qr_id}"
    
    return QRCodeResponse(
        qr_id=qr_id, 
        expires_at=expires_at,
        image_url=image_url
    )

@app.get("/qr/retrieve/{qr_id}")
async def retrieve(qr_id: str, db: Session = Depends(get_db)):
    qr_service = QRCodeService(db)
    qr_code = await qr_service.get_qr_code(qr_id)
    if not qr_code:
        raise HTTPException(status_code=404, detail="QR code not found")
    return qr_code
