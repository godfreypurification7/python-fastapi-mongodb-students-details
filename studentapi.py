from fastapi import FastAPI, HTTPException, Path
from typing import List
from uuid import UUID
from fastapi.responses import JSONResponse
from model import StudentCreate, StudentDetails,StudentUpdate
from mongoconnect import insertStudent, get_all_students, delete_student_by_id
from mongoconnect import update_student_by_id



app = FastAPI()

# GET all students
@app.get("/students", response_model=List[StudentDetails])
async def read_students():
    try:
        students = await get_all_students()
        return students
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# POST a new student
@app.post("/students", status_code=201)
async def create_student(student: StudentCreate):
    try:
        created_student = await insertStudent(student)
        return {
            "message": "Student created successfully",
            "data": created_student.model_dump()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# DELETE a student by UUID
@app.delete("/students/{student_id}", status_code=204)
async def delete_student(student_id: UUID = Path(..., description="UUID of the student to delete")):
    try:
        deleted = await delete_student_by_id(student_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Student not found")
        return  # 204 No Content
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.put("/students/{student_id}", response_model=StudentDetails, status_code=200)
async def update_student(
    student: StudentUpdate,  # partial fields to update
    student_id: UUID = Path(..., description="UUID of the student to update")
):
    """
    Update any field of a student by UUID.
    Only the provided fields will be updated.
    Returns the updated student.
    """
    try:
        updated_student = await update_student_by_id(student_id, student)
        if not updated_student:
            raise HTTPException(status_code=404, detail="Student not found")
        return updated_student  # Swagger will display the updated StudentDetails
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



