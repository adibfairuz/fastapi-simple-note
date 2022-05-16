import sys
import os
module_path = os.path.abspath(os.getcwd())
if module_path not in sys.path:       
    sys.path.append(module_path)

from app.db.database import Base, engine
from app.models.tables import UserTable, PostTable

print("Creating database...")

Base.metadata.create_all(engine)