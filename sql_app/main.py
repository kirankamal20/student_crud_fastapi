import os
from typing_extensions import Annotated
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
def login(user: schemas.UserCreate ,db:Session = Depends(get_db)):
    try:
        db_user = crud.login(db , email=user.email,password=user.password )
        if not db_user:
            raise HTTPException(status_code=401, detail="Incorrect username or password") 
        raise HTTPException(status_code=200, detail={"message":"Successfully Logged","id":db_user.id})
    except HTTPException as ex: 
        print(ex.detail)
        raise HTTPException(status_code=ex.status_code, detail=ex.detail)
       



@app.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        if not user.email:
            raise HTTPException(status_code=400, detail="Email cannot be empty")
        else:
            db_user = crud.get_user_by_email(db, email=user.email)
            if db_user:
                raise HTTPException(status_code=400, detail="Email already registered")
            return crud.create_user(db=db, user=user)
    except HTTPException as ex:
        print(ex.detail)
        raise HTTPException(status_code=ex.status_code, detail=ex.detail)
 
@app.get("/getallUsers/")
def getallstudents( db: Session = Depends(get_db)):
    try:
        users = crud.get_users(db)
        return users
    except HTTPException as ex: 
        print(ex.detail)
        raise HTTPException(status_code=ex.status_code, detail=ex.detail)


@app.get("/getAstudent/{student_id}",)
def get_student(student_id: int, db: Session = Depends(get_db)):
    try:
        db_user = crud.retrive_students(db, student_id = student_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="student not found")
        return db_user
    except HTTPException as ex: 
        print(ex.detail)
        raise HTTPException(status_code=ex.status_code, detail=ex.detail)


@app.post("/addstudent/{user_id}")
async def add_student(
    user_id: int,student_name: Annotated[str, Form()], student_age: Annotated[str, Form()],date_of_birth: Annotated[str, Form()] ,gender: Annotated[str, Form()],country: Annotated[str, Form()], image:  UploadFile = File(...) ,  db: Session = Depends(get_db)):
    try:
        db_user = crud.get_user(db, user_id=user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
         
        if image.filename is not None:
            file_name = os.path.basename(image.filename)
        else:
            file_name = ""
        file_path = f"images/{file_name}"
    

    # Create the 'images' directory if it doesn't exist
        os.makedirs("images", exist_ok=True)
        with open(file_path, "wb") as f:
            contents = await image.read()  # Read the contents of the file
            f.write(contents)
        data = schemas.StudentBase( student_name = student_name,student_age = student_age,date_of_birth = date_of_birth,country = country,gender = gender,image = file_name) 
        return crud.add_student(db=db, student = data, user_id=user_id)
    except HTTPException as ex: 
        print(ex.detail)
        raise HTTPException(status_code=ex.status_code, detail=ex.detail)
    
@app.get("/getAllstudents/", )
def get_all_students( db: Session = Depends(get_db)):
    try:
        students = crud.get_all_student(db)
        return students
    except HTTPException as ex: 
        print(ex.detail)
        raise HTTPException(status_code=ex.status_code, detail=ex.detail)


@app.delete("/delete/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    try:
        student = crud.retrive_students(db, student_id=student_id)
        print(student)
        if not student:
            raise HTTPException(status_code=404, detail="student not found")
        crud.delete_student(db, student_id=student_id)
        return {"message": "student deleted successfully"}
    except HTTPException as ex: 
        print(ex.detail)
        raise HTTPException(status_code=ex.status_code, detail=ex.detail)

@app.put("/update/{student_id}")
async def update_student(student_id: int,student_name: Annotated[str, Form()], student_age: Annotated[str, Form()],date_of_birth: Annotated[str, Form()] ,gender: Annotated[str, Form()],country: Annotated[str, Form()], image:  UploadFile = File(...) , db: Session = Depends(get_db)):
     try:  
        data = crud. retrive_students(db, student_id=student_id)
        print(data)
        if not data:
            raise HTTPException(status_code=404, detail="student not found")
        
        if image.filename is not None:
            file_name = os.path.basename(image.filename)
        else:
          file_name = ""
          file_path = f"images/{file_name}"
                    # Create the 'images' directory if it doesn't exist
          os.makedirs("images", exist_ok=True)
          with open(file_path, "wb") as f:
           contents = await image.read()  # Read the contents of the file
          f.write(contents)
        student = schemas.StudentBase( student_name = student_name,student_age = student_age,date_of_birth = date_of_birth,country = country,gender = gender,image = file_name) 
        crud.update_student(db=db,  student_id=student_id,student=student)
        return {"message":"successfully updated"}
     except HTTPException as ex: 
        print(ex.detail)
        raise HTTPException(status_code=ex.status_code, detail=ex.detail)
    
@app.get("/download-image/{file_name}")
async def download_file(file_name: str):
    try:
       file_path = f"images/{file_name}"
       return FileResponse(file_path)
    except HTTPException as ex: 
        print(ex.detail)
        raise HTTPException(status_code=ex.status_code, detail=ex.detail)