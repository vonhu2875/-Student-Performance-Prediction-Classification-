from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from src.preprocessing import validate_input   
import joblib
import os
import pandas as pd

# 1. Load Model
current_folder = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_folder, 'models', 'best_model.pkl')

if os.path.exists(model_path):
    model = joblib.load(model_path)
else:
    print("Lỗi: Không tìm thấy file model!")


GRADE_MIN = 0.0
GRADE_MAX = 100.0


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

    # ── 3. Parse (an toàn vì đã validate ở trên) ────────────────────────────
    att    = float(data['AttendanceRate'])
    study  = float(data['StudyHoursPerWeek'])
    prev   = float(data['PreviousGrade'])
    act    = int(float(data['ExtracurricularActivities']))
    gender  = str(data['Gender']).strip()
    support = str(data['ParentalSupport']).strip()
    is_online = str(data['Online Classes Taken']).strip().lower() in ('true', '1', 'yes')

    # ── 4. Feature engineering (phải khớp với preprocessing.py) ─────────────
    raw_score             = study * att
    study_attendance_score = np.log1p(raw_score)        # log-scale như clean_data()
    study_per_activity    = study / (act + 1)

    df = pd.DataFrame([{
        'AttendanceRate':           att,
        'StudyHoursPerWeek':        study,
        'PreviousGrade':            prev,
        'ExtracurricularActivities': act,
        'Gender':                   gender,
        'ParentalSupport':          support,
        'Online Classes Taken':     is_online,
        'Study_Attendance_Score':   study_attendance_score,
        'Study_per_Activity':       study_per_activity,
    }])

    cols = [
        'AttendanceRate', 'StudyHoursPerWeek', 'PreviousGrade',
        'ExtracurricularActivities', 'Gender', 'ParentalSupport',
        'Online Classes Taken', 'Study_Attendance_Score', 'Study_per_Activity'
    ]
    df = df[cols]

    # ── 5. Predict + clamp kết quả về [0, 100] ───────────────────────────────
    prediction = model.predict(df)
    predicted_grade = float(prediction[0])
    predicted_grade = max(GRADE_MIN, min(GRADE_MAX, predicted_grade))  # clamp

    return Response({'result': round(predicted_grade, 2)})