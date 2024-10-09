from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db, AnalysisResult

rating_router = APIRouter()


class RatingForm(BaseModel):
    analysis_id: int
    score: int
    comment: str


# 별점 및 리뷰 저장
@rating_router.post("/")
async def submit_rating(rating_form: RatingForm, db: Session = Depends(get_db)):
    analysis_record = db.query(AnalysisResult).filter(AnalysisResult.analysis_id == rating_form.analysis_id).first()
    if not analysis_record:
        raise HTTPException(status_code=404, detail="Analysis ID not found.")

    analysis_record.score = rating_form.score
    analysis_record.comment = rating_form.comment
    try:
        db.commit()
        return {"message": "Rating and comment saved."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error while saving rating and comment.")
