from rest_framework.decorators import api_view
from rest_framework.response import Response
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


@api_view(['POST'])
def predict_view(request):
    data = request.data

    att = float(data.get('AttendanceRate', 0))
    study = float(data.get('StudyHoursPerWeek', 0))
    prev = float(data.get('PreviousGrade', 0))
    act = int(float(data.get('ExtracurricularActivities', 0)))
    gender = data.get('Gender')
    support = data.get('ParentalSupport')

    online_input = data.get('Online Classes Taken')
    is_online = str(online_input).lower() == 'true'

    df = pd.DataFrame([{
        'AttendanceRate': att,
        'StudyHoursPerWeek': study,
        'PreviousGrade': prev,
        'ExtracurricularActivities': act,
        'Gender': gender,
        'ParentalSupport': support,
        'Online Classes Taken': is_online,
        'Study_Attendance_Score': float(study * att),
        'Study_per_Activity': float(study / (act + 1))
    }])

    cols = [
        'AttendanceRate', 'StudyHoursPerWeek', 'PreviousGrade',
        'ExtracurricularActivities', 'Gender', 'ParentalSupport',
        'Online Classes Taken', 'Study_Attendance_Score', 'Study_per_Activity'
    ]
    df = df[cols]

    prediction = model.predict(df)

    return Response({'result': prediction[0]})