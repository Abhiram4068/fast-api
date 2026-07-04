from app.database.base import Base
from app.database.engine import engine

# Import all models so SQLAlchemy registers them
import app.models

Base.metadata.create_all(bind=engine)

print("✅ All tables created successfully!")