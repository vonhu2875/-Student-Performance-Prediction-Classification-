from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import joblib
import pandas as pd
from datetime import datetime
from flask_cors import CORS  # Quan trọng: Để React có thể gọi được Flask

app = Flask(__name__)
CORS(app) # Cho phép React truy cập API
app = Flask(__name__)

# Cấu hình Database SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


# Tạo bảng lưu lịch sử dự đoán
class PredictionHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100))
    attendance = db.Column(db.Float)
    study_hours = db.Column(db.Float)
    prediction = db.Column(db.String(20))
    probability = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.now())


# Tạo Database (chạy 1 lần duy nhất)
with app.app_context():
    db.create_all()

# Load Model (Đảm bảo đường dẫn đúng tới file .pkl của Như)
model = joblib.load('models/final_best_student_model.pkl')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.json  # React sẽ gửi dữ liệu dạng JSON

    # 1. Trích xuất dữ liệu từ JSON
    name = data.get('name')
    attendance = float(data.get('attendance'))
    study_hours = float(data.get('study_hours'))
    prev_grade = float(data.get('prev_grade'))

    # 2. Tạo DataFrame và Tính toán Feature Engineering (Y hệt như bước trước mình làm)
    input_data = pd.DataFrame([{
        'Name': name, 'Gender': 'Male', 'AttendanceRate': attendance,
        'StudyHoursPerWeek': study_hours, 'PreviousGrade': prev_grade,
        'ExtracurricularActivities': 0, 'ParentalSupport': 'Medium',
        'Study Hours': study_hours, 'Attendance (%)': attendance,
        'Online Classes Taken': False
    }])
    input_data['Study_Attendance'] = input_data['StudyHoursPerWeek'] * input_data['AttendanceRate']
    input_data['Study_Efficiency'] = input_data['StudyHoursPerWeek'] / (input_data['AttendanceRate'] + 1)

    # 3. Dự đoán
    prediction = int(model.predict(input_data)[0])  # Chuyển về int để JSON đọc được
    prob = float(model.predict_proba(input_data)[0][prediction] * 100)

    result = "PASS" if prediction == 1 else "FAIL"

    # 4. (Tùy chọn) Lưu vào Database
    # ... (code lưu DB của Như) ...

    # 5. Trả về kết quả cho React
    return jsonify({
        'name': name,
        'prediction': result,
        'probability': round(prob, 2)
    })


if __name__ == '__main__':
    app.run(debug=True)