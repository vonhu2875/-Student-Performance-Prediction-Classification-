from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC


def get_models():
    return {
        "Logistic Regression": LogisticRegression(
            max_iter=1000,
            class_weight='balanced',
            random_state=42
        ),

        "Random Forest": RandomForestClassifier(
            n_estimators=200,  # Tăng lên 200 cây để xử lý 20,000 dòng tốt hơn
            max_depth=15,  # Giới hạn độ sâu để tránh Overfitting
            random_state=42,
            class_weight='balanced',
            n_jobs=-1  # Tận dụng tối đa CPU để train nhanh hơn
        ),

        "SVM": SVC(
            probability=True,
            kernel='rbf',  # Dùng kernel rbf để bắt các mối quan hệ phi tuyến
            class_weight='balanced',
            random_state=42
        )
    }