# infrastructure/repositories/question_repository.py
from infrastructure.models.pba_model import Question, QuestionBank
from infrastructure.databases.mssql import db_session  # theo repo
from sqlalchemy.orm import Session

class QuestionRepository:
    def __init__(self, session: Session = db_session):
        self.session = session

    def add(self, question: Question):
        self.session.add(question)
        self.session.commit()
        self.session.refresh(question)
        return question

    def get_by_id(self, qid: int):
        return self.session.query(Question).filter(Question.id == qid).one_or_none()

    def list(self, bank_id=None, subject=None, topic=None, difficulty=None, qtype=None, limit=100, offset=0):
        q = self.session.query(Question)
        if bank_id: q = q.filter(Question.bank_id == bank_id)
        if subject: q = q.filter(Question.subject == subject)
        if topic: q = q.filter(Question.topic == topic)
        if difficulty: q = q.filter(Question.difficulty == difficulty)
        if qtype: q = q.filter(Question.qtype == qtype)
        return q.offset(offset).limit(limit).all()

    def search(self, text, limit=50):
        return self.session.query(Question).filter(Question.content.ilike(f"%{text}%")).limit(limit).all()
