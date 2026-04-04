from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

def get_models():
    return {
        "Logistic": LogisticRegression(),
        "RandomForest": RandomForestClassifier(),
        "SVM": SVC()
    }