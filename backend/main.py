from fastapi import FastAPI
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.modules.api.routes import router as patients_router


app = FastAPI(
    title="MedCostPredict API",
    description="API for managing patients in a health system.",
    version="1.0.0",
)

app.include_router(patients_router)
