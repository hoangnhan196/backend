# application/services/submission_service.py
from infrastructure.repositories.submission_repository import SubmissionRepository
from infrastructure.models.pba_model import Submission


class SubmissionService:
    def __init__(self, repo: SubmissionRepository = None):
        self.repo = repo or SubmissionRepository()

    def create_submission(self, exam_id: int, student_id: int, answers: dict):
        submission = Submission(exam_id=exam_id, student_id=student_id, answers=answers)
        return self.repo.add(submission)

    def get_submission(self, submission_id: int):
        return self.repo.get_by_id(submission_id)

    def list_submissions(self, exam_id=None, student_id=None):
        return self.repo.list(exam_id=exam_id, student_id=student_id)

    def grade_submission(self, submission_id: int, score: int, answers: dict = None):
        return self.repo.update_score(submission_id, score, answers)
