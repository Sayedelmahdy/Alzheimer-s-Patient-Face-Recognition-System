from fastapi import FastAPI
import nest_asyncio
import uvicorn
from app.routers import patient, family_member

app = FastAPI()

# Include routers
app.include_router(patient.router)  # This should now work correctly
app.include_router(family_member.router)

if __name__ == "__main__":
    nest_asyncio.apply()
    uvicorn.run(app, host="127.0.0.1", port=8010)
