import joblib
import pandas as pd
import os

# 1. Load mô hình trọn gói (Pipeline)
model_path = '../models/final_best_student_model.pkl'
if not os.path.exists(model_path):
    print("Không tìm thấy file model! Như hãy chạy lại file tuning.py trước nhé.")
else:
    model = joblib.load(model_path)

    # 2. Tạo dữ liệu sinh viên mới
    #Dữ liệu học sinh giỏi - pass
    new_student = pd.DataFrame([{
            'Gender': 'Male',  # Male/Female tùy dữ liệu
            'AttendanceRate': 95.0,  # Điểm danh rất cao
            'StudyHoursPerWeek': 20.0,  # Học 20 tiếng/tuần
            'PreviousGrade': 85.0,  # Điểm cũ giỏi
            'ExtracurricularActivities': 1.0,
            'ParentalSupport': 'High',  # Hỗ trợ từ gia đình tốt
            'Online Classes Taken': True,
            'Study Hours': 20.0,
            'Attendance (%)': 95.0
        }])
    # Dữ liệu học sinh dở - fail
    # new_student = pd.DataFrame([{
    #     'Gender': 'Male',
    #     'AttendanceRate': 5.0,  # Cực thấp
    #     'StudyHoursPerWeek': 0.5,  # Gần như không học
    #     'PreviousGrade': 5.0,  # Điểm cũ lẹt đẹt
    #     'ExtracurricularActivities': 0.0,
    #     'ParentalSupport': 'Low',
    #     'Online Classes Taken': False,
    #     'Study Hours': 0.5,
    #     'Attendance (%)': 5.0
    # }])
    # 3. Tạo các cột tính toán (Feature Engineering) - BẮT BUỘC phải có
    new_student['Study_Attendance'] = new_student['StudyHoursPerWeek'] * new_student['AttendanceRate']
    new_student['Study_Efficiency'] = 0.2

    # --- BƯỚC QUAN TRỌNG: Đảm bảo thứ tự cột phải khớp hoàn toàn với lúc Train ---
    # Lấy danh sách cột mà Pipeline yêu cầu
    feature_names = model.feature_names_in_
    new_student = new_student[feature_names]

    # 4. Dự đoán
    try:
        prediction = model.predict(new_student)
        probability = model.predict_proba(new_student)

        print("\n" + "=" * 35)
        print("KẾT QUẢ DỰ ĐOÁN SINH VIÊN")
        print("=" * 35)
        result = "PASS (ĐẬU)" if prediction[0] == 1 else "❄️ FAIL (RỚT)"
        print(f"Kết luận: {result}")
        print(f"Chi tiết: FAIL ({probability[0][0]:.2%}) | PASS ({probability[0][1]:.2%})")
        print("=" * 35)

    except Exception as e:
        print(f"Lỗi dự đoán: {e}")