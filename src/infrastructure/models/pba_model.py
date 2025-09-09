# infrastructure/models/pba_models.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from infrastructure.databases.base import Base  # tùy theo repo của bạn: Base từ nơi khởi tạo ORM

class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class QuestionBank(Base):
    __tablename__ = 'question_banks'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    teacher = relationship("Teacher", backref="banks")

class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    bank_id = Column(Integer, ForeignKey('question_banks.id'), nullable=False)
    subject = Column(String(100), nullable=False)  # e.g., "Chemistry"
    topic = Column(String(200), nullable=True)
    difficulty = Column(String(50), nullable=True)  # e.g., "easy","medium","hard"
    qtype = Column(String(50), nullable=False)  # 'mcq','short','fill'
    content = Column(Text, nullable=False)
    options = Column(JSON, nullable=True)  # list of options for MCQ: [{"key":"A","text":"..."}]
    answer = Column(String(200), nullable=False)  # canonical answer (e.g., "A" for mcq)
    explanation = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    bank = relationship("QuestionBank", backref="questions")

class Exam(Base):
    __tablename__ = 'exams'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.id'), nullable=False)
    meta = Column(JSON, nullable=True)  # store settings like number_of_questions, randomize etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    teacher = relationship("Teacher", backref="exams")

class ExamItem(Base):
    __tablename__ = 'exam_items'
    id = Column(Integer, primary_key=True)
    exam_id = Column(Integer, ForeignKey('exams.id'), nullable=False)
    question_id = Column(Integer, ForeignKey('questions.id'), nullable=False)
    order = Column(Integer, nullable=True)
    exam = relationship("Exam", backref="items")
    question = relationship("Question")

class Submission(Base):
    __tablename__ = 'submissions'
    id = Column(Integer, primary_key=True)
    exam_id = Column(Integer, ForeignKey('exams.id'), nullable=False)
    student_name = Column(String(200), nullable=True)
    student_id = Column(String(100), nullable=True)
    raw_text = Column(Text, nullable=True)  # OCR extracted text
    answers = Column(JSON, nullable=True)  # e.g., {"1":"A", "2":"C"}
    score = Column(Integer, nullable=True)
    graded = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    exam = relationship("Exam")
