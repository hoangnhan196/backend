# interfaces/controllers/exam_controller.py
from flask import Blueprint, request, jsonify
from services.exam_service import ExamService


exam_bp = Blueprint("exam", __name__, url_prefix="/exams")
service = ExamService()


@exam_bp.route("/", methods=["POST"])
def create_exam():
    data = request.json
    exam = service.create_exam(
        title=data.get("title"),
        teacher_id=data.get("teacher_id"),
        items=data.get("items", [])
    )
    return jsonify({"id": exam.id, "title": exam.title, "teacher_id": exam.teacher_id}), 201


@exam_bp.route("/", methods=["GET"])
def list_exams():
    teacher_id = request.args.get("teacher_id")
    exams = service.list_exams(teacher_id)
    return jsonify([{"id": e.id, "title": e.title} for e in exams])


@exam_bp.route("/<int:exam_id>", methods=["GET"])
def get_exam(exam_id):
    exam = service.get_exam(exam_id)
    if not exam:
        return jsonify({"error": "Exam not found"}), 404
    return jsonify({"id": exam.id, "title": exam.title, "teacher_id": exam.teacher_id})
