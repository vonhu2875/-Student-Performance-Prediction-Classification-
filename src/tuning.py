import sys
import os
import wandb
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, f1_score, accuracy_score, confusion_matrix

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline as SkPipeline
# --- 1. LOAD DATA VÀ TIỀN XỬ LÝ BAN ĐẦU ---
sys.path.append(os.path.abspath(".."))
from src.preprocessing import preprocess_data # Đảm bảo hàm này trả về preprocessor

# Đọc file dataset 10,000 dòng
df = pd.read_csv("../data/student_performance_v2.csv")
df.columns = df.columns.str.strip()

# Tạo cột result (Target)
if 'result' not in df.columns:
    df['result'] = df['final_grade'].apply(lambda x: 1 if str(x).strip().upper() in ['A', 'B', 'C', 'D'] else 0)

# Feature Engineering đồng bộ với Bước 3
df['Study_Attendance'] = df['study_hours'] * df['attendance_percentage']
df['Academic_Avg'] = (df['math_score'] + df['science_score'] + df['english_score']) / 3

# Tách X (dữ liệu thô) và y
drop_cols = ['student_id', 'first_name', 'last_name', 'final_grade', 'overall_score', 'school_name', 'result']
X = df.drop(columns=drop_cols, errors='ignore')
y = df['result']

# Chia tập Train/Test
X_train_raw, X_test_raw, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
# Chỉ lấy danh sách cột từ X (đã bỏ result)
num_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
cat_cols = X.select_dtypes(include=['object']).columns.tolist()

num_pipeline = SkPipeline([
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())
])

cat_pipeline = SkPipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(drop='first', handle_unknown='ignore', sparse_output=False))
])

preprocessor = ColumnTransformer([
    ('num', num_pipeline, num_cols),
    ('cat', cat_pipeline, cat_cols)
])

# --- 2. KHỞI TẠO WANDB ---
wandb.init(project="student-performance-v2", entity="vothibichnhu2875", name="Hyperparameter_Tuning_RF")

# --- 3. TẠO PIPELINE TRỌN GÓI (End-to-End Pipeline) ---
# Quy trình: Tiền xử lý -> SMOTE -> Model
pipeline = ImbPipeline([
    ('preprocessor', preprocessor),
    ('smote', SMOTE(random_state=42)),
    ('model', RandomForestClassifier(random_state=42, class_weight='balanced'))
])

# --- 4. THIẾT LẬP GRID SEARCH ---
# Tinh chỉnh các tham số quan trọng để tối ưu F1-Score
param_grid = {
    'model__n_estimators': [100, 200],
    'model__max_depth': [10, 20, None],
    'model__min_samples_leaf': [2, 4],
    'model__max_features': ['sqrt', 'log2']
}

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
grid_search = GridSearchCV(
    pipeline, param_grid, cv=cv, scoring='f1_macro', n_jobs=-1, verbose=1
)

# --- 5. HUẤN LUYỆN VÀ ĐÁNH GIÁ ---
print("Đang bắt đầu Tuning...")
grid_search.fit(X_train_raw, y_train)

# Lấy Pipeline tốt nhất sau khi Tuning
best_pipeline = grid_search.best_estimator_
y_pred = best_pipeline.predict(X_test_raw)

print("\n" + "="*30)
print("KẾT QUẢ SAU TINH CHỈNH")
print("="*30)
print(classification_report(y_test, y_pred))

# Tính toán Metrics
acc = accuracy_score(y_test, y_pred)
f1_macro = f1_score(y_test, y_pred, average='macro')
cm = confusion_matrix(y_test, y_pred)

# --- VẼ CONFUSION MATRIX ---
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='RdYlGn',
            xticklabels=['FAIL', 'PASS'], yticklabels=['FAIL', 'PASS'])
plt.title("Confusion Matrix - Best Model")
plt.xlabel("Dự đoán")
plt.ylabel("Thực tế")

# --- LOG KẾT QUẢ LÊN WANDB ---
wandb.log({
    "accuracy": acc,
    "f1_macro": f1_macro,
    "best_params": str(grid_search.best_params_),
    "confusion_matrix": wandb.Image(plt),
    "classification_report": wandb.Image(plt) # WandB hỗ trợ log ảnh báo cáo
})
plt.close()

# --- 6. LƯU MÔ HÌNH TRỌN GÓI ---
# Lưu file .pkl chứa cả preprocessor + smote + model
os.makedirs('../models', exist_ok=True)
joblib.dump(best_pipeline, "../models/final_best_student_model.pkl")

print(f"\nTham số tốt nhất: {grid_search.best_params_}")

wandb.finish()