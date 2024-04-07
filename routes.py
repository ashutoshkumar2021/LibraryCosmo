from fastapi import APIRouter, Body
from bson import ObjectId
from pydantic import BaseModel
from pydantic import validator
from db import students_collection
class Student(BaseModel):
    name: str
    age: int =0
    address: dict = {
        "city": str,
        "country": str
    }
    @validator("address")
    def validate_address(cls, value):
        if not isinstance(value, dict):
            raise ValueError("address must be a dictionary")
        return value

    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "age": 25,
                "address": {
                    "city": "New York",
                    "country": "USA"
                },
            }
        }


def studentEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "age": item["age"],
        "address": item["address"],
    }


def studentsEntity(entity) -> list:
    return [studentEntity(item) for item in entity]


student = APIRouter()

@student.post("/students", response_model=str, status_code=201)
async def create_student(student: Student = Body(...)):
  '''API to create a student in the system. All fields are mandatory and required while creating the student in the system.'''
  student_dict = student.dict()
  inserted_student = students_collection.insert_one(student_dict)
  return str(inserted_student.inserted_id)

@student.get("/students", response_model=list[Student])
async def list_students(country: str = None, age: int = None):
    '''An API to find a list of students. You can apply filters on this API by passing the query parameters as listed below.'''
    filters = {}
    if country:
        filters["address.country"] = country
    if age:
        filters["age"] = {"$gte": age}
    students = students_collection.find(filters)
    return [Student(**student) for student in students]


@student.get("/students/{student_id}", response_model=Student)
async def fetch_student(student_id: str):
    student = students_collection.find_one({"_id": ObjectId(student_id)})
    if student:
        student["id"] = str(student["_id"])
        return Student(**student)
    else:
        return None


@student.patch("/students/{student_id}", status_code=204)
async def update_student(student_id: str, student: Student = Body(None)):

    '''API to update the student's properties based on information provided. Not mandatory that all information would be sent in PATCH, only what fields are sent should be updated in the Database.'''
    update_data = {field: value for field, value in student.dict().items() if value}
    students_collection.update_one({"_id": ObjectId(student_id)}, {"$set": update_data})


@student.delete("/students/{student_id}", status_code=200)
async def delete_student(student_id: str):
    delete_result = students_collection.delete_one({"_id": ObjectId(student_id)})
    return {"deleted_count": delete_result.deleted_count}
