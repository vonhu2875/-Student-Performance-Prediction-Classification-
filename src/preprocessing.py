import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

def preprocess_data(df):
    # 1. Feature Engineering
    df['Study_Attendance'] = df['StudyHoursPerWeek'] * df['AttendanceRate']
    df['Study_Efficiency'] = df['FinalGrade'] / (df['StudyHoursPerWeek'] + 1)

    # 2. Tạo Target
    df['pass'] = df['FinalGrade'].apply(lambda x: 1 if x >= 50 else 0)

    # 3. LOẠI CỘT (CỰC KỲ QUAN TRỌNG: Phải bỏ FinalGrade để không bị lộ đáp án)
    # Theo bài C5.04, tránh Data Leakage
    drop_cols = ['StudentID', 'Name', 'FinalGrade']
    df = df.drop(columns=drop_cols, errors='ignore')

    # 4. Tách X, y
    X = df.drop('pass', axis=1)
    y = df['pass']

    # 5. Chia Train/Test (Dùng Stratify theo bài C5.03 cho dữ liệu lệch)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # 6. Xác định loại cột
    num_cols = X_train.select_dtypes(include=[np.number]).columns
    cat_cols = X_train.select_dtypes(include=['object']).columns

    # 7. Pipeline xử lý (Theo bài C5.04)
    num_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='mean')),
        ('scaler', StandardScaler())
    ])

    cat_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(drop='first', handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer([
        ('num', num_pipeline, num_cols),
        ('cat', cat_pipeline, cat_cols)
    ])

    # Transform dữ liệu
    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)

    return X_train_processed, X_test_processed, y_train, y_test, preprocessor