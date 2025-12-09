import uvicorn
import sys 
from pathlib import Path
from fastapi import FastAPI

from src.route.users import router as user_router

sys.path.append(str(Path(__file__).parent.parent))


app = FastAPI()

app.include_router(user_router)

if __name__ == "__main__" :
    uvicorn.run("main:app", host="127.0.0.1", port= 8000,reload= True)