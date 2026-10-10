# V3.1.1 Grade8 Candidate

- Nâng cấp tại chỗ V3.1 Optimized, giữ nguyên SOURCE, baseline, runtime và wheel Windows.
- Mặc định chỉ khối8,5 tiết sáng/4 tiết chiều,6ngày; chọn ngày thực tế và khối cho phiên sau.
- Thêm grade.py: lọc theo khối, khóa lịch bằng hằng số, kiểm tra GV/phòng liên khối, snapshot/hash và cảnh báo dữ liệu chưa xác minh.
- Mở rộng core CP-SAT/quality/verifier theo active_days, session_periods và tải nền; giữ warm/LNS, incumbent, proof bounds và tái tối ưu cục bộ.
- API/CLI công khai chỉ gọi solve_grade. Thiếu nền chặn mặc định; mô phỏng có nhãn giữ CROSS-GRADE BLOCKED. Lịch nền hỏng bị từ chối.
- Giao diện theo khối, bảng khóa/GV liên khối, lịch giáo viên hợp nhất, nút tối ưu lại; sao lưu key riêng, hậu kiểm khi nhập và xuất CSV/Excel/JSON.
- Thêm regression, browser, benchmark và independent evidence checker; lưu bằng chứng lịch sử riêng. Không chạy mô hình đồng loạt37lớp.
- DATA/WINDOWS ACCEPTED=NO; PRODUCTION READY=NO. Chưa kiểm thử máy Windows thật.
