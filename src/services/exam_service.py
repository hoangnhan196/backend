# application/services/exam_service.py
from infrastructure.repositories.exam_repository import ExamRepository
from infrastructure.models.pba_model import Exam, ExamItem


class ExamService:
    def __init__(self, repo: ExamRepository = None):
        self.repo = repo or ExamRepository()

    def create_exam(self, title: str, teacher_id: int, items: list = None):
        exam = Exam(title=title, teacher_id=teacher_id)
        exam = self.repo.add(exam)

        if items:
            for i, question_id in enumerate(items):
                exam_item = ExamItem(exam_id=exam.id, question_id=question_id, order=i + 1)
                self.repo.add_item(exam_item)

        return exam

    def get_exam(self, exam_id: int):
        return self.repo.get_by_id(exam_id)

    def list_exams(self, teacher_id=None):
        return self.repo.list(teacher_id=teacher_id)

    def list_items(self, exam_id: int):
        return self.repo.list_items(exam_id)
