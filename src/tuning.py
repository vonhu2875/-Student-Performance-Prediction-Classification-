import sys
import os
import wandb
import pandas as pd
import joblib
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, f1_score, accuracy_score, confusion_matrix

# --- 1. LOAD DATA VÀ TỰ TẠO CỘT MỤC TIÊU ---
sys.path.append(os.path.abspath(".."))
from src.preprocessing import preprocess_data

# Đọc file gốc
df = pd.read_csv("../data/student_performance.csv")
df.columns = df.columns.str.strip()

# Tạo cột pass nếu chưa có (Dành cho Classification)
if 'pass' not in df.columns:
    df['pass'] = (df['FinalGrade'] >= 10).astype(int)

# Tạo các cột Feature Engineering để khớp với Preprocessor ở Bước 3
df['Study_Attendance'] = df['StudyHoursPerWeek'] * df['AttendanceRate']
df['Study_Efficiency'] = 0.8

target_col = 'pass'
df = df.dropna(subset=[target_col])

# Tách X (dữ liệu thô) và y
X = df.drop(columns=['StudentID', 'Name', 'FinalGrade', 'pass'], errors='ignore')
y = df[target_col]

# Chia tập Train/Test (Giữ nguyên tỉ lệ đậu rớt bằng stratify)
X_train_raw, X_test_raw, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Lấy bộ tiền xử lý từ src
_, _, _, _, preprocessor = preprocess_data(df)

# --- 2. KHỞI TẠO WANDB ---
wandb.init(project="student-performance-btl", name="Final_Tuning_Balanced")

# --- 3. TẠO PIPELINE TRỌN GÓI ---
pipeline = ImbPipeline([
    ('preprocessor', preprocessor),
    ('smote', SMOTE(random_state=42)),
    ('model', RandomForestClassifier(random_state=42, class_weight='balanced'))
])

# --- 4. THIẾT LẬP GRID SEARCH ---
# Giảm max_depth xuống để tránh máy chỉ học vẹt lớp Đậu
param_grid = {
    'model__n_estimators': [100, 200],
    'model__max_depth': [5, 10, None],
    'model__min_samples_leaf': [2, 4],
    'model__max_features': ['sqrt', 'log2']
}

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
grid_search = GridSearchCV(
    pipeline, param_grid, cv=cv, scoring='f1_macro', n_jobs=-1, verbose=1
)

# --- 5. HUẤN LUYỆN VÀ ĐÁNH GIÁ ---
print("Đang Tuning để cứu lớp FAIL, vui lòng đợi...")
grid_search.fit(X_train_raw, y_train)

best_pipeline = grid_search.best_estimator_
y_pred = best_pipeline.predict(X_test_raw)

print("\n--- BÁO CÁO KẾT QUẢ CUỐI CÙNG ---")
print(classification_report(y_test, y_pred))

# --- METRICS ---
acc = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred, average='macro')
cm = confusion_matrix(y_test, y_pred)

print("Accuracy:", acc)
print("F1-macro:", f1)
print("Confusion Matrix:\n", cm)

# --- VẼ CONFUSION MATRIX ---
import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(6,4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")

# --- LOG WANDB ---
wandb.log({
    "accuracy": acc,
    "f1_macro": f1,
    "best_params": str(grid_search.best_params_),
    "confusion_matrix": wandb.Image(plt),
    "classification_report": classification_report(y_test, y_pred)
})

plt.close()

# --- 6. LƯU MÔ HÌNH ---
os.makedirs('../models', exist_ok=True)
joblib.dump(best_pipeline, "../models/final_best_student_model.pkl")

print("\nXONG! File models/final_best_student_model.pkl")

wandb.finish()