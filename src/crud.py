from sqlalchemy.orm import Session

from . import models, schemas

def get_report(db: Session, report_id: int):
    return db.query(models.Report).filter(models.Report.id == report_id).first()

def get_report_by_file_name(db: Session, file_name: str):
    return db.query(models.Report).filter(models.Report.file_name == file_name).first()

def get_reports(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Report).offset(skip).limit(limit).all()


def create_report(db: Session, report: schemas.ReportCreate):
    db_report = models.Report(file_name=report.file_name, result=report.result)
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report
