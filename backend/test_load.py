import os
import joblib
import pandas as pd
import numpy as np
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.preprocessing import validate_input


BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(BASE_DIR, '..'))

model_path  = os.path.join(project_root, 'notebooks', 'models', 'model.joblib')
scaler_path = os.path.join(project_root, 'notebooks', 'models', 'scaler.joblib')

model  = joblib.load(model_path)
scaler = joblib.load(scaler_path)

# Mean imputation cho 2 cột không có trong form
_means              = dict(zip(scaler.feature_names_in_, scaler.mean_))
STUDY_HOURS_MEAN    = _means['Study Hours']
ATTENDANCE_PCT_MEAN = _means['Attendance (%)']

GENDER_MAP  = {'Female': 0, 'Male': 1}
SUPPORT_MAP = {'Low': 0, 'Medium': 1, 'High': 2}


def make_prediction(att, study, prev, act, gender, support, online):
    df = pd.DataFrame([{
        'Gender':                    GENDER_MAP.get(gender, 0),
        'AttendanceRate':            att,
        'StudyHoursPerWeek':         study,
        'PreviousGrade':             prev,
        'ExtracurricularActivities': act,
        'ParentalSupport':           SUPPORT_MAP.get(support, 1),
        'Study Hours':               STUDY_HOURS_MEAN,
        'Attendance (%)':            ATTENDANCE_PCT_MEAN,
        'Online Classes Taken':      int(online),
    }])
    X_scaled   = scaler.transform(df)
    prediction = model.predict(X_scaled)[0]
    label      = 'Pass' if prediction == 1 else 'Fail'
    # SVM probability=False → dùng decision_function + sigmoid
    decision   = float(model.decision_function(X_scaled)[0])
    raw_prob   = 1 / (1 + np.exp(-decision))
    prob       = round(raw_prob if prediction == 1 else 1 - raw_prob, 4)
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