from fastapi import FastAPI
from pydantic import BaseModel

from .database import init_db, insert_feedback, fetch_all
from .llm import generate_user_response, summarize_review, recommend_action

app = FastAPI()
init_db()

class Feedback(BaseModel):
    rating: int
    review: str

@app.post("/submit")
def submit_feedback(data: Feedback):
    response = generate_user_response(data.rating, data.review)
    summary = summarize_review(data.review)
    action = recommend_action(data.rating)

    insert_feedback(
        data.rating,
        data.review,
        response,
        summary,
        action
    )

    return {"ai_response": response}

@app.get("/admin")
def admin_data():
    return fetch_all()
