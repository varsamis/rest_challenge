"""
Chalenge restfull API
"""
from fastapi import Depends, FastAPI, HTTPException, UploadFile
from sqlalchemy.orm import Session

from . import crud, models, schemas, helpers
from .database import SessionLocal, engine

import asyncio

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/report/{report_id}')
def read_report(report_id: int, db: Session = Depends(get_db)):
    db_report = crud.get_report(db, report_id=report_id)
    if db_report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return db_report


@app.post("/report/new")
def create_report(file: UploadFile, db: Session = Depends(get_db)):
    if file.filename.split('.')[-1] not in ['csv', 'json']:
        raise HTTPException(status_code=415, detail='Unsupported Media Type')
    result = asyncio.run(helpers.process_file(file))
    db_report = crud.create_report(db, report=schemas.ReportCreate(file_name=file.filename, result=result))
    return db_report


@app.get('/reports', response_model=list[schemas.Report])
def read_reports(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    reports = crud.get_reports(db, skip=skip, limit=limit)
    return reports
    