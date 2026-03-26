import os
import joblib
import pandas as pd


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, 'backend', 'models', 'best_model.pkl')

model = joblib.load(model_path)


data = pd.DataFrame([{
    'Gender': 'Male',
    'AttendanceRate': 90,
    'StudyHoursPerWeek': 20,
    'PreviousGrade': 75,
    'ExtracurricularActivities': 2,
    'ParentalSupport': 'Medium',
    'Online Classes Taken': True,
    'Study_Attendance_Score': 1800,
    'Study_per_Activity': 10
}])


result = model.predict(data)

print("Kết quả:", result)