from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import joblib
import os
import numpy as np
import pandas as pd

from src.preprocessing import validate_input

# ===== 1. Load Model =====
current_folder = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_folder, 'models', 'best_model.pkl')

if os.path.exists(model_path):
    model = joblib.load(model_path)
else:
    model = None
    print("Lỗi: Không tìm thấy file model!")


@api_view(['POST'])
def predict_view(request):
    # ── 1. Kiểm tra model đã load chưa ──────────────────────────────────────
    if model is None:
        return Response(
            {'error': 'Model chưa được load. Vui lòng liên hệ quản trị viên.'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )

    data = request.data

    # ── 2. Validate input ────────────────────────────────────────────────────
    errors = validate_input(data)
    if errors:
        return Response(
            {'error': 'Dữ liệu đầu vào không hợp lệ.', 'details': errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    # ── 3. Parse ─────────────────────────────────────────────────────────────
    att       = float(data['AttendanceRate'])
    study     = float(data['StudyHoursPerWeek'])
    prev      = float(data['PreviousGrade'])
    act       = int(float(data['ExtracurricularActivities']))
    gender    = str(data['Gender']).strip()
    support   = str(data['ParentalSupport']).strip()
    is_online = str(data['Online Classes Taken']).strip().lower() in ('true', '1', 'yes')

    # ── 4. Feature engineering (phải khớp với preprocessing.py) ─────────────
    df = pd.DataFrame([{
        'AttendanceRate':            att,
        'StudyHoursPerWeek':         study,
        'PreviousGrade':             prev,
        'ExtracurricularActivities': act,
        'Gender':                    gender,
        'ParentalSupport':           support,
        'Online Classes Taken':      is_online,
        'Study_Attendance_Score':    study * att,
        'Study_per_Activity':        study / (act + 1),
    }])

    cols = [
        'AttendanceRate', 'StudyHoursPerWeek', 'PreviousGrade',
        'ExtracurricularActivities', 'Gender', 'ParentalSupport',
        'Online Classes Taken', 'Study_Attendance_Score', 'Study_per_Activity'
    ]
    df = df[cols]

    # ── 5. Predict ───────────────────────────────────────────────────────────
    prediction  = model.predict(df)[0]           # 0 = Fail, 1 = Pass
    probability = model.predict_proba(df)[0]     # [prob_fail, prob_pass]

    result_label = 'Pass' if prediction == 1 else 'Fail'
    result_prob  = round(float(probability[prediction]), 4)  # xác suất của nhãn được chọn

    return Response({
        'result':      result_label,   # 'Pass' hoặc 'Fail'
        'probability': result_prob,    # xác suất từ 0.0 → 1.0
    })








