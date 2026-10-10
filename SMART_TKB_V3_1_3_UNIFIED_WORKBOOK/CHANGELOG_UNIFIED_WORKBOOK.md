# Changelog — V3.1.3 Unified Workbook Candidate

- Thêm workbook thật 11 sheet, tiêu đề tiếng Việt, tab màu, freeze/filter, chọn danh mục và kiểm tra số nguyên trong Excel; ví dụ chỉ ở HUONG_DAN.
- Thêm bộ nhập/xuất toàn bộ module, chuẩn mã và tham chiếu; giữ dữ liệu/truy vết/cấu hình khi roundtrip workbook 37 lớp.
- Lịch từng lớp/ngày có số tiết sáng/chiều riêng; 0 nghỉ. Phạm vi XEP và KHOA độc lập, lịch các khối khác giữ nguyên.
- Thêm preview không ghi dữ liệu, báo lỗi theo ô Excel và tải báo cáo. Token xem trước có hạn, bảo vệ stale context và chỉ dùng một lần.
- Xác nhận nhập toàn bộ, lưu bản trước nhập và khôi phục sau tải lại trang. Lưu trình duyệt thất bại không thay một phần phiên. Lịch được hậu kiểm lại khi khôi phục, không kế thừa chứng minh cũ.
- Giữ nguyên grade-only CP-SAT, warm start, local reoptimization, teacher-time priorities và independent conflict checks.
- Thêm 43 kiểm thử workbook Python và 16 kiểm tra browser; chạy lại 163 regression Python và 55 kiểm tra browser kế thừa. Đã mở/lưu lại workbook bằng LibreOffice và nhập lại dữ liệu 37 lớp.
- Không ghi đè SOURCE/baseline, không sửa main, không nâng Production; Microsoft Excel/Windows thực tế chưa nghiệm thu.
