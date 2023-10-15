from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import string

from enpoints import router
from config import server_config

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=server_config.server_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=router, prefix="/api")
