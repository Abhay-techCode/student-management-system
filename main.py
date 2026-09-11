from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from dotenv import load_dotenv
import os


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


if not SUPABASE_URL:
    raise RuntimeError("SUPABASE_URL is missing from .env")

if not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_KEY is missing from .env")


# =========================================================
# SUPABASE CONNECTION
# =========================================================

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# =========================================================
# FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="Student Management API",
    description="FastAPI backend connected to Supabase",
    version="1.0.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# ROOT
# =========================================================

@app.get("/")
def root():

    return {
        "message": "Student Management API is running",
        "database": "Supabase",
        "table": "students"
    }


# =========================================================
# DATABASE CONNECTION TEST
# =========================================================

@app.get("/health")
def health():

    try:

        response = (
            supabase
            .table("students")
            .select("id")
            .limit(1)
            .execute()
        )

        return {
            "status": "connected",
            "database": "Supabase",
            "table": "students"
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }


# =========================================================
# GET ALL STUDENTS
# =========================================================

@app.get("/students")
def get_students():

    try:

        response = (
            supabase
            .table("students")
            .select("id,name,course,marks")
            .order("id")
            .execute()
        )

        return {
            "success": True,
            "data": response.data
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# GET ONE STUDENT
# =========================================================

@app.get("/students/{student_id}")
def get_student(student_id: int):

    try:

        response = (
            supabase
            .table("students")
            .select("id,name,course,marks")
            .eq("id", student_id)
            .execute()
        )

        if not response.data:

            raise HTTPException(
                status_code=404,
                detail="Student not found"
            )

        return {
            "success": True,
            "data": response.data[0]
        }

    except HTTPException:

        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# ADD STUDENT
# =========================================================

@app.post("/students")
def add_student(
    name: str,
    course: str,
    marks: int
):

    if not name.strip():

        raise HTTPException(
            status_code=400,
            detail="Student name is required"
        )

    if not course.strip():

        raise HTTPException(
            status_code=400,
            detail="Course is required"
        )

    if marks < 0 or marks > 100:

        raise HTTPException(
            status_code=400,
            detail="Marks must be between 0 and 100"
        )

    try:

        response = (
            supabase
            .table("students")
            .insert({
                "name": name.strip(),
                "course": course.strip(),
                "marks": marks
            })
            .execute()
        )

        return {
            "success": True,
            "message": "Student added successfully",
            "data": response.data
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# UPDATE STUDENT
# =========================================================

@app.put("/students/{student_id}")
def update_student(
    student_id: int,
    name: str,
    course: str,
    marks: int
):

    if not name.strip():

        raise HTTPException(
            status_code=400,
            detail="Student name is required"
        )

    if not course.strip():

        raise HTTPException(
            status_code=400,
            detail="Course is required"
        )

    if marks < 0 or marks > 100:

        raise HTTPException(
            status_code=400,
            detail="Marks must be between 0 and 100"
        )

    try:

        # First check if student exists

        existing = (
            supabase
            .table("students")
            .select("id")
            .eq("id", student_id)
            .execute()
        )

        if not existing.data:

            raise HTTPException(
                status_code=404,
                detail="Student not found"
            )

        # Update existing record

        response = (
            supabase
            .table("students")
            .update({
                "name": name.strip(),
                "course": course.strip(),
                "marks": marks
            })
            .eq("id", student_id)
            .execute()
        )

        return {
            "success": True,
            "message": "Student updated successfully",
            "data": response.data
        }

    except HTTPException:

        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# DELETE STUDENT
# =========================================================

@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    try:

        # Check if student exists

        existing = (
            supabase
            .table("students")
            .select("id")
            .eq("id", student_id)
            .execute()
        )

        if not existing.data:

            raise HTTPException(
                status_code=404,
                detail="Student not found"
            )

        # Delete

        response = (
            supabase
            .table("students")
            .delete()
            .eq("id", student_id)
            .execute()
        )

        return {
            "success": True,
            "message": "Student deleted successfully"
        }

    except HTTPException:

        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# RUN WITH:
#
# uvicorn backend:app --reload
#
# =========================================================