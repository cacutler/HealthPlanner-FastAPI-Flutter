from fastapi import FastAPI
from app.routers import auth, users, workouts, exercises, nutrition, weight
app = FastAPI(title="Health Planner API", description="Track workouts, nutrition, and weight with JWT authentication.", version="1.0.0")
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(workouts.router)
app.include_router(exercises.router)
app.include_router(nutrition.router)
app.include_router(weight.router)
@app.get("/health")
async def health_check():
    return {"status": "ok"}