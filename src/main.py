from fastapi import FastAPI, APIRouter
from src.product.router import router as product_router

app = FastAPI(title="Zania API", description="API for the Zania project")

router = APIRouter(prefix="/api/v1")
router.include_router(product_router)

@router.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(router)
