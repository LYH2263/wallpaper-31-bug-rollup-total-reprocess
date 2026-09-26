from fastapi import APIRouter, HTTPException
from app.repositories import history as repo

router = APIRouter()


@router.get("/runs")
def list_runs(limit: int = 50):
    return {"items": repo.list_runs(limit)}


@router.get("/runs/{run_id}")
def get_run(run_id: int):
    run = repo.get_run(run_id)
    if not run:
        raise HTTPException(404, "run not found")
    return run
