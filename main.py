import uvicorn
from src.config.router_config import app
from src.controllers.depth_map import router


app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
