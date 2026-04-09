from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
import numpy as np


# ===== VALID VALUE RANGES (based on training data) =====
VALID_RANGES = {
    'AttendanceRate':              (0, 100),
    'StudyHoursPerWeek':           (0, 168),
    'PreviousGrade':               (0, 100),
    'ExtracurricularActivities':   (0, 10),
}

VALID_CATEGORIES = {
    'Gender':          ['Male', 'Female'],
    'ParentalSupport': ['Low', 'Medium', 'High'],
}


PASS_THRESHOLD = 70


def validate_input(data: dict) -> list[str]:
    """
    Kiểm tra dữ liệu đầu vào trước khi predict.
    Trả về danh sách lỗi (rỗng = hợp lệ).
    """
    errors = []

    
    for field, (lo, hi) in VALID_RANGES.items():
        if field not in data:
            errors.append(f"Thiếu trường bắt buộc: '{field}'.")
            continue
        try:
            val = float(data[field])
        except (TypeError, ValueError):
            errors.append(f"'{field}' phải là số, nhận được: '{data[field]}'.")
            continue
        if not (lo <= val <= hi):
            errors.append(
                f"'{field}' phải nằm trong khoảng [{lo}, {hi}], nhận được: {val}."
            )

   
    for field, choices in VALID_CATEGORIES.items():
        if field not in data:
            errors.append(f"Thiếu trường bắt buộc: '{field}'.")
            continue
        val = str(data[field]).strip()
        if val not in choices:
            errors.append(
                f"'{field}' phải là một trong {choices}, nhận được: '{val}'."
            )

  
    if 'Online Classes Taken' not in data:
        errors.append("Thiếu trường bắt buộc: 'Online Classes Taken'.")
    else:
        val = str(data['Online Classes Taken']).strip().lower()
        if val not in ('true', 'false', '1', '0', 'yes', 'no'):
            errors.append(
                f"'Online Classes Taken' phải là true/false, nhận được: '{data['Online Classes Taken']}'."
            )

    return errors


def clean_data(df):
    df = df.copy()

    # ===== 1. DATA CLEANING =====
    df.drop(['StudentID', 'Name'], axis=1, inplace=True, errors='ignore')
    df.fillna(df.mean(numeric_only=True), inplace=True)
    df.fillna(df.mode().iloc[0], inplace=True)
    df.drop_duplicates(inplace=True)

    cols_check = ['AttendanceRate', 'StudyHoursPerWeek', 'PreviousGrade']
    for col in cols_check:
        if col in df.columns:
            df = df[df[col].between(0, 100)]

   
    df['AttendanceRate']            = df['AttendanceRate'].clip(0, 100)
    df['StudyHoursPerWeek']         = df['StudyHoursPerWeek'].clip(0, 168)
    df['PreviousGrade']             = df['PreviousGrade'].clip(0, 100)
    df['ExtracurricularActivities'] = df['ExtracurricularActivities'].clip(0, 10)

    df['Study_Attendance_Score'] = df['StudyHoursPerWeek'] * df['AttendanceRate']
    df['Study_per_Activity']     = df['StudyHoursPerWeek'] / (df['ExtracurricularActivities'] + 1)

    
    df['Pass'] = (df['FinalGrade'] >= PASS_THRESHOLD).astype(int)
    df.drop('FinalGrade', axis=1, inplace=True)

    return df


def get_preprocess(X_train):
    
    num_cols = X_train.select_dtypes(include=['int64', 'float64']).columns
    cat_cols = X_train.select_dtypes(include=['object', 'str', 'bool']).columns

    preprocessor = ColumnTransformer([
        ('num', StandardScaler(), num_cols),
        ('cat', OneHotEncoder(handle_unknown='ignore'), cat_cols)
    ])

    return preprocessor