import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

def preprocess_data(df):
    # 1. FEATURE ENGINEERING
    # Tạo biến tương tác giữa giờ học và chuyên cần
    df['Study_Attendance'] = df['study_hours'] * df['attendance_percentage']

    # Tạo biến điểm trung bình các môn học (Academic Background)
    df['Academic_Avg'] = (df['math_score'] + df['science_score'] + df['english_score']) / 3

    # 2. TẠO TARGET (Biến mục tiêu)
    # Quy đổi điểm chữ sang nhị phân (A,B,C,D = 1; E,F = 0)
    df['result'] = df['final_grade'].apply(lambda x: 1 if str(x).strip().upper() in ['A', 'B', 'C', 'D'] else 0)

    # 3. LOẠI BỎ CÁC CỘT GÂY RÒ RỈ DỮ LIỆU (DATA LEAKAGE)
    # Phải bỏ 'final_grade' và 'overall_score' vì chúng chứa kết quả trực tiếp
    drop_cols = [
        'student_id', 'first_name', 'last_name',
        'final_grade', 'overall_score', 'school_name'
    ]
    df = df.drop(columns=drop_cols, errors='ignore')

    # 4. TÁCH X VÀ Y
    X = df.drop('result', axis=1)
    y = df['result']

    # 5. CHIA DỮ LIỆU TRAIN/TEST
    # Sử dụng stratify=y để đảm bảo tỉ lệ pass/fail đồng nhất ở cả 2 tập
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # 6. XÁC ĐỊNH DANH SÁCH CỘT SỐ VÀ CỘT CHỮ
    num_cols = X_train.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = X_train.select_dtypes(include=['object']).columns.tolist()

    print(f"--- Đã xác định Features ---")
    print(f"Cột số ({len(num_cols)}): {num_cols}")
    print(f"Cột chữ ({len(cat_cols)}): {cat_cols}")

    # 7. XÂY DỰNG PIPELINE XỬ LÝ (Theo chuẩn ColumnTransformer)
    # Xử lý cột số: Điền giá trị thiếu bằng Mean + Chuẩn hóa dữ liệu
    num_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='mean')),
        ('scaler', StandardScaler())
    ])

    # Xử lý cột chữ: Điền giá trị thiếu bằng Mode + Mã hóa One-Hot
    cat_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(drop='first', handle_unknown='ignore', sparse_output=False))
    ])

    # Gom các Pipeline vào bộ điều phối ColumnTransformer
    preprocessor = ColumnTransformer([
        ('num', num_pipeline, num_cols),
        ('cat', cat_pipeline, cat_cols)
    ])

    # 8. THỰC THI BIẾN ĐỔI (Fit trên Train và Transform trên cả hai)
    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)

    # Chuyển đổi ngược lại thành DataFrame để dễ kiểm soát tên cột
    feature_names = preprocessor.get_feature_names_out()
    X_train_final = pd.DataFrame(X_train_processed, columns=feature_names)
    X_test_final = pd.DataFrame(X_test_processed, columns=feature_names)

    print("\n--- Tiền xử lý hoàn tất ---")
    print(f"Hình dạng X_train sau xử lý: {X_train_final.shape}")

    return X_train_final, X_test_final, y_train, y_test, preprocessor