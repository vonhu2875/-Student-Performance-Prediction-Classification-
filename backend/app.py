from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import os
from model import PredictionHistory
from database import db

app = Flask(__name__)
CORS(app)

# 1. Cấu hình Database SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///predictions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# LIÊN KẾT DB VỚI APP
db.init_app(app)

# 2. Định nghĩa Model Database (Lưu tất cả thông tin) ở file model.py


# Tạo bảng
with app.app_context():
    db.create_all()

# 3. Load Model AI
model_path = os.path.join('../models', 'final_best_student_model.pkl')
if os.path.exists(model_path):
    model = joblib.load(model_path)
else:
    print("CRITICAL: Không tìm thấy file model!")


@app.route('/')
def hello():
    return "Backend AI đang chạy thành công!"


@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.json

        # Kiểm tra lỗi nhập liệu cơ bản
        fields_to_check = ['study_hours', 'attendance', 'math_score', 'science_score', 'english_score']
        for field in fields_to_check:
            val = data.get(field)
            if val is None or val == "":
                return jsonify({'success': False, 'error': f"Thiếu dữ liệu: {field}"}), 400

            num_val = float(val)
            if num_val < 0:
                return jsonify({'success': False, 'error': f"{field} không được âm"}), 400

        # 4. Tạo DataFrame (Đồng bộ hóa 100% với CSV)
        input_df = pd.DataFrame([{
            'age': int(data.get('age', 18)),
            'gender': str(data.get('gender', 'male')).strip().lower(),
            'school_type': str(data.get('school_type', 'public')).strip().lower(),
            'parent_education': str(data.get('parent_education', 'high school')).strip().lower(),
            'study_hours': float(data['study_hours']),
            'attendance_percentage': float(data['attendance']),
            'internet_access': str(data.get('internet_access', 'yes')).strip().lower(),
            'travel_time': str(data.get('travel_time', '<15 min')).strip().lower(),
            'extra_activities': str(data.get('extra_activities', 'no')).strip().lower(),
            'study_method': str(data.get('study_method', 'notes')).strip().lower(),
            'math_score': float(data['math_score']),
            'science_score': float(data['science_score']),
            'english_score': float(data['english_score'])
        }])

        # Feature Engineering (giống lúc train)
        input_df['Study_Attendance'] = input_df['study_hours'] * input_df['attendance_percentage']
        input_df['Academic_Avg'] = (input_df['math_score'] + input_df['science_score'] + input_df['english_score']) / 3

        # 5. Dự đoán
        prediction = int(model.predict(input_df)[0])
        probabilities = model.predict_proba(input_df)[0]
        prob_value = float(probabilities[prediction] * 100)
        res_text = "PASS" if prediction == 1 else "FAIL"

        # 6. Lưu tất cả vào Database
        student_name = data.get('name', 'Unknown')
        new_entry = PredictionHistory(
            student_name=student_name,
            age=int(input_df['age'][0]),
            gender=input_df['gender'][0],
            school_type=input_df['school_type'][0],
            parent_education=input_df['parent_education'][0],
            study_hours=input_df['study_hours'][0],
            attendance=input_df['attendance_percentage'][0],
            math_score=input_df['math_score'][0],
            science_score=input_df['science_score'][0],
            english_score=input_df['english_score'][0],
            internet_access=input_df['internet_access'][0],
            travel_time=input_df['travel_time'][0],
            extra_activities=input_df['extra_activities'][0],
            study_method=input_df['study_method'][0],
            result=res_text,
            probability=round(prob_value, 2)
        )
        db.session.add(new_entry)
        db.session.commit()

        return jsonify({
            'success': True,
            'prediction': res_text,
            'probability': round(prob_value, 2),
            'pass_chance': round(float(probabilities[1] * 100), 2),
            'fail_chance': round(float(probabilities[0] * 100), 2)
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/history', methods=['GET'])
def get_history():
    history = PredictionHistory.query.order_by(PredictionHistory.timestamp.desc()).all()
    results = []
    for h in history:
        results.append({
            "id": h.id,
            "name": h.student_name,
            "details": {
                "age": h.age, "gender": h.gender, "school": h.school_type,
                "study": h.study_hours, "att": h.attendance, "method": h.study_method
            },
            "scores": {"math": h.math_score, "sci": h.science_score, "eng": h.english_score},
            "result": h.result,
            "prob": h.probability,
            "time": h.timestamp.strftime("%d/%m/%Y %H:%M")
        })
    return jsonify(results)


if __name__ == '__main__':
    app.run(port=8000, debug=True)