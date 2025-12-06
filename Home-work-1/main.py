from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Dict, List
import uvicorn

# Initialize FastAPI app
app = FastAPI(title="Мини-анкета", description="Веб приложение для сбора анкет пользователей")

# Hardcoded questions
QUESTIONS = [
    {"id": 1, "text": "Как вас зовут?"},
    {"id": 2, "text": "Сколько вам лет?"},
    {"id": 3, "text": "Какой ваш любимый язык программирования?"},
    {"id": 4, "text": "Оцените этот опрос от 1 до 10"}
]

# In-memory storage for answers (dictionary of dictionaries)
answers_storage: Dict[str, Dict[int, str]] = {}

# Models
class Answer(BaseModel):
    question_id: int
    answer_text: str

class UserAnswers(BaseModel):
    username: str
    answers: List[Answer]

# API Endpoints
@app.get("/questions")
def get_questions():
    """Return the list of questions"""
    return QUESTIONS

@app.post("/answers")
def save_answers(user_answers: UserAnswers):
    """Save user answers to memory storage"""
    username = user_answers.username
    answers = user_answers.answers
    
    # Initialize user entry if not exists
    if username not in answers_storage:
        answers_storage[username] = {}
    
    # Save each answer
    for answer in answers:
        answers_storage[username][answer.question_id] = answer.answer_text
    
    return {"message": "Ответы успешно сохранены"}

# Serve frontend
@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("index.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read())

# Serve static files
app.mount("/", StaticFiles(directory=".", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8082)