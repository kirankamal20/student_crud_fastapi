from pydantic import BaseModel


class StudentBase(BaseModel):
    student_name: str
    student_age: str 
    gender: str
    country: str
    date_of_birth: str
    image: str


class StudentCreate(StudentBase):
    pass


class Student(StudentBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Student] = []

     
        
 