from fastapi import FastAPI, HTTPException
app=FastAPI()
students=[]
@app.get("/student/{student_id}")
def get_students(students:int):
    if students_id>len(student_id):
        raise HTTPException (status status_code=404, details="notfound")
    else:
        return students(student_id)
    
    