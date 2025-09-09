# interfaces/controllers/submission_controller.py
from flask import Blueprint, request, jsonify
from services.submission_service import SubmissionService

submission_bp = Blueprint("submission", __name__, url_prefix="/submissions")
service = SubmissionService()


@submission_bp.route("/", methods=["POST"])
def create_submission():
    data = request.json
    sub = service.create_submission(
        exam_id=data.get("exam_id"),
        student_id=data.get("student_id"),
        answers=data.get("answers", {})
    )
    return jsonify({"id": sub.id, "exam_id": sub.exam_id, "student_id": sub.student_id}), 201


@submission_bp.route("/", methods=["GET"])
def list_submissions():
    exam_id = request.args.get("exam_id")
    student_id = request.args.get("student_id")
    submissions = service.list_submissions(exam_id, student_id)
    return jsonify([{"id": s.id, "exam_id": s.exam_id, "student_id": s.student_id} for s in submissions])


@submission_bp.route("/<int:sid>", methods=["GET"])
def get_submission(sid):
    sub = service.get_submission(sid)
    if not sub:
        return jsonify({"error": "Submission not found"}), 404
    return jsonify({"id": sub.id, "exam_id": sub.exam_id, "student_id": sub.student_id, "score": sub.score})


@submission_bp.route("/<int:sid>/score", methods=["PUT"])
def grade_submission(sid):
    data = request.json
    sub = service.grade_submission(sid, score=data.get("score"), answers=data.get("answers"))
    if not sub:
        return jsonify({"error": "Submission not found"}), 404
    return jsonify({"id": sub.id, "score": sub.score, "graded": sub.graded})
