from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class QRCode(Base):
    __tablename__ = "qr_codes"
    
    id = Column(String, primary_key=True)
    file_path = Column(String, nullable=False)
    original_data = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
