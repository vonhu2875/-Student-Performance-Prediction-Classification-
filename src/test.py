import joblib
import pandas as pd
import os

# 1. Load mô hình
model_path = '../models/final_best_student_model.pkl'

if not os.path.exists(model_path):
    print(f"Không tìm thấy file tại: {model_path}")
else:
    pipeline = joblib.load(model_path)

    # 2. Tạo dữ liệu sinh viên mới
    # #1: SINH VIÊN CHĂM CHỈ (Kỳ vọng: PASS)
    # new_student = pd.DataFrame([{
    #     'age': 18,
    #     'gender': 'Female',
    #     'school_type': 'Private',
    #     'parent_education': "Master's Degree",
    #     'study_hours': 15.0,
    #     'attendance_percentage': 92.0,
    #     'internet_access': 'Yes',
    #     'travel_time': 'Short',
    #     'extra_activities': 'Yes',
    #     'study_method': 'Group',
    #     'math_score': 85.0,
    #     'science_score': 80.0,
    #     'english_score': 88.0
    # }])

    # 2: SINH VIÊN LƯỜI HỌC (Kỳ vọng: FAIL) - Như có thể uncomment để test
    new_student = pd.DataFrame([{
        'age': 18,
        'gender': 'male',
        'school_type': 'public',
        'parent_education': 'diploma',
        'study_hours': 15.0,
        'attendance_percentage': 37.0,
        'internet_access': 'yes',
        'travel_time': '<15 min',
        'extra_activities': 'yes',
        'study_method': 'notes',
        'math_score': 70.0,
        'science_score': 30.0,
        'english_score': 70.0
    }])

    # 3. FEATURE ENGINEERING
    new_student['Study_Attendance'] = new_student['study_hours'] * new_student['attendance_percentage']
    new_student['Academic_Avg'] = (new_student['math_score'] + new_student['science_score'] + new_student[
        'english_score']) / 3

    # 4. DỰ ĐOÁN
    try:
        # Pipeline sẽ tự động thực hiện: preprocessor -> predict
        prediction = pipeline.predict(new_student)
        probability = pipeline.predict_proba(new_student)

        print("\n" + "=" * 40)
        print("KẾT QUẢ DỰ ĐOÁN SINH VIÊN (Dữ liệu mới)")
        print("=" * 40)

        result = "PASS" if prediction[0] == 1 else "FAIL"

        print(f"Kết luận: {result}")
        print(f"Xác suất FAIL: {probability[0][0]:.2%}")
        print(f"Xác suất PASS: {probability[0][1]:.2%}")
        print("=" * 40)

    except Exception as e:
        print(f"Lỗi: Có thể thiếu cột hoặc tên cột sai. Chi tiết: {e}")