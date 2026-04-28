# FINAL PROJECT ARTIFICIAL INTELLIGENCE - ĐỀ TÀI 9 - STUDENT PERFORMANCE PREDICTION (CLASSIFICATION)
## Mô tả 

Dự án tập trung vào việc xây dựng mô hình Học máy (Machine Learning) để dự đoán kết quả học tập của sinh viên (Đạt/Không đạt) dựa trên các yếu tố như: thời gian học tập, tỉ lệ chuyên cần, điểm số các môn thành phần và nền tảng gia đình.

Dataset: Bộ dữ liệu bao gồm 20,000 bản ghi với các thuộc tính đa dạng (nhân khẩu học, hành vi học tập).

Mục tiêu: Giúp cơ sở giáo dục nhận diện sớm các sinh viên có nguy cơ rớt môn để đưa ra các biện pháp hỗ trợ kịp thời.
## Thành viên nhóm 
| MSSV | Họ tên | Vai trò | 
|------|--------|---------| 
|2351050127|Võ Thị Bích Như | ML / Notebook	Thực hiện EDA, Preprocessing, Feature Engineering, huấn luyện ≥3 models, Tuning, Evaluation và tích hợp WandB. |
| 2351050037 | Nguyễn Diệp Thái Hà | Frontend (ReactJS)	Thiết kế UI, phát triển giao diện ReactJS, tích hợp API, xây dựng form nhập và hiển thị kết quả dự đoán. | 
| 2351050183 | Nguyễn Đức Nhu Toàn | Backend (API)	Thiết kế API, phát triển Backend (Flask), load model, tạo endpoint predict và quản lý Database. | 
## Công nghệ
- Machine Learning: Python, Scikit-learn, Pandas, Numpy, Imbalanced-learn (SMOTE).

- Experiment Tracking: Weights & Biases (WandB) để quản lý các phiên huấn luyện.

- Frontend: ReactJS + Tailwind CSS / Bootstrap.

- Backend: Flask + Joblib (để load model .pkl).

- Notebook: Jupyter Notebook để phân tích dữ liệu (EDA).
## Cài đặt và chạy 
### Yêu cầu
- Python 3.9+
- Node.js & npm (cho Frontend)
- Tài khoản WandB (để xem log)
### Chạy Notebook 
jupyter notebook notebooks/student_performance_p2.ipynb 
### Chạy Backend 
pip install -r requirements.txt && cd backend python app.py 
### Chạy Frontend 
cd frontend && npm install && npm start 
### Truy cập
- Frontend: http://localhost:3000
- API: http://localhost:8000
## Demo
- wandb: [[link]](https://wandb.ai/vothibichnhu2875/student-performance-v2)
- Screenshot/video: Nằm trong thư mục screenshots/ 
## Nộp bài
- Báo cáo: report/report.pdf 