import sys
import os
import wandb
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

sys.path.append(os.path.abspath(".."))

from src.preprocessing import preprocess_data  # Import hàm từ Bước 3
from model import get_models  # Import danh sách model

# 1. ĐỌC VÀ TIỀN XỬ LÝ DỮ LIỆU
df = pd.read_csv("../data/student_performance.csv")
X_train, X_test, y_train, y_test, preprocessor = preprocess_data(df)

# 2. LẤY DANH SÁCH MÔ HÌNH
models_dict = get_models()

# 3. VÒNG LẶP HUẤN LUYỆN 3 MÔ HÌNH (3 RUNS)
for name, model in models_dict.items():
    print(f"\n--- Đang huấn luyện: {name} ---")

    # Khởi tạo Run trên WandB (Bài C5.04)
    run = wandb.init(
        project="student-performance-btl",
        name=f"Baseline_{name}",
        config={
            "model_type": name,
            "class_weight": "balanced",
            "features_used": "Enhanced (with Study Efficiency)"
        }
    )

    # Huấn luyện mô hình
    model.fit(X_train, y_train)

    # Dự đoán
    y_pred = model.predict(X_test)

    # Tính toán các Metrics
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average='macro')
    rec = recall_score(y_test, y_pred, average='macro')
    f1 = f1_score(y_test, y_pred, average='macro')

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
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=['FAIL', 'PASS'], yticklabels=['FAIL', 'PASS'])
    plt.title(f'Confusion Matrix: {name}')
    plt.ylabel('Thực tế')
    plt.xlabel('Dự đoán')

    # Gửi ảnh lên WandB
    wandb.log({f"cm_{name}": wandb.Image(fig)})
    plt.close(fig)

    print(f"Hoàn thành {name}: Accuracy={acc:.2f}, F1={f1:.2f}")

    # Kết thúc Run hiện tại
    wandb.finish()

print("\nĐã hoàn thành 3 runs. Bạn hãy lên WandB để so sánh kết quả nhé!")