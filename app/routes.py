
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from . import database, models, schemas
from typing import List
import json
from pathlib import Path

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("calculator.html", {"request": request})

@router.post("/calculate", response_model=schemas.CalculationOut)
def calculate(calc: schemas.CalculationCreate, db: Session = Depends(get_db)):
    try:
        result = eval(calc.expression)
        db_calc = models.Calculation(expression=calc.expression, result=result)
        db.add(db_calc)
        db.commit()
        db.refresh(db_calc)
        return db_calc
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid expression")

@router.get("/records", response_model=List[schemas.CalculationOut])
def get_records(db: Session = Depends(get_db)):
    return db.query(models.Calculation).order_by(models.Calculation.created_at.desc()).limit(10).all()

@router.delete("/calculate/{calc_id}")
def delete_calc(calc_id: int, db: Session = Depends(get_db)):
    calc = db.query(models.Calculation).get(calc_id)
    if not calc:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(calc)
    db.commit()
    return {"deleted_id": calc_id}

@router.put("/calculate/{calc_id}", response_model=schemas.CalculationOut)
def update_calc(calc_id: int, data: schemas.CalculationUpdate, db: Session = Depends(get_db)):
    calc = db.query(models.Calculation).get(calc_id)
    if not calc:
        raise HTTPException(status_code=404, detail="Not found")
    calc.expression = data.expression
    calc.result = data.result
    db.commit()
    db.refresh(calc)
    return calc

RECORD_FILE = Path("app/data/records.json")
RECORD_FILE.parent.mkdir(exist_ok=True)

@router.post("/save-file")
def save_file_records(db: Session = Depends(get_db)):
    records = db.query(models.Calculation).order_by(models.Calculation.created_at).all()
    data = [
        {
            "id": r.id,
            "expression": r.expression,
            "result": r.result,
            "created_at": str(r.created_at)
        } for r in records
    ]
    with open(RECORD_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return {"status": "saved", "count": len(data)}


@router.get("/load-file")
def load_file_records():
    if not RECORD_FILE.exists():
        return []
    try:
        with open(RECORD_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return sorted(data, key=lambda x: x.get("id", 0), reverse=True)
    except json.JSONDecodeError:
        return []

