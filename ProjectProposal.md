# Đề xuất đề tài Bài Tập Lớn - Trí tuệ nhân tạo 
## 1. Thông tin nhóm
- **Nhóm**: 16
- **Thành viên**:
  
  2351050127 - Võ Thị Bích Như
  
  2351050037 - Nguyễn Diệp Thái Hà
  
  2351050183 - Nguyễn Đức Nhu Toàn
  
- **GVHD**: ThS.Võ Việt Khoa

## 2. Đề tài chọn
- **Đề tài số:** 9
- **Tên:** Student Performance Prediction
- **Loại bài toán:** Classification
- **Dataset:** [Student Performance (Kaggle Source)](https://www.kaggle.com/code/samanyuk/student-performance)
## 3. Mục tiêu
- Mục tiêu của đề tài là xây dựng mô hình học máy phân loại (Classification) để dự đoán kết quả học tập của sinh viên (Pass/Fail) dựa trên các yếu tố như thời gian học, môi trường gia đình và lịch sử học tập. Thông qua quá trình phân tích khám phá (EDA), đề tài sẽ rút ra các insight về những yếu tố ảnh hưởng mạnh nhất đến điểm số. Từ đó, cung cấp cơ sở để nhà trường đưa ra các biện pháp cảnh báo và can thiệp hỗ trợ học tập sớm. 
## 4. Công nghệ dự kiến
- **ML**: Python, Scikit-learn, Pandas, Jupyter Notebook, wandb (Tracking).
- **Frontend**: ReactJS
- **Backend**: Django (Sử dụng Django REST Framework để làm API).
- **DB:** MySQL (Sử dụng MySQL Workbench) hoặc SQLite (Tùy thuộc vào yêu cầu triển khai thực tế).
## 5. Phân công công việc 
| Thành viên | Công việc chính | Timeline |
|---------------|-----------------|--------| 
|Võ Thị Bích Như|- Quản lý dự án (PM), lập kế hoạch và viết báo cáo tuần.<br>- Thiết kế Database (MySQL/SQLite), xây dựng API Backend (Flask).<br>- Tích hợp Model AI vào hệ thống, thực hiện load model (.joblib).|Tuần 1 - 10| 
|Nguyễn Đức Nhu Toàn| - Phân tích dữ liệu (EDA), tiền xử lý (Preprocessing).<br>- Huấn luyện và so sánh ≥3 Model ML, tối ưu và tracking trên wandb.<br>- Hỗ trợ thiết kế logic Database và cấu trúc API Backend.|Tuần 1 - 10| 
|Nguyễn Diệp Thái Hà| - Thiết kế giao diện (UI/UX), phát triển Frontend (ReactJS).<br>- Kiểm thử hệ thống (QA), chụp ảnh/quay video demo.|Tuần 1 - 10| 
## 6. Timeline
- Tuần 1–2: Khởi động, EDA
- Tuần 3–4: Preprocessing, Modeling
- Tuần 5–6: Model + Persistence, wandb
- Tuần 7–8: FE + BE, Demo, Báo cáo
- Tuần 9–10: Nộp bài, Bảo vệ 
