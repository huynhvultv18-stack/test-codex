# V3.1.2 Session Config Candidate

- Từ baseline V3.1.1 bất biến; không ghi đè SOURCE, phiên bản cũ hoặc main.
- Cấu hình buổi riêng theo khối/lớp/ngày;0=NGHỈ,1..N là miền tiết. Mặc định khối8 đúng cấu hình41ô/9buổi của người dùng; Chủ nhật tùy chọn, mở rộng tối đa8.
- CP-SAT, hậu kiểm độc lập, phân bố môn, công suất GV/phòng/lớp dùng lịch hiệu lực từng lớp. Giữ HARD-first, warm/best incumbent, cục bộ và chẩn đoán vô nghiệm.
- UI chỉnh/copy/áp dụng cả khối, lưu/khôi phục/JSON, cảnh báo công suất/tiết cố định, NGHỈ và không tạo ô giả.
- Xác nhận gắn với SHA của cấu hình và lịch cũ khi ảnh hưởng tiết đã xếp; API chặn trước CP nếu thiếu xác nhận. Hủy giữ lịch, tắt warm không bỏ qua xác nhận; reload giữ cấu hình đang sửa.
- Chuyển khối trong phiên sau giữ lịch buổi từng lớp của lịch khóa, không mở rộng thành lịch đồng nhất. Không giải đồng loạt37lớp.
- CSV/Excel giữ rõ buổi0; nhập lại kiểm tra lịch buổi và xung đột liên khối. Nhập cấu hình bất hợp lệ không sửa trạng thái; khóa thao tác trong khi chờ nhập để tránh phản hồi cũ ghi đè thao tác mới.
- Kiểm thử và benchmark riêng khối8; bằng chứng hiện tại trong reports/SESSION_*. Báo cáo cũ trong reports/historical_v311, không là nghiệm thu V3.1.2.
- DATA ACCEPTED=NO; WINDOWS ACCEPTED=NO; PRODUCTION READY=NO.

# V3.1.1 Grade8 Candidate

- Nâng cấp tại chỗ V3.1 Optimized, giữ nguyên SOURCE, baseline, runtime và wheel Windows.
- Mặc định chỉ khối8,5 tiết sáng/4 tiết chiều,6ngày; chọn ngày thực tế và khối cho phiên sau.
- Thêm grade.py: lọc theo khối, khóa lịch bằng hằng số, kiểm tra GV/phòng liên khối, snapshot/hash và cảnh báo dữ liệu chưa xác minh.
- Mở rộng core CP-SAT/quality/verifier theo active_days, session_periods và tải nền; giữ warm/LNS, incumbent, proof bounds và tái tối ưu cục bộ.
- API/CLI công khai chỉ gọi solve_grade. Thiếu nền chặn mặc định; mô phỏng có nhãn giữ CROSS-GRADE BLOCKED. Lịch nền hỏng bị từ chối.
- Giao diện theo khối, bảng khóa/GV liên khối, lịch giáo viên hợp nhất, nút tối ưu lại; sao lưu key riêng, hậu kiểm khi nhập và xuất CSV/Excel/JSON.
- Thêm regression, browser, benchmark và independent evidence checker; lưu bằng chứng lịch sử riêng. Không chạy mô hình đồng loạt37lớp.
- DATA/WINDOWS ACCEPTED=NO; PRODUCTION READY=NO. Chưa kiểm thử máy Windows thật.
