import os
import joblib
import pandas as pd
import numpy as np
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.preprocessing import validate_input


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, 'backend', 'models', 'best_model.pkl')

model = joblib.load(model_path)


# ============================================================
# HÀM HỖ TRỢ
# ============================================================

def make_prediction(att, study, prev, act, gender, support, online):
    data = pd.DataFrame([{
        'AttendanceRate':            att,
        'StudyHoursPerWeek':         study,
        'PreviousGrade':             prev,
        'ExtracurricularActivities': act,
        'Gender':                    gender,
        'ParentalSupport':           support,
        'Online Classes Taken':      online,
        'Study_Attendance_Score':    study * att,
        'Study_per_Activity':        study / (act + 1),
    }])
    prediction  = model.predict(data)[0]
    # Chuyển prediction thành probability bằng sigmoid
    prob_value = 1 / (1 + np.exp(-prediction))
    label = 'Pass' if prob_value >= 0.5 else 'Fail'
    prob  = round(float(prob_value), 4)
    return label, prob


def run_valid_test(label, **kwargs):
    print(f"  {label}")
    # Tạo dict đúng cho validate_input
    data = {
        'AttendanceRate': kwargs['att'],
        'StudyHoursPerWeek': kwargs['study'],
        'PreviousGrade': kwargs['prev'],
        'ExtracurricularActivities': kwargs['act'],
        'Gender': kwargs['gender'],
        'ParentalSupport': kwargs['support'],
        'Online Classes Taken': kwargs['online']
    }
    errors = validate_input(data)
    if errors:
        print(f"Validate thất bại: {errors}\n")
        return
    result, prob = make_prediction(**kwargs)
    print(f"Kết quả: {result} (xác suất: {prob*100:.1f}%)\n")


def run_invalid_test(label, data: dict):
    """Chạy test không hợp lệ — in danh sách lỗi."""
    print(f"  {label}")
    errors = validate_input(data)
    if errors:
        for e in errors:
            print(f" {e}")
        print()
    else:
        print("Lẽ ra phải báo lỗi nhưng không có lỗi nào!\n")


def section(title):
    print("=" * 50)
    print(f"  {title}")
    print("=" * 50)





run_valid_test(
    "Học sinh bình thường",
    att=80.0, study=20.0, prev=75.0,
    act=1, gender='Male', support='Medium', online=True
)

run_valid_test(
    "Học sinh xuất sắc",
    att=95.0, study=30.0, prev=90.0,
    act=3, gender='Female', support='High', online=True
)

run_valid_test(
    "Học sinh yếu",
    att=20.0, study=1.0, prev=10.0,
    act=0, gender='Male', support='Low', online=False
)