import { useState } from 'react'
import axios from 'axios'
import './App.css'

function App() {
    const [formData, setFormData] = useState({
        AttendanceRate: '',
        StudyHoursPerWeek: '',
        PreviousGrade: '',
        ExtracurricularActivities: '',
        Gender: 'Male',
        ParentalSupport: 'Medium',
        OnlineClasses: 'False'
    });

    const [prediction, setPrediction] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handlePredict = async () => {
        setLoading(true);

        const att = Number(formData.AttendanceRate) || 0;
        const study = Number(formData.StudyHoursPerWeek) || 0;
        const prev = Number(formData.PreviousGrade) || 0;
        const act = Number(formData.ExtracurricularActivities) || 0;

        const finalData = {
            'AttendanceRate': att,
            'StudyHoursPerWeek': study,
            'PreviousGrade': prev,
            'ExtracurricularActivities': act,
            'Gender': formData.Gender,
            'ParentalSupport': formData.ParentalSupport,
            'Online Classes Taken': formData.OnlineClasses === 'True'
        };

        try {
            const response = await axios.post('http://127.0.0.1:8000/api/predict/', finalData);
            let resVal = response.data.result;

            // Lấy kết quả và hiển thị
            const finalScore = Array.isArray(resVal) ? resVal[0] : resVal;
            setPrediction(Number(finalScore).toFixed(2));
        } catch (error) {
            console.error("Lỗi:", error);
            alert("Đã có lỗi xảy ra khi dự đoán!");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container">
            <h1>Dự Đoán Kết Quả Học Tập</h1>
            <div className="predict-form">
                <div className="input-group">
                    <label>Tỷ lệ chuyên cần (%):</label>
                    <input type="text" name="AttendanceRate" value={formData.AttendanceRate} onChange={handleChange} placeholder="Ví dụ: 90" />
                </div>
                <div className="input-group">
                    <label>Giờ học mỗi tuần:</label>
                    <input type="text" name="StudyHoursPerWeek" value={formData.StudyHoursPerWeek} onChange={handleChange} placeholder="Ví dụ: 20" />
                </div>
                <div className="input-group">
                    <label>Điểm số kỳ trước:</label>
                    <input type="text" name="PreviousGrade" value={formData.PreviousGrade} onChange={handleChange} placeholder="Ví dụ: 75" />
                </div>
                <div className="input-group">
                    <label>Số hoạt động ngoại khóa:</label>
                    <input type="text" name="ExtracurricularActivities" value={formData.ExtracurricularActivities} onChange={handleChange} placeholder="Ví dụ: 2" />
                </div>
                <div className="input-group">
                    <label>Giới tính:</label>
                    <select name="Gender" value={formData.Gender} onChange={handleChange}>
                        <option value="Male">Nam</option>
                        <option value="Female">Nữ</option>
                    </select>
                </div>
                <div className="input-group">
                    <label>Hỗ trợ gia đình:</label>
                    <select name="ParentalSupport" value={formData.ParentalSupport} onChange={handleChange}>
                        <option value="Low">Thấp</option>
                        <option value="Medium">Trung bình</option>
                        <option value="High">Cao</option>
                    </select>
                </div>
                <div className="input-group">
                    <label>Học trực tuyến:</label>
                    <select name="OnlineClasses" value={formData.OnlineClasses} onChange={handleChange}>
                        <option value="True">Có</option>
                        <option value="False">Không</option>
                    </select>
                </div>
                <button className="btn-predict" onClick={handlePredict} disabled={loading}>
                    {loading ? 'Đang tính...' : 'Dự Đoán Ngay'}
                </button>
            </div>
            {prediction && (
                <div className="result-section">
                    <h3>Điểm dự đoán của bạn: <span className="highlight">{prediction}</span></h3>
                </div>
            )}
        </div>
    );
}

export default App;