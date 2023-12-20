import os
from typing_extensions import Annotated
 
from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from fastapi import File, UploadFile
from sql_app.db.repository import crud
from sql_app.db.session import get_db
from sql_app.schemas import schemas
from sql_app.core.security import verify_token
from fastapi import UploadFile
 
router = APIRouter(tags=["CRUD Operations"] )
 
@router.get("/getallUsers")
async def getAllUsers(db: Session = Depends(get_db), token: str = Depends(verify_token)):
    try:
        print(token)
        users = crud.get_users(db)
        if users is None:
             raise HTTPException(status_code=404, detail="Users are not found")
        return users
    except HTTPException as ex: 
        print(ex.detail)
        raise HTTPException(status_code=ex.status_code, detail=ex.detail)


@router.post("/getAstudent")
def get_a_student(student_id: int, db: Session = Depends(get_db),userid: str = Depends(verify_token)):
    try:
        db_user = crud.get_user(db, user_id= int(userid) )
        student = crud.get_a_student(db=db,student_id=student_id ,user_id=  int(userid) )
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        elif student is None:
             raise HTTPException(status_code=404, detail="student not found")
        else:
         return student
    except HTTPException as ex: 
        print(ex.detail)
        raise HTTPException(status_code=ex.status_code, detail=ex.detail)


@router.post("/addstudent")
async def add_student(
     student_name: Annotated[str, Form()], student_age: Annotated[str, Form()],date_of_birth: Annotated[str, Form()] ,gender: Annotated[str, Form()],country: Annotated[str, Form()], image:  UploadFile = File(...) ,  db: Session = Depends(get_db),user_id: str = Depends(verify_token)):
    try:
        db_user = crud.get_user(db, user_id=int(user_id))
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
        return crud.add_student(db=db, student = data, user_id=int(user_id))
    except HTTPException as ex: 
        print(ex.detail)
        raise HTTPException(status_code=ex.status_code, detail=ex.detail)
    
@router.get("/getAllstudents", )
def get_all_students(  db: Session = Depends(get_db),user_id: str = Depends(verify_token)):
    try:
        students = crud.get_all_student(db=db,user_id=int(user_id))
        if students is None:
             return []
        return students
    except HTTPException as ex: 
        print(ex.detail)
        raise HTTPException(status_code=ex.status_code, detail=ex.detail)


@router.delete("/delete")
def delete_student( student_id: int, db: Session = Depends(get_db),user_id: str = Depends(verify_token)):
    try:
        db_user = crud.get_user(db, user_id= int(user_id))
        student = crud.get_a_student(db=db,student_id=student_id,user_id=int(user_id))
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        elif student is None:
             raise HTTPException(status_code=404, detail="student not found")
        else:
            crud.delete_student(db, student_id=student_id,user_id=int(user_id))
            crud.delete_file(file_name=student.image)
            return {"message": "student deleted successfully",}   
    except HTTPException as ex: 
        print(ex.detail)
        raise HTTPException(status_code=ex.status_code, detail=ex.detail)

@router.put("/update")
async def update_student(   student_id: Annotated[int, Form()],student_name: Annotated[str, Form()], student_age: Annotated[str, Form()],date_of_birth: Annotated[str, Form()] ,gender: Annotated[str, Form()],country: Annotated[str, Form()], image:  UploadFile = File(...) , db: Session = Depends(get_db),user_id: str = Depends(verify_token)):
     try:  
        db_user = crud.get_user(db, user_id=int(user_id))
        student = crud.get_a_student(db=db,student_id=student_id,user_id=int(user_id))
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        elif student is None:
             raise HTTPException(status_code=404, detail="student not found")
        else:
        
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
    
@router.get("/download-image/{file_name}")
async def download_file(file_name: str):
    try:
       file_path = f"images/{file_name}"
       return FileResponse(file_path)
    except HTTPException as ex: 
        print(ex.detail)
        raise HTTPException(status_code=ex.status_code, detail=ex.detail)
    
 
        
 