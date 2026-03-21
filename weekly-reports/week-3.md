# Báo cáo Tuần 3

**Tuần:** 3 (16/03/2026 - 22/03/2026)   

**Nhóm:**    16

**Đề tài:** Đề tài 9 - Student Performance Prediction (Classification)

**Nhóm trưởng:** Võ Thị Bích Như - 2351050127
---
## 1. Công việc đã hoàn thành 

| Thành viên | MSSV | Công việc | Link Commit/PR | 
|------------|------|-----------|----------------| 
| Võ Thị Bích Như | 2351050127  | Xây dựng hệ thống Local logging (so sánh loss/accuracy), thực hiện Tuning (Grid Search) tìm alpha tối ưu cho mô hình baseline. | [Link commit](https://github.com/vonhu2875/-Student-Performance-Prediction-Classification-/commit/8c0ae9c2c9d10dbad3694efad4cfd25faf4bf969) |
| Nguyễn Diệp Thái Hà | 2351050037 | Xây dựng Pipeline huấn luyện cho 7 mô hình (Ridge, RF, SVM...), thực hiện Cross-Validation | [Link commit](https://github.com/vonhu2875/-Student-Performance-Prediction-Classification-/commit/0fd0b671d2405c0e87ed995d06b98b84fedda282) |
| Nguyễn Đức Nhu Toàn | 2351050183  | Hoàn thiện hàm preprocess_data: cleaning, feature engineering, và pipeline scaling/encoding. | [Link commit](https://github.com/vonhu2875/-Student-Performance-Prediction-Classification-/commit/b5bb874d94733b478dd452d10963a30f6d9f5799) |
---
## 2. Tiến độ tổng thể
| Hạng mục | Trạng thái | % | 
|----------|------------|---| 
| EDA | Đã hoàn thành  | 100% | 
| Preprocessing + Pipeline |  Đã hoàn thành | 100% | 
| Modeling (≥3 models, wandb) |  Đã hoàn thành | 100% | 
| Model Persistence | Đang làm | 50% | 
| Frontend (ReactJS) | Chưa làm | 0% | 
| Backend (API) | Chưa làm | 0% | 
| Demo FE ↔ BE ↔ AI | Chưa làm | 0% | 
| Báo cáo | Chưa làm | 0% | 

**Tổng tiến độ: 40%**
---
## 3. Kế hoạch tuần tới

| Thành viên | Công việc dự kiến |
| --- | --- |
| **Võ Thị Bích Như** | Thiết kế giao diện demo (frontend) và viết hướng dẫn sử dụng hệ thống. |
| **Nguyễn Đức Nhu Toàn** | Xây dựng API (Backend) để kết nối mô hình .pkl với giao diện. |
| **Nguyễn Diệp Thái Hà** | Kiểm thử mô hình trên dữ liệu thực tế mới và hoàn thiện tài liệu kỹ thuật cuối cùng. |
---
## 4. Khó khăn / Cần hỗ trợ
- Kỹ thuật: Gặp sự cố kết nối API WandB do hạ tầng mạng, nhóm đã chuyển sang dùng hệ thống Local Logging để lưu trữ thông số huấn luyện.
- Dữ liệu: Chỉ số R^2 hiện tại chưa cao(có giá trị âm) do đặc thù dữ liệu nhiễu, nhóm sẽ tập trung cải thiện thêm ở bước Feature Engineering trong các lần lặp tiếp theo.
---
*Ngày nộp: 21/03/2026*   
*Xác nhận của Nhóm trưởng: Võ Thị Bích Như*
