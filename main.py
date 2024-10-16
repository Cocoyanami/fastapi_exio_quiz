from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Dict, List

app = FastAPI()

# Permitir CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes especificar dominios específicos en lugar de "*"
    allow_credentials=True,
    allow_methods=["*"],  # Permitir cualquier método (GET, POST, etc.)
    allow_headers=["*"],  # Permitir cualquier encabezado
)


class QuizData(BaseModel):
    question: int  # Valor de la pregunta
    answer: int    # Valor de la respuesta seleccionada


# Diccionario para almacenar las preguntas y respuestas por usuario
user_quiz_data: Dict[EmailStr, List[QuizData]] = {}

@app.get("/")
def index():
    return {"message": "Bienvenido al sistema de preguntas y respuestas del quiz."}

@app.post("/saveAnswers")
def save_answers(email: EmailStr, answers: List[QuizData]):
    if email not in user_quiz_data:
        user_quiz_data[email] = []  # Inicializa los datos del usuario si no existen
    
    for answer in answers:
        user_quiz_data[email].append(answer)

    return {"message": "Respuestas guardadas con éxito."}


@app.get("/questions/{user_email}")
def get_questions(user_email: EmailStr):
    if user_email in user_quiz_data:
        return {"questions": user_quiz_data[user_email]}
    else:
        raise HTTPException(status_code=404, detail="No hay preguntas almacenadas para este usuario.")

@app.get("/question/{user_email}/{id}")
def mostrar_respuestas(user_email: EmailStr, id: int):
    if user_email in user_quiz_data:
        if 0 <= id < len(user_quiz_data[user_email]):
            return user_quiz_data[user_email][id]
        else:
            raise HTTPException(status_code=404, detail="ID de pregunta no válido.")
    else:
        raise HTTPException(status_code=404, detail="No hay preguntas almacenadas para este usuario.")

# Obtener pregunta y respuesta específica de un usuario
@app.get("/question_answer/{user_email}/{id}")
def get_question_answer(user_email: EmailStr, id: int):
    if user_email in user_quiz_data:
        if 0 <= id < len(user_quiz_data[user_email]):
            quiz_data = user_quiz_data[user_email][id]
            return {"question": quiz_data.question, "answer": quiz_data.answer}
        else:
            raise HTTPException(status_code=404, detail="ID de pregunta no válido.")
    else:
        raise HTTPException(status_code=404, detail="No hay preguntas almacenadas para este usuario.")
