"""
Chalenge restfull API
"""
import logging
from logging.handlers import RotatingFileHandler
import asyncio
import structlog

from fastapi import Depends, FastAPI, HTTPException, UploadFile
from sqlalchemy.orm import Session

from . import crud, models, schemas, helpers
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def setup_logging():
    # Get the Logger
    _logger = logging.getLogger(__file__)
    
    # Set logging level
    _logger.setLevel(logging.INFO)
    
    # Configure log handler
    rotating_log_handler = RotatingFileHandler('/tmp/testLogFile.log', maxBytes=10000, backupCount=1)
    
    # Add RotatingFileHandler to the logger
    _logger.addHandler(rotating_log_handler)
    
    # Configure Structlog
    struct_logger = structlog.wrap_logger(
        _logger,
        wrapper_class=structlog.BoundLogger,
        context_class=dict,
        cache_logger_on_first_use=None,
        logger_factory_args=None
    )

    return struct_logger

log = setup_logging()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/report/{report_id}')
def read_report(report_id: int, db: Session = Depends(get_db)):
    log.info('GET /report/', report_id=report_id)
    db_report = crud.get_report(db, report_id=report_id)
    if db_report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    log.info('Response /report/', db_report=db_report)
    return db_report


@app.post("/report/new")
def create_report(file: UploadFile, db: Session = Depends(get_db)):
    log.info('POST /report/new', file=file.filename)
    if file.filename.split('.')[-1] not in ['csv', 'json']:
        raise HTTPException(status_code=415, detail='Unsupported Media Type')
    result = asyncio.run(helpers.process_file(file))
    db_report = crud.create_report(db, report=schemas.ReportCreate(file_name=file.filename, result=result))
    log.info('Response /report/new', db_report=db_report)
    return db_report


@app.get('/reports', response_model=list[schemas.Report])
def read_reports(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    log.info('GET /reports')
    reports = crud.get_reports(db, skip=skip, limit=limit)
    log.info('GET /reports', reports_len=len(reports))
    return reports
