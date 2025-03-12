from fastapi import FastAPI
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.modules.api.patients.routes import router as patients_router
from backend.modules.db.preparation.users.create_db import init_db

init_db()

app = FastAPI(
    title="MedCostPredict API",
    description="API for managing patients in a health system.",
    version="1.0.0",
)

app.include_router(patients_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
