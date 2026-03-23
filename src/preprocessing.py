from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer


def clean_data(df):
    df = df.copy()
    # ===== 1. DATA CLEANING =====
    df.drop(['StudentID', 'Name'], axis=1, inplace=True, errors='ignore')
    df.fillna(df.mean(numeric_only=True), inplace=True)
    df.fillna(df.mode().iloc[0], inplace=True)
    df.drop_duplicates(inplace=True)

    # Không lọc FinalGrade ở đây vì là biến mục tiêu
    cols_check = ['AttendanceRate', 'PreviousGrade']
    for col in cols_check:
        if col in df.columns:
            df = df[(df[col] >= 0) & (df[col] <= 100)]

    # ===== 2. FEATURE ENGINEERING =====
    df['Study_Attendance_Score'] = df['StudyHoursPerWeek'] * df['AttendanceRate']
    df['Study_per_Activity'] = df['StudyHoursPerWeek'] / (df['ExtracurricularActivities'] + 1)

    return df

def get_preprocess(X_train):
    # ===== 3. ENCODING + SCALING =====
    num_cols = X_train.select_dtypes(include=['int64', 'float64']).columns
    cat_cols = X_train.select_dtypes(include=['object', 'str', 'bool']).columns

    preprocessor = ColumnTransformer([
        ('num', StandardScaler(), num_cols),
        ('cat', OneHotEncoder(handle_unknown='ignore'), cat_cols)
    ])

    return preprocessor


