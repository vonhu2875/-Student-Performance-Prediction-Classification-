import sys
import os
import numpy as np
import pandas as pd
import joblib

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# ===== 1. Path Setup =====
current_folder = os.path.dirname(os.path.abspath(__file__))
project_root   = os.path.abspath(os.path.join(current_folder, '..', '..'))

if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.preprocessing import validate_input

# ===== 2. Load Model + Scaler =====
model_path  = os.path.join(project_root, 'notebooks', 'models', 'model.joblib')
scaler_path = os.path.join(project_root, 'notebooks', 'models', 'scaler.joblib')

model  = joblib.load(model_path)  if os.path.exists(model_path)  else None
scaler = joblib.load(scaler_path) if os.path.exists(scaler_path) else None

if model  is None: print("Lỗi: Không tìm thấy model!")
if scaler is None: print("Lỗi: Không tìm thấy scaler!")

# Mean của 'Study Hours' và 'Attendance (%)' từ training data
# (dùng để impute vì form không thu thập 2 cột này)
_feature_means = (
    dict(zip(scaler.feature_names_in_, scaler.mean_))
    if scaler is not None else {}
)
STUDY_HOURS_MEAN  = _feature_means.get('Study Hours',   2.40)
ATTENDANCE_PCT_MEAN = _feature_means.get('Attendance (%)', 77.46)

# ===== 3. Categorical Encoding =====
# Dựa theo thứ tự LabelEncoder (alphabetical) khi train:
#   Gender:        Female=0, Male=1
#   ParentalSupport: Low=0, Medium=1, High=2  (ordinal, thứ tự tự nhiên)
GENDER_MAP  = {'Female': 0, 'Male': 1}
SUPPORT_MAP = {'Low': 0, 'Medium': 1, 'High': 2}


@api_view(['POST'])
def predict_view(request):
    # ── 1. Kiểm tra model & scaler đã load chưa ──────────────────────────────
    if model is None or scaler is None:
        return Response(
            {'error': 'Model/Scaler chưa được load. Vui lòng liên hệ quản trị viên.'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )

    data = request.data

    # ── 2. Validate input ─────────────────────────────────────────────────────
    errors = validate_input(data)
    if errors:
        return Response(
            {'error': 'Dữ liệu đầu vào không hợp lệ.', 'details': errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    # ── 3. Parse ──────────────────────────────────────────────────────────────
    att     = float(data['AttendanceRate'])
    study   = float(data['StudyHoursPerWeek'])
    prev    = float(data['PreviousGrade'])
    act     = int(float(data['ExtracurricularActivities']))
    gender  = str(data['Gender']).strip()
    support = str(data['ParentalSupport']).strip()
    is_online = str(data['Online Classes Taken']).strip().lower() in ('true', '1', 'yes')

    # ── 4. Build DataFrame khớp scaler.feature_names_in_ ─────────────────────
    # ['Gender', 'AttendanceRate', 'StudyHoursPerWeek', 'PreviousGrade',
    #  'ExtracurricularActivities', 'ParentalSupport',
    #  'Study Hours', 'Attendance (%)', 'Online Classes Taken']
    #
    # 'Study Hours' và 'Attendance (%)' là cột riêng trong dataset gốc,
    # không có trong form → dùng mean training (sau scaling = 0, không ảnh hưởng).
    df = pd.DataFrame([{
        'Gender':                    GENDER_MAP.get(gender, 0),
        'AttendanceRate':            att,
        'StudyHoursPerWeek':         study,
        'PreviousGrade':             prev,
        'ExtracurricularActivities': act,
        'ParentalSupport':           SUPPORT_MAP.get(support, 1),
        'Study Hours':               STUDY_HOURS_MEAN,
        'Attendance (%)':            ATTENDANCE_PCT_MEAN,
        'Online Classes Taken':      int(is_online),
    }])

    # ── 5. Scale ──────────────────────────────────────────────────────────────
    X_scaled = scaler.transform(df)

    # ── 6. Predict ────────────────────────────────────────────────────────────
    prediction   = model.predict(X_scaled)[0]          # 0 = Fail, 1 = Pass
    result_label = 'Pass' if prediction == 1 else 'Fail'

    # Model được train với probability=False nên dùng decision_function + sigmoid
    decision    = float(model.decision_function(X_scaled)[0])
    raw_prob    = 1 / (1 + np.exp(-decision))          # sigmoid
    # Nếu predict Fail (0), xác suất Fail = 1 - raw_prob
    result_prob = round(raw_prob if prediction == 1 else 1 - raw_prob, 4)

    return Response({
        'result':      result_label,   # 'Pass' hoặc 'Fail'
        'probability': result_prob,    # xác suất của nhãn được chọn (0.0 → 1.0)
    })
