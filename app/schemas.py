from pydantic import BaseModel
from typing import List

class CalculationCreate(BaseModel):
    expression: str

class CalculationOut(CalculationCreate):
    id: int
    result: float
    class Config:
        orm_mode = True

class CalculationUpdate(BaseModel):
    expression: str
    result: float
