import { useState } from 'react'
import './App.css'

function App() {
  // 1. Nơi lưu trữ dữ liệu người dùng nhập
  const [formData, setFormData] = useState({
    AttendanceRate: '',
    StudyHoursPerWeek: '',
    PreviousGrade: '',
    ExtracurricularActivities: '' // 1 là có, 0 là không
  });



  // 2. Hàm xử lý khi gõ vào ô nhập
  const handleChange = (e) => {
    const { name, value } = e.target;

    // Ràng buộc: Chỉ cho phép nhập số hoặc để trống
    if (!isNaN(value) || value === '') {
      setFormData({
        ...formData,
        [name]: value
      });
    }
  };

  return (
    <div className="container">
      <h1>Dự Đoán Kết Quả Học Tập</h1>

      <form className="predict-form">
        <div className="input-group">
          <label>Tỷ lệ chuyên cần (%):</label>
          <input
            type="text"
            name="AttendanceRate"
            value={formData.AttendanceRate}
            onChange={handleChange}
            placeholder="Ví dụ: 95"
          />
        </div>

        <div className="input-group">
          <label>Giờ học mỗi tuần:</label>
          <input
            type="text"
            name="StudyHoursPerWeek"
            value={formData.StudyHoursPerWeek}
            onChange={handleChange}
            placeholder="Ví dụ: 20"
          />
        </div>

        <div className="input-group">
          <label>Điểm số kỳ trước:</label>
          <input
            type="text"
            name="PreviousGrade"
            value={formData.PreviousGrade}
            onChange={handleChange}
            placeholder="Ví dụ: 85"
          />
        </div>

        <button type="button" className="btn-predict">
          Dự Đoán Ngay
        </button>
      </form>

      <div className="result-section">
        <h3>Kết quả dự đoán: --</h3>
      </div>
    </div>
  )
}

export default App