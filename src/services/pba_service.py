# services/pba_service.py
import random
from infrastructure.repositories.question_repository import QuestionRepository
from infrastructure.repositories.exam_repository import ExamRepository
from infrastructure.repositories.submission_repository import SubmissionRepository
from infrastructure.models.pba_model import Exam, ExamItem, Submission, Question
from infrastructure.databases.mssql import db_session

class PBAService:
    def __init__(self):
        self.qrepo = QuestionRepository()
        self.erepo = ExamRepository()
        self.srepo = SubmissionRepository()

    def create_question(self, data):
        q = Question(**data)
        return self.qrepo.add(q)

    def generate_exam(self, teacher_id, title, filters: dict, number_of_questions: int, randomize=True):
        # filters can be {subject, topic, difficulty}
        candidates = self.qrepo.list(**filters, limit=1000)
        if not candidates:
            raise ValueError("No questions found for filters")
        chosen = random.sample(candidates, min(number_of_questions, len(candidates)))
        exam = Exam(title=title, teacher_id=teacher_id, meta={"filters": filters, "number": number_of_questions})
        exam = self.erepo.add(exam)
        for i, q in enumerate(chosen, start=1):
            item = ExamItem(exam_id=exam.id, question_id=q.id, order=i)
            db_session.add(item)
        db_session.commit()
        return exam

    def grade_mcq_submission(self, exam_id, answer_map: dict):
        # answer_map: {"1": "A", "2": "C"} keys are exam_item order or question_id
        exam = self.erepo.get_by_id(exam_id)
        items = exam.items
        total = len(items)
        correct = 0
        answers_record = {}
        for item in items:
            q = item.question
            key = str(item.order)
            student_answer = answer_map.get(key) or answer_map.get(str(q.id))
            correct_answer = q.answer
            answers_record[key] = {"student": student_answer, "correct": correct_answer}
            if student_answer and student_answer.strip().upper() == correct_answer.strip().upper():
                correct += 1
        score = int(100 * correct / total) if total else 0
        submission = Submission(exam_id=exam_id, answers=answer_map, score=score, graded=True)
        submission = self.srepo.add(submission)
        return {"score": score, "total": total, "correct": correct, "submission_id": submission.id, "details": answers_record}
