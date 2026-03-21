from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer


def preprocess_data(df, test_size=0.2, random_state=42):
    df = df.copy()
    # ===== 1. DATA CLEANING =====
    df.drop(['StudentID', 'Name'], axis=1, inplace=True, errors='ignore')
    df.fillna(df.mean(numeric_only=True), inplace=True)
    df.fillna(df.mode().iloc[0], inplace=True)
    df.drop_duplicates(inplace=True)
    df.drop(['Attendance (%)', 'Study Hours'], axis=1, inplace=True, errors='ignore')

    cols_0_100 = ['AttendanceRate', 'PreviousGrade', 'FinalGrade']
    df = df[(df[cols_0_100].ge(0).all(axis=1)) &
            (df[cols_0_100].le(100).all(axis=1))]
    df = df[df['StudyHoursPerWeek'] >= 0]

    # ===== 2. FEATURE ENGINEERING =====
    df['Study_Attendance_Score'] = df['StudyHoursPerWeek'] * df['AttendanceRate']
    df['Study_per_Activity'] = df['StudyHoursPerWeek'] / (df['ExtracurricularActivities'] + 1)

    # ===== 3. SPLIT =====
    X = df.drop('FinalGrade', axis=1)
    y = df['FinalGrade']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    # ===== 4. ENCODING + SCALING =====
    num_cols = X_train.select_dtypes(include=['int64', 'float64']).columns
    cat_cols = X_train.select_dtypes(include=['object', 'str', 'bool']).columns

    preprocessor = ColumnTransformer([
        ('num', StandardScaler(), num_cols),
        ('cat', OneHotEncoder(handle_unknown='ignore'), cat_cols)
    ])

    return X_train, X_test, y_train, y_test, preprocessor


