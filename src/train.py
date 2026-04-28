import sys
import os
import wandb
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# Thêm đường dẫn để import từ folder src
sys.path.append(os.path.abspath(".."))

# Import các hàm chúng ta đã viết ở Bước 3 và file model.py
from src.preprocessing import preprocess_data
from model import get_models

# 1. ĐỌC VÀ TIỀN XỬ LÝ DỮ LIỆU
df = pd.read_csv("../data/student_performance_v2.csv")

# Lấy dữ liệu đã xử lý từ Bước 3
X_train, X_test, y_train, y_test, preprocessor = preprocess_data(df)

# 2. LẤY DANH SÁCH MÔ HÌNH
models_dict = get_models()

# 3. VÒNG LẶP HUẤN LUYỆN
for name, model in models_dict.items():
    print(f"\n--- Đang huấn luyện: {name} ---")

    # Khởi tạo Run trên WandB
    run = wandb.init(
        project="student-performance-v2",
        name=f"Run_{name}",
        config={
            "model_type": name,
            "dataset_size": len(df),
            "features": "Academic_Avg + Study_Attendance"
        }
    )

    # Huấn luyện mô hình
    model.fit(X_train, y_train)

    # Dự đoán
    y_pred = model.predict(X_test)

    # Tính toán các Metrics (Dùng 'binary' vì pass/fail là 0,1)
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    # Log kết quả lên WandB
    wandb.log({
        "accuracy": acc,
        "precision": prec,
        "recall": rec,
        "f1_score": f1
    })

    # Vẽ và log Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Purples',
                xticklabels=['FAIL', 'PASS'], yticklabels=['FAIL', 'PASS'])
    plt.title(f'Confusion Matrix: {name}')
    plt.ylabel('Thực tế')
    plt.xlabel('Dự đoán')

    # Gửi ảnh lên WandB
    wandb.log({f"confusion_matrix_{name}": wandb.Image(fig)})
    plt.close(fig)

    print(f"Hoàn thành {name}: Accuracy={acc:.4f}, F1={f1:.4f}")

    # Kết thúc Run hiện tại trên WandB
    wandb.finish()