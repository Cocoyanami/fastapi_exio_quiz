from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from typing import Dict, List

app = FastAPI()

class QuizData(BaseModel):
    question: int  # Pregunta como entero
    answer: int    # Respuesta como entero

# Diccionario para almacenar las preguntas y respuestas por usuario
user_quiz_data: Dict[EmailStr, List[QuizData]] = {}

@app.get("/")
def index():
    return {"message": "Bienvenido al sistema de preguntas y respuestas del quiz."}

@app.post("/add_question/{user_email}")
def add_question(user_email: EmailStr, data: QuizData):
    if user_email not in user_quiz_data:
        user_quiz_data[user_email] = []

    if len(user_quiz_data[user_email]) < 24:
        user_quiz_data[user_email].append(data)
        return {"message": "Pregunta añadida con éxito."}
    else:
        return {"message": "Límite de preguntas alcanzado para este usuario."}

@app.get("/questions/{user_email}")
def get_questions(user_email: EmailStr):
    if user_email in user_quiz_data:
        return {"questions": user_quiz_data[user_email]}
    else:
        return {"message": "No hay preguntas almacenadas para este usuario."}

@app.get("/question/{user_email}/{id}")
def mostrar_respuestas(user_email: EmailStr, id: int):
    if user_email in user_quiz_data:
        if 0 <= id < len(user_quiz_data[user_email]):
            return user_quiz_data[user_email][id]
        else:
            return {"message": "ID de pregunta no válido."}
    else:
        return {"message": "No hay preguntas almacenadas para este usuario."}


# Obtener pregunta y respuesta específica de un usuario
@app.get("/question_answer/{user_email}/{id}")
def get_question_answer(user_email: EmailStr, id: int):
    if user_email in user_quiz_data:
        if 0 <= id < len(user_quiz_data[user_email]):
            quiz_data = user_quiz_data[user_email][id]
            return {"question": quiz_data.question, "answer": quiz_data.answer}
        else:
            return {"message": "ID de pregunta no válido."}
    else:
        return {"message": "No hay preguntas almacenadas para este usuario."}