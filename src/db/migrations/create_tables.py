from ..models import Base
from ..session import engine

def create_tables():
    Base.metadata.create_all(bind=engine)
