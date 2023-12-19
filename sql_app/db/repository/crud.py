import os
from sqlalchemy.orm import Session
from sql_app.core.hashing import Hasher

from sql_app.db  . models import models
from sql_app. schemas import schemas
from passlib.context import CryptContext




def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def login(db: Session, email: str,password):
    user = db.query(models.User).filter(models.User.email == email).first()

    if user is not None:
         hashedPassword=Hasher.  verify_password( password,  user.password)
         if hashedPassword is True:
            return user
    else:
        return None

def get_users(db: Session):
    return db.query(models.User ).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashedPassword = Hasher.get_password_hash(user.password)
    db_user = models.User(email=user.email, password= hashedPassword)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_all_student(db: Session,user_id:int):
    return  db.query(models.Student).filter(models.Student.owner_id==user_id).all()

# db.query(models.Student).order_by(models.Student.id.asc()).all()

def get_a_student(db: Session,  student_id:int,user_id:int):
    return db.query(models.Student).filter(models.Student.id==student_id,models.Student.owner_id==user_id).first()


def add_student(db: Session, student: schemas.StudentBase, user_id: int):
    db_student = models.Student(**student.dict(), owner_id=user_id)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def delete_student(db:Session,student_id:int,user_id):
   db_student=db.query(models. Student).filter_by(id=student_id,owner_id=user_id).first()
   db.delete(db_student)
   db.commit()
   return db_student

def update_student(db:Session,student_id:int,student: schemas.StudentBase):
   db_student=db.query(models.Student).get(student_id)
   if db_student:
        db_student.student_name = student.student_name
        db_student.student_age = student.student_age 
        db_student.date_of_birth = student.date_of_birth
        db_student.country = student.country
        db_student.gender = student.gender
        db_student.image = student.image
        db.commit()
   db.close()
   return db_student

def delete_file(file_name):
    file_path = f"images/{file_name}"
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"File {file_path} deleted successfully.")
    else:
        print(f"File {file_path} does not exist.")