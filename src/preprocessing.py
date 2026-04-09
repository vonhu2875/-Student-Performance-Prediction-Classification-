from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer

def preprocess_data(df):

    # Drop cột không cần
    df = df.drop(['StudentID', 'Name'], axis=1)

<<<<<<< HEAD
    # Tạo target
    df['pass'] = df['FinalGrade'].apply(lambda x: 1 if x >= 50 else 0)
=======
    # Không lọc FinalGrade ở đây vì là biến mục tiêu
    cols_check = ['AttendanceRate', 'StudyHoursPerWeek', 'PreviousGrade']

    for col in cols_check:
        if col in df.columns:
            df = df[df[col].between(0, 100)]
>>>>>>> 2ab2841dc8e81a0fd83c399fe1145670df571b44

    # Tách X, y
    X = df.drop(['FinalGrade', 'pass'], axis=1)
    y = df['pass']

    # Xử lý missing
    num_cols = X.select_dtypes(include=['float64', 'int64']).columns
    cat_cols = X.select_dtypes(include='object').columns

    imputer_num = SimpleImputer(strategy='mean')
    X[num_cols] = imputer_num.fit_transform(X[num_cols])

    imputer_cat = SimpleImputer(strategy='most_frequent')
    X[cat_cols] = imputer_cat.fit_transform(X[cat_cols])

    # Encode categorical
    le = LabelEncoder()
    for col in cat_cols:
        X[col] = le.fit_transform(X[col])

    # Train test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Scale
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    return X_train, X_test, y_train, y_test, scaler