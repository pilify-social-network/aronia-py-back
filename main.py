from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routes.userRoute import router as UserRouter
from routes.postRoute import router as PostRouter
import time

app = FastAPI()

# Logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    print(f"DEBUG: {request.method} {request.url.path} - Status: {response.status_code} - {process_time:.2f}ms")
    return response

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(UserRouter, tags=["User"], prefix="/user")
app.include_router(PostRouter, tags=["Posts"], prefix="/posts")

@app.get("/")
def read_root():
    return {"message": "Hello FastAPI 🚀"}
