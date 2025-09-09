# infrastructure/repositories/submission_repository.py
from sqlalchemy.orm import Session
from infrastructure.models.pba_model import Submission
from infrastructure.databases.mssql import db_session


class SubmissionRepository:
    def __init__(self, session: Session = db_session):
        self.session = session

    def add(self, submission: Submission):
        """Thêm submission (bài nộp) mới"""
        self.session.add(submission)
        self.session.commit()
        self.session.refresh(submission)
        return submission

    def get_by_id(self, sid: int):
        """Lấy submission theo ID"""
        return self.session.query(Submission).filter(Submission.id == sid).one_or_none()

    def list(self, exam_id=None, student_id=None, limit=50, offset=0):
        """Danh sách submission theo exam hoặc student"""
        q = self.session.query(Submission)
        if exam_id:
            q = q.filter(Submission.exam_id == exam_id)
        if student_id:
            q = q.filter(Submission.student_id == student_id)
        return q.order_by(Submission.created_at.desc()).offset(offset).limit(limit).all()

    def update_score(self, sid: int, score: int, answers: dict = None):
        """Cập nhật điểm và đáp án đã chấm"""
        submission = self.get_by_id(sid)
        if not submission:
            return None
        submission.score = score
        submission.graded = True
        if answers:
            submission.answers = answers
        self.session.commit()
        self.session.refresh(submission)
        return submission
