import React from 'react';
import { User, Send, BookOpen, BarChart3 } from 'lucide-react';
const PredictionForm = ({ formData, handleChange, handleSubmit, loading }) => {
  return (
    <form onSubmit={handleSubmit} className=" shadow-sm bg-white rounded">
      {/* PHẦN 1: THÔNG TIN CÁ NHÂN */}
      <div className="mb-4">
        <h5 className="text-primary border-bottom pb-2 mb-3">
          <User className="me-2" size={20} /> Thông tin cá nhân
        </h5>
        <div className="row g-3 p-3">
          <div className="col-md-6">
            <label className="form-label fw-bold">Họ và tên</label>
            <input type="text" name="name" className="form-control" placeholder="Nguyễn Văn A" onChange={handleChange} required />
          </div>
          <div className="col-md-3">
            <label className="form-label fw-bold">Tuổi</label>
            <input type="number" name="age" className="form-control" defaultValue="18" min="14" max="25" onChange={handleChange} />
          </div>
          <div className="col-md-3">
            <label className="form-label fw-bold">Giới tính</label>
            <select name="gender" className="form-select" onChange={handleChange}>
              <option value="male">Nam</option>
              <option value="female">Nữ</option>
              <option value="other">Khác</option>
            </select>
          </div>
        </div>
      </div>

      {/* PHẦN 2: HOÀN CẢNH HỌC TẬP */}
      <div className="mb-4 p-3">
        <h5 className="text-success border-bottom pb-2 mb-3">
          <BookOpen className="me-2" size={20} /> Môi trường & Thói quen
        </h5>
        <div className="row g-3">
          <div className="col-md-4">
            <label className="form-label fw-bold">Loại trường</label>
            <select name="school_type" className="form-select" onChange={handleChange}>
              <option value="public">Công lập</option>
              <option value="private">Dân lập</option>
            </select>
          </div>
          <div className="col-md-4">
            <label className="form-label fw-bold">Học vấn phụ huynh</label>
            <select name="parent_education" className="form-select" onChange={handleChange}>
              <option value="no formal">Không có bằng cấp</option>
              <option value="high school">Cấp 3</option>
              <option value="diploma">Cao đẳng</option>
              <option value="graduate">Đại học</option>
              <option value="post graduate">Sau đại học</option>
              <option value="phd">Tiến sĩ</option>
            </select>
          </div>
          <div className="col-md-4">
            <label className="form-label fw-bold">Cách thức học</label>
            <select name="study_method" className="form-select" onChange={handleChange}>
                <option value="notes">Ghi chép</option>
                <option value="textbook">Sách giáo khoa</option>
                <option value="group study">Học nhóm</option>
                <option value="coaching">Luyện thi</option>
                <option value="mixed">Hỗn hợp</option>
            </select>
          </div>
          <div className="col-md-4">
            <label className="form-label fw-bold">Thời gian đi học</label>
            <select name="travel_time" className="form-select" onChange={handleChange}>
              <option value="<15 min">Dưới 15 phút</option>
              <option value="15-30 min">15 - 30 phút</option>
              <option value="30-60 min">30 - 60 phút</option>
              <option value=">60 min">Trên 60 phút</option>
            </select>
          </div>
          <div className="col-md-4">
            <label className="form-label fw-bold">Internet</label>
            <select name="internet_access" className="form-select" onChange={handleChange}>
              <option value="yes">Có</option>
              <option value="no">Không</option>
            </select>
          </div>
          <div className="col-md-4">
            <label className="form-label fw-bold">Ngoại khóa</label>
            <select name="extra_activities" className="form-select" onChange={handleChange}>
              <option value="no">Không</option>
              <option value="yes">Có</option>
            </select>
          </div>
        </div>
      </div>

      {/* PHẦN 3: KẾT QUẢ HỌC TẬP */}
      <div className="mb-4 p-3 bg-light rounded">
        <h5 className="text-danger border-bottom pb-2 mb-3">
          <BarChart3 className="me-2" size={20} /> Chỉ số học tập
        </h5>
        <div className="row g-3">
          <div className="col-md-6">
            <label className="form-label fw-bold">Giờ học/Tuần: {formData.study_hours}</label>
            <input type="number" name="study_hours" className="form-control" defaultValue="15" onChange={handleChange} />
          </div>
          <div className="col-md-6">
              <label className="form-label fw-semibold">Chuyên cần: {formData.attendance}%</label>
              <input type="range" name="attendance" className="form-range" defaultValue="85" onChange={handleChange} />
          </div>
          <div className="col-md-4">
            <label className="form-label fw-bold">Điểm Toán</label>
            <input type="number" name="math_score" className="form-control text-primary fw-bold" defaultValue="70" onChange={handleChange} />
          </div>
          <div className="col-md-4">
            <label className="form-label fw-bold">Điểm Khoa học</label>
            <input type="number" name="science_score" className="form-control text-success fw-bold" defaultValue="70" onChange={handleChange} />
          </div>
          <div className="col-md-4">
            <label className="form-label fw-bold">Điểm Tiếng Anh</label>
            <input type="number" name="english_score" className="form-control text-warning fw-bold" defaultValue="70" onChange={handleChange} />
          </div>
        </div>
      </div>

      <div className="text-center mt-4 pb-3">
        <button type="submit" className="btn btn-primary btn-lg px-5 shadow" disabled={loading}>
          {loading ? "Đang phân tích..." : "DỰ ĐOÁN NGAY"}
        </button>
      </div>
    </form>
  );
};

export default PredictionForm;