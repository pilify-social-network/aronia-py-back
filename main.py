from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.userRoute import router as UserRouter

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(UserRouter, tags=["User"], prefix="/user")

@app.get("/")
def read_root():
    return {"message": "Hello FastAPI 🚀"}
