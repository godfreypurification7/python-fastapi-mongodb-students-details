from motor.motor_asyncio import AsyncIOMotorClient
from model import StudentCreate, StudentDetails,StudentUpdate
from uuid import uuid4, UUID
async def insertStudent(student: StudentCreate):
    uri = "mongodb://localhost:27017/studentsDB"
    client = AsyncIOMotorClient(uri)

    try:
        db = client.get_database()
        collection = db["students"]

        # Generate UUID for _id
        student_id = str(uuid4())

        # Convert StudentCreate to dict
        data = student.model_dump()
        data["_id"] = student_id  # store _id as UUID string

        # Insert into MongoDB
        await collection.insert_one(data)

        # Return StudentDetails with proper UUID type
        return StudentDetails(id=UUID(student_id), **student.model_dump())

    finally:
        client.close()


async def get_all_students():
    uri = "mongodb://localhost:27017/studentsDB"
    client = AsyncIOMotorClient(uri)
    students_list = []

    try:
        db = client.get_database()
        collection = db["students"]

        # Fetch all students
        async for doc in collection.find({}):
            students_list.append(
                StudentDetails(
                    id=UUID(doc["_id"]),  # convert string to UUID
                    studentName=doc["studentName"],
                    studentParentName=doc["studentParentName"],
                    studentEmail=doc["studentEmail"],
                    studentAddress=doc["studentAddress"],
                    sex=doc["sex"],
                    subject=doc["subject"],
                )
            )

        return students_list

    finally:
        client.close()
async def delete_student_by_id(student_id: UUID):
    uri = "mongodb://localhost:27017/studentsDB"
    client = AsyncIOMotorClient(uri)
    try:
        db = client.get_database()
        collection = db["students"]

        result = await collection.delete_one({"_id": str(student_id)})
        return result.deleted_count > 0
    finally:
        client.close()


async def update_student_by_id(student_id: UUID, student: StudentUpdate):
    uri = "mongodb://localhost:27017/studentsDB"
    client = AsyncIOMotorClient(uri)
    try:
        db = client.get_database()
        collection = db["students"]

        # Only include fields that are provided
        update_data = {k: v for k, v in student.model_dump().items() if v is not None}

        if not update_data:
            return None

        # Update only the provided fields
        result = await collection.update_one(
            {"_id": str(student_id)},
            {"$set": update_data}
        )

        if result.modified_count == 0:
            return None

        updated_doc = await collection.find_one({"_id": str(student_id)})

        if not updated_doc:
            return None

        # Convert MongoDB document to StudentDetails
        return StudentDetails(
            id=UUID(updated_doc["_id"]),
            studentName=updated_doc.get("studentName", ""),
            studentParentName=updated_doc.get("studentParentName", ""),
            studentEmail=updated_doc.get("studentEmail", ""),
            studentAddress=updated_doc.get("studentAddress", ""),
            sex=updated_doc.get("sex", ""),
            subject=updated_doc.get("subject", [])
        )
    finally:
        client.close()



