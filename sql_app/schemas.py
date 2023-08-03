from pydantic import BaseModel 


class StudentBase(BaseModel):
    student_name: str
    student_age: str 
    gender: str
    country: str
    date_of_birth: str
    image: str

class Student(StudentBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email:str
    #     EmailStr

    # def __repr__(self):
    #     return f"UserBase(email={self.email})"


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items:  Student 

class DeleteStudent(BaseModel):
    user_id:int
    student_id:int
class GetAStudent(BaseModel):
    user_id:int
    student_id:int
        
 