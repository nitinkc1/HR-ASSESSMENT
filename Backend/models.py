from pydantic import BaseModel
from typing import List, Optional

class Employee(BaseModel):
    id: int
    name: str
    role: Optional[str] = None
    department: Optional[str] = None
    skills: List[str]
    experience_years: int
    projects: List[str]
    availability: str

class ChatQuery(BaseModel):
    query: str

class ChatResponse(BaseModel):
    response: str
    employees: Optional[List[Employee]] = None
