from pydantic import BaseModel

class Student(BaseModel):
    name: str
    age: int
    address: dict = {"city": str, "country": str}

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
