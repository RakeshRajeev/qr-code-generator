from ..db.models import QRCode
from ..schemas.qr import QRCodeInDB
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
import redis
from ..config import get_settings

settings = get_settings()

class QRCodeService:
    def __init__(self, db: Session):
        self.db = db
        self.redis = redis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            decode_responses=True
        )

    async def create_qr_code(self, qr_id: str, file_path: str, 
                            original_data: str, expires_at: Optional[datetime] = None) -> QRCodeInDB:
        qr_code = QRCode(
            id=qr_id,
            file_path=file_path,
            original_data=original_data,
            expires_at=expires_at
        )
        self.db.add(qr_code)
        self.db.commit()
        self.db.refresh(qr_code)
        
        # Cache the QR code
        self.redis.setex(f"qr:{qr_id}", 3600, file_path)
        
        return QRCodeInDB.from_orm(qr_code)

    async def get_qr_code(self, qr_id: str) -> Optional[str]:
        # Try cache first
        cached = self.redis.get(f"qr:{qr_id}")
        if cached:
            return cached

        # Query database
        qr_code = self.db.query(QRCode).filter(
            QRCode.id == qr_id,
            (QRCode.expires_at > datetime.utcnow()) | (QRCode.expires_at.is_(None))
        ).first()

        if qr_code:
            self.redis.setex(f"qr:{qr_id}", 3600, qr_code.file_path)
            return qr_code.file_path
        return None
