from fastapi import FastAPI

from routes import student

app = FastAPI()
app.include_router(student)