from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)

    # Corrected relationship name from "items" to "student"
    student = relationship("Student", back_populates="owner")

class Student(Base):
    __tablename__ = "student"

    id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String, index=True)
    student_age = Column(String, index=True)
    date_of_birth = Column(String, index=True)
    country = Column(String, index=True)
    gender = Column(String, index=True)
    image = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    # Corrected relationship name from "owner" to "items"
    owner = relationship("User", back_populates="student")
