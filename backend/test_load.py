import os
import joblib
import pandas as pd


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, 'backend', 'models', 'best_model.pkl')

model = joblib.load(model_path)


# df['Study_Attendance_Score'] = df['StudyHoursPerWeek'] * df['AttendanceRate']
#     df['Study_per_Activity'] = df['StudyHoursPerWeek'] / (df['ExtracurricularActivities'] + 1)
data = pd.DataFrame([{
    'AttendanceRate': 80.0,
    'StudyHoursPerWeek': 20.0,
    'PreviousGrade': 75.0,
    'ExtracurricularActivities': 1,
    'Gender': 'Male',
    'ParentalSupport': 'Medium',
    'Online Classes Taken': True,
    'Study_Attendance_Score': 20.0*80.0,
    'Study_per_Activity': (20.0/(1+1))*1.0
}])


result = model.predict(data)

print("Kết quả:", result)