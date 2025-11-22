from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from typing import List, Optional

# Request model (no ID)
class StudentCreate(BaseModel):
    studentName: str
    studentParentName: str
    studentEmail: str
    studentAddress: str
    sex: str
    subject: List[str]

# Response model (has ID)
class StudentDetails(StudentCreate):
    id: UUID = Field(default_factory=uuid4)


class StudentUpdate(BaseModel):
    studentName: Optional[str] = None
    studentParentName: Optional[str] = None
    studentEmail: Optional[str] = None
    studentAddress: Optional[str] = None
    sex: Optional[str] = None
    subject: Optional[List[str]] = None
