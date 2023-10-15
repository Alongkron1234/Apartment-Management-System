from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from rest.routers import router
from config import server_config


def main() -> FastAPI:
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=server_config.server_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router=router, prefix="/api")
    return app


if __name__ == "__main__":
    app = main()
    uvicorn.run(
        app=app,
        host=server_config.server_host,
        port=server_config.server_port,
        reload=server_config.server_reload,
    )
