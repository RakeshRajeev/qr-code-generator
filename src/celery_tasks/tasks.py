from celery import Celery
from datetime import datetime
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from storage.storage import QRCode, Base

celery = Celery('tasks', broker=os.getenv("CELERY_BROKER_URL"))

@celery.task
def cleanup_expired_codes():
    engine = create_engine(os.getenv("DATABASE_URL"))
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        expired_codes = session.query(QRCode).filter(
            QRCode.expires_at < datetime.utcnow()
        ).all()
        
        for code in expired_codes:
            # Delete the file
            if os.path.exists(code.file_path):
                os.remove(code.file_path)
            # Delete the database record
            session.delete(code)
        
        session.commit()
    finally:
        session.close()

# Configure periodic task
@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Run cleanup every hour
    sender.add_periodic_task(3600.0, cleanup_expired_codes.s())
