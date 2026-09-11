from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import Session

from database import Base, engine, get_db


app = FastAPI(title="Student Management System")


# -------------------------
# CORS
# -------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "https://student-management-system-kappa-roan.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------
# Database Model
# -------------------------

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    course = Column(String, nullable=False)
    marks = Column(Float, nullable=False)


# Create table automatically
Base.metadata.create_all(bind=engine)


# -------------------------
# Home
# -------------------------

@app.get("/")
def home():
    return {
        "message": "Student Management System API is running"
    }


# -------------------------
# GET ALL STUDENTS
# -------------------------

@app.get("/students")
def get_students(db: Session = Depends(get_db)):

    students = db.query(Student).all()

    data = []

    for student in students:
        data.append({
            "id": student.id,
            "name": student.name,
            "course": student.course,
            "marks": student.marks
        })

    return {
        "data": data
    }


# -------------------------
# ADD STUDENT
# -------------------------

@app.post("/students")
def add_student(
    name: str,
    course: str,
    marks: float,
    db: Session = Depends(get_db)
):

    student = Student(
        name=name,
        course=course,
        marks=marks
    )

    db.add(student)
    db.commit()
    db.refresh(student)

    return {
        "message": "Student added successfully",
        "data": {
            "id": student.id,
            "name": student.name,
            "course": student.course,
            "marks": student.marks
        }
    }


# -------------------------
# UPDATE STUDENT
# -------------------------

@app.put("/students/{student_id}")
def update_student(
    student_id: int,
    name: str,
    course: str,
    marks: float,
    db: Session = Depends(get_db)
):

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    student.name = name
    student.course = course
    student.marks = marks

    db.commit()
    db.refresh(student)

    return {
        "message": "Student updated successfully",
        "data": {
            "id": student.id,
            "name": student.name,
            "course": student.course,
            "marks": student.marks
        }
    }


# -------------------------
# DELETE STUDENT
# -------------------------

@app.delete("/students/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    db.delete(student)
    db.commit()

    return {
        "message": "Student deleted successfully"
    }
