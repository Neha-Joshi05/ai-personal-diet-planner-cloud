from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.schemas import PlanOut
from backend.utils.deps import get_db, get_current_user
from backend.models.user import User
from backend.services.plan_service import generate_and_save_plan
from cloud import database_service

router = APIRouter(tags=["plans"])


@router.post("/generate-plan", response_model=PlanOut, status_code=201)
def generate_plan_route(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        plan = generate_and_save_plan(db, current_user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return plan


@router.get("/plans", response_model=list[PlanOut])
def list_plans(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return database_service.list_plans(db, current_user.user_id)


@router.get("/plans/{plan_id}", response_model=PlanOut)
def get_plan(plan_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    plan = database_service.get_plan(db, current_user.user_id, plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan


@router.delete("/plans/{plan_id}", status_code=204)
def delete_plan(plan_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    deleted = database_service.delete_plan(db, current_user.user_id, plan_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Plan not found")
