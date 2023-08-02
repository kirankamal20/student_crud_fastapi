from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def login(db: Session, email: str,password):
    user = db.query(models.User).filter(models.User.email == email).first()

    if user is not None:
        if user.password == password:
            return user
    else:
        return None

def get_users(db: Session):
    return db.query(models.User.email,models.User.id).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_all_student(db: Session):
    return db.query(models.Student).order_by(models.Student.id.asc()).all()

def retrive_students(db: Session,  student_id:int):
    return db.query(models.Student).filter(models.Student.id==student_id).all()


def add_student(db: Session, student: schemas.StudentBase, user_id: int):
    db_student = models.Student(**student.dict(), owner_id=user_id)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def delete_student(db:Session,student_id:int):
   db_student=db.query(models. Student).filter_by(id=student_id).first()
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