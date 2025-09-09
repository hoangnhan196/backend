# infrastructure/repositories/exam_repository.py
from sqlalchemy.orm import Session
from infrastructure.models.pba_model import Exam, ExamItem
from infrastructure.databases.mssql import db_session


class ExamRepository:
    def __init__(self, session: Session = db_session):
        self.session = session

    def add(self, exam: Exam):
        """Thêm exam mới"""
        self.session.add(exam)
        self.session.commit()
        self.session.refresh(exam)
        return exam

    def get_by_id(self, exam_id: int):
        """Lấy exam theo ID (bao gồm items và câu hỏi)"""
        return (
            self.session.query(Exam)
            .filter(Exam.id == exam_id)
            .options()
            .one_or_none()
        )

    def list(self, teacher_id=None, limit=50, offset=0):
        """Danh sách exam theo giáo viên (nếu có)"""
        q = self.session.query(Exam)
        if teacher_id:
            q = q.filter(Exam.teacher_id == teacher_id)
        return q.order_by(Exam.created_at.desc()).offset(offset).limit(limit).all()

    def add_item(self, item: ExamItem):
        """Thêm một ExamItem"""
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def list_items(self, exam_id: int):
        """Lấy danh sách ExamItem của một exam"""
        return (
            self.session.query(ExamItem)
            .filter(ExamItem.exam_id == exam_id)
            .order_by(ExamItem.order.asc())
            .all()
        )
