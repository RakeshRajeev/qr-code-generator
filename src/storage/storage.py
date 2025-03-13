import os
from datetime import datetime
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import redis
from typing import Optional
import time
from ..config import get_settings

settings = get_settings()

class Base(DeclarativeBase):
    pass

class QRCode(Base):
    __tablename__ = "qr_codes"
    
    id = Column(String, primary_key=True)
    file_path = Column(String, nullable=False)
    original_data = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)

class QRCodeStorage:
    def __init__(self):
        self._init_db_connection()
        self._init_redis_connection()

    def _init_db_connection(self, max_retries=5):
        retry_count = 0
        while retry_count < max_retries:
            try:
                self.engine = create_engine(settings.database_url)
                Base.metadata.create_all(self.engine)
                self.Session = sessionmaker(bind=self.engine)
                break
            except Exception as e:
                retry_count += 1
                if retry_count == max_retries:
                    raise Exception(f"Failed to connect to database after {max_retries} attempts")
                time.sleep(2)

    def _init_redis_connection(self, max_retries=5):
        retry_count = 0
        while retry_count < max_retries:
            try:
                self.redis = redis.Redis(
                    host=settings.redis_host,
                    port=settings.redis_port,
                    decode_responses=True
                )
                self.redis.ping()  # Test connection
                break
            except redis.ConnectionError:
                retry_count += 1
                if retry_count == max_retries:
                    raise Exception(f"Failed to connect to Redis after {max_retries} attempts")
                time.sleep(2)

    async def save_qr_code(self, qr_id: str, file_path: str, 
                          original_data: str, expires_at: Optional[datetime] = None):
        session = self.Session()
        try:
            qr_code = QRCode(
                id=qr_id,
                file_path=file_path,
                original_data=original_data,
                expires_at=expires_at
            )
            session.add(qr_code)
            session.commit()
            
            # Cache the QR code data
            self.redis.setex(
                f"qr:{qr_id}",
                3600,  # Cache for 1 hour
                file_path
            )
        finally:
            session.close()

    async def get_qr_code(self, qr_id: str):
        # Try cache first
        cached = self.redis.get(f"qr:{qr_id}")
        if cached:
            return cached  # Redis is already configured with decode_responses=True

        # If not in cache, query database
        session = self.Session()
        try:
            qr_code = session.query(QRCode).filter(
                QRCode.id == qr_id,
                (QRCode.expires_at > datetime.utcnow()) | (QRCode.expires_at.is_(None))
            ).first()
            
            if qr_code:
                # Update cache
                self.redis.setex(f"qr:{qr_id}", 3600, qr_code.file_path)
                return qr_code.file_path
            return None
        finally:
            session.close()
