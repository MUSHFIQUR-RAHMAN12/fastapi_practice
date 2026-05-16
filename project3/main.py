from fastapi import FastAPI,Depends, Query,status,Path,HTTPException
from database.db import create_tables
from routers.mydb_project import router as mydb_router
from routers.auth import router as auth_router
from routers.userrouter import router as user_router
app = FastAPI()

app.include_router(user_router)
app.include_router(mydb_router)
app.include_router(auth_router)

@app.on_event("startup")
def on_startup():
    create_tables()
