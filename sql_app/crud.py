from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def login(db: Session, email: str ):
    user = db.query(models.User).filter(models.User.email == email).first()
    return user

def get_users(db: Session):
    return db.query(models.User).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_all_student(db: Session):
    return db.query(models.Student).order_by(models.Student.id.asc()).all()

def retrive_students(db: Session,  student_id:int):
    return db.query(models.Student).filter(models.Student.id==student_id).all()


def add_student(db: Session, student: schemas.StudentCreate, user_id: int):
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

def update_student(db:Session,student_id:int,student: schemas.StudentCreate):
   db_student=db.query(models.Student).get(student_id)
   if db_student:
        db_student.title = student.title
        db_student.description = student.description
        db.commit()

    # close the session
   db.close()
   return db_student