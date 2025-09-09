# api/controllers/ocr_controller.py
import io
from flask import Blueprint, request, jsonify
from PIL import Image
import pytesseract
from services.pba_service import PBAService
from infrastructure.repositories.exam_repository import ExamRepository

ocr_bp = Blueprint('ocr', __name__, url_prefix='/api/ocr')
service = PBAService()

@ocr_bp.route('/grade/<int:exam_id>', methods=['POST'])
def grade_upload(exam_id):
    """
    POST multipart/form-data
    field 'file' - image/pdf
    Optional: 'student_name'
    """
    if 'file' not in request.files:
        return jsonify({"error": "file missing"}), 400
    f = request.files['file']
    try:
        img = Image.open(f.stream).convert('RGB')
    except Exception as e:
        return jsonify({"error": f"Failed to open image: {str(e)}"}), 400

    # Basic OCR
    text = pytesseract.image_to_string(img, lang='eng+vie')  # nếu có bộ chữ Việt
    # TODO: implement parsing strategy to map OCR text to answers.
    # Here we do a simple parse: lines contain "1. A" or "1)A" etc
    answers = {}
    import re
    for line in text.splitlines():
        line = line.strip()
        m = re.match(r'^\s*(\d+)\s*[\.\)\:-]?\s*([A-Za-z])\b', line)
        if m:
            qnum = m.group(1)
            ans = m.group(2).upper()
            answers[qnum] = ans

    # Call grade function
    result = service.grade_mcq_submission(exam_id, answers)
    # Save raw_text and answers in submission (via repo inside service)
    return jsonify({"ocr_text": text[:5000], "parsed_answers": answers, "grading": result})
