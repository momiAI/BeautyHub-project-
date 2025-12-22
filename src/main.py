import uvicorn
import sys
from pathlib import Path
from fastapi import FastAPI

sys.path.append(str(Path(__file__).parent.parent))

from src.route.users import router as user_router
from src.route.masters import router as masters_router
from src.route.service import router as service_router
from src.route.master_specialization import router as master_specialization_router
from src.route.admin import router as admin_router

app = FastAPI()

app.include_router(user_router)
app.include_router(masters_router)
app.include_router(service_router)
app.include_router(master_specialization_router)
app.include_router(admin_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
