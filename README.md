# python-fastapi-mongodb-students
Here is a detailed write‑up (around 4,000 characters) for your GitHub repository **`python-fastapi-mongodb-students-details`** (at `https://github.com/godfreypurification7/python-fastapi-mongodb-students-details`), which you can use in your README or project description:

---

This project, **python-fastapi-mongodb-students-details**, is a full‑fledged REST API built with **FastAPI** and **MongoDB** to manage student records. It provides a clean, well-structured backend service that supports creating, reading, updating, and deleting student data in an asynchronous, type-safe manner.

At its core, the API uses Pydantic models to define **request schemas**, **update schemas**, and **response schemas**, giving precise control over which fields are required, optional, or read-only. The `StudentCreate` model represents the data that a client needs to supply when creating a new student (name, parent name, email, address, sex, and subject list). For updates, the `StudentUpdate` model uses **optional fields**, allowing partial updates so that clients can send only the fields they want to change — other data remains intact. The `StudentDetails` response model extends the create schema by adding an `id` field, represented as a **UUID**, not the default MongoDB ObjectId.

Instead of relying on MongoDB's default `_id` ObjectId, this application uses **UUID strings** generated via `uuid4()` for each student. This design ensures consistency between Pydantic models and MongoDB storage, making data handling safer and more predictable. Internally, when inserting a new student, the code generates a UUID, stores it as a string in MongoDB under `_id`, and returns it to the client as a `UUID` object in the response.

The database integration is handled by **Motor**, the asynchronous MongoDB driver, which enables non-blocking database operations. This asynchrony is paired with FastAPI’s asynchronous endpoints, making the API highly performant and scalable.

Key API endpoints include:

1. **POST /students** – Create a new student. The user provides all required student fields (except `id`), and the server generates a UUID, stores the data, and returns a success message with the new student’s data.

2. **GET /students** – Retrieve a list of all students. Returns each student in the `StudentDetails` format, including their UUID.

3. **PUT /students/{student_id}** – Update any subset of student fields by UUID. Only the fields provided in the request are updated (using MongoDB’s `$set`), and other fields remain unchanged. The endpoint returns the full, updated student object, making it easy to verify changes.

4. **DELETE /students/{student_id}** – Delete a student by their UUID. If a student matching the ID is found, it is removed; otherwise, a 404 error is returned. A 204 (No Content) is returned on successful deletion.

In the database layer, the `update_student_by_id` function carefully builds an update dictionary by filtering out `None` values from the Pydantic `StudentUpdate` model. This ensures that only the explicitly provided fields are modified in MongoDB. After updating, the function fetches the modified document and converts it back into a `StudentDetails` model, preserving type consistency by converting the stored string `_id` back into a `UUID`.

This architecture promotes **clean separation of concerns**:

* **Models** (Pydantic) define how data should be validated and serialized.
* **Database layer** (Motor) handles all data persistence.
* **API layer** (FastAPI) handles client interaction, input validation, and formatted responses.

Using UUIDs for `_id` enhances type safety and avoids common issues with BSON ObjectIds when interacting with Python types. The use of Pydantic ensures that the API only accepts valid data, while the asynchronous MongoDB driver guarantees responsive, scalable operations.

To get started with the project, a user would:

1. Clone the repository from GitHub.
2. Install dependencies (FastAPI, Motor, Pydantic, etc.).
3. Run a MongoDB instance locally (e.g. at `mongodb://localhost:27017`).
4. Launch the FastAPI application using `uvicorn main:app --reload`.
5. Access the interactive Swagger UI at `http://localhost:8000/docs` to test all endpoints.

Future improvements for this project could include adding **validation rules** (such as email format, allowed values for `sex` or `subject`), **authentication** (to restrict who can edit or delete student records), **pagination** and **filtering** for the GET endpoint, and **error-handling enhancements** to provide more user-friendly validation messages.

In summary, `python-fastapi-mongodb-students-details` is a modern, asynchronous CRUD API that demonstrates best practices in combining FastAPI, Pydantic, Motor, and MongoDB — all while maintaining clean, maintainable code and a strong type-safe foundation.

