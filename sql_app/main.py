import os
from typing import Annotated
from click import File
from fastapi import Depends, FastAPI, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from fastapi import File, UploadFile, FastAPI
from . import crud, models, schemas
from .database import SessionLocal, engine
from fastapi import UploadFile
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/login",response_model=schemas.User)
def loginUser(user: schemas.UserCreate ,db:Session = Depends(get_db)):
    db_user = crud.login(db , email=user.email )
    if not db_user:
        raise HTTPException(status_code=401, detail="Incorrect username") 
    raise HTTPException(status_code=200, detail="Successfully Logged")
       


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users( db: Session = Depends(get_db)):
    users = crud.get_users(db)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/students/", response_model=schemas.Student)
async def add_student(
    user_id: int, student_name: Annotated[str, Form()], student_age: Annotated[str, Form()],date_of_birth: Annotated[str, Form()] ,gender: Annotated[str, Form()],country: Annotated[str, Form()], image:  UploadFile = File(...) , db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    file_name = os.path.basename(image.filename)
    file_path = f"images/{file_name}"

    # Create the 'images' directory if it doesn't exist
    os.makedirs("images", exist_ok=True)
    with open(file_path, "wb") as f:
        contents = await image.read()  # Read the contents of the file
        f.write(contents)
    data = schemas.StudentCreate( student_name = student_name,student_age = student_age,date_of_birth = date_of_birth,country = country,gender = gender,image = file_name) 
    return crud.add_student(db=db, student = data, user_id=user_id)
     


@app.get("/students/", response_model=list[schemas.Student])
def read_student( db: Session = Depends(get_db)):
    students = crud.get_all_student(db)
    return students


@app.delete("/delete/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = crud.retrive_students(db, student_id=student_id)
    print(student)
    if not student:
        raise HTTPException(status_code=404, detail="student not found")
    crud.delete_student(db, student_id=student_id)
    return {"message": "student deleted successfully"}

@app.put("/update/{student_id}")
def update_student(student_id: int,student: schemas.StudentCreate,db:Session = Depends(get_db)):
    # try:  
        data = crud. retrive_students(db, student_id=student_id)
        print(data)
        if not data:
            raise HTTPException(status_code=404, detail="student not found")
        crud.update_student(db=db,  student_id=student_id,student=student)
        return {"message":"successfully updated"}
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))
@app.get("/download-image/{file_name}")
async def download_file(file_name: str):
    file_path = f"images/{file_name}"
    return FileResponse(file_path)