import React, { useState, useRef, useEffect } from 'react';
import { GraduationCap, CheckCircle2, AlertCircle} from 'lucide-react';
import axios from 'axios';
import PredictionForm from './PredictionForm';

function App() {
  const resultRef = useRef(null);
  const [formData, setFormData] = useState({
          name: '',
          age: 18,
          gender: 'male',
          school_type: 'public',
          parent_education: 'high school',
          study_hours: 15,
          attendance: 85,
          math_score: 70,
          science_score: 70,
          english_score: 70,
          internet_access: 'yes',
          travel_time: '<15 min',
          extra_activities: 'no',
          study_method: 'notes'
        });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  useEffect(() => {
  if (result && resultRef.current) {
    resultRef.current.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }
  }, [result]);

  const handleSubmit = async (e) => {
  e.preventDefault();
  setLoading(true);
  try {
    const response = await axios.post('http://127.0.0.1:8000/api/predict', formData);
    if (response.data.success) {
      setResult(response.data);
    } else {
      alert("Lỗi: " + response.data.error); // Hiện lỗi từ Backend (ví dụ: số âm)
    }
  } catch (error) {
    // Nếu Backend trả về lỗi 400, nó sẽ rơi vào catch này
    const msg = error.response?.data?.error || "Lỗi kết nối Backend!";
    alert(msg);
  }
  setLoading(false);
};

  return (
  // Thêm bg-light để có nền xám nhạt nhìn sang hơn, min-vh-100 để phủ kín màn hình
  <div className="container-fluid bg-light min-vh-100 py-5" ref={resultRef}>
    <div className="container">
      {/* Căn giữa tiêu đề */}
      <header className="text-center mb-5">
        <h1 className="text-center my-4 fw-bold text-uppercase" style={{ color: '#2c3e50' }}>
            Hệ thống dự báo kết quả học tập
        </h1>

        <p className="text-center text-muted">Đề tài 9: Student Performance Prediction (Classification)</p>
        <div className="mx-auto bg-primary" style={{ height: '4px', width: '80px', borderRadius: '2px' }}></div>
      </header>

      {/* Căn giữa row bằng justify-content-center */}
      <div className="row justify-content-center g-2">
        {/* Cột Form bên trái */}
        <div className="col-lg-7 col-md-8">
          <div className="card shadow-sm border-0 rounded-3">
            <div className="card-body p-4">
              <PredictionForm
                formData={formData}
                handleChange={handleChange}
                handleSubmit={handleSubmit}
                loading={loading}
              />
            </div>
          </div>
        </div>

        {/* Cột Kết quả bên phải */}
        <div className="col-lg-5" >
          {result ? (
            <div className={`card shadow p-4 text-center ${result.prediction === 'PASS' ? 'border-success' : 'border-danger'}`}>
              <h3 className="text-muted d-flex align-items-center justify-content-center">
                  {result.prediction === 'PASS' ?
                    <CheckCircle2 className="text-success me-2" /> :
                    <AlertCircle className="text-danger me-2" />
                  }
                  KẾT QUẢ
                </h3>
              <div className={`display-1 fw-bold ${result.prediction === 'PASS' ? 'text-success' : 'text-danger'}`}>
                {result.prediction}
              </div>
              <p className="fs-5">Độ tin cậy: <strong>{result.probability}%</strong></p>

              <div className="mt-4 p-3 bg-light rounded">
                <p className="mb-1 text-start">Xác suất Đậu:</p>
                <div className="progress mb-3" style={{height: "20px"}}>
                  <div className="progress-bar bg-success" style={{width: `${result.pass_chance}%`}}>{result.pass_chance}%</div>
                </div>
                <p className="mb-1 text-start">Xác suất Rớt:</p>
                <div className="progress" style={{height: "20px"}}>
                  <div className="progress-bar bg-danger" style={{width: `${result.fail_chance}%`}}>{result.fail_chance}%</div>
                </div>
              </div>
            </div>
          ) : (
            <div className="card shadow d-flex align-items-center justify-content-center bg-light border-0 py-5">
               <p className="text-muted italic px-3 text-center">Nhập dữ liệu và nhấn DỰ ĐOÁN NGAY để xem kết quả AI</p>
            </div>
          )}
        </div>

      </div>
    </div>
  </div>
);
}

export default App;