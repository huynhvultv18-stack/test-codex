# V3.0 Candidate

- Thay luồng xếp ngẫu nhiên tham lam V2 bằng Google OR-Tools CP-SAT; không sử dụng `Math.random()` để quyết định lịch.
- Thêm importer đọc trực tiếp cả 5 sheet PCCM, đối chiếu tổng theo lớp/GV/môn và truy vết dòng/ô nguồn. Giữ nguyên mọi mã giáo viên tạm, ký hiệu phân môn, cảnh báo định danh.
- Thêm ràng buộc cứng lớp/GV/phòng, ca, lịch nghỉ, tiết khóa, số tiết/buổi, tiết đôi không vượt buổi. Không xuất lịch một phần khi chưa có nghiệm.
- Tối ưu lexicographic 6 mức ưu tiên, warm start đầy đủ, khóa ngoài phạm vi khi xếp lại cục bộ; chẩn đoán capacity và sufficient assumption core khi vô nghiệm.
- Thêm verifier độc lập, trạng thái nghiệm/cận/proof rõ ràng, bảo vệ lịch cũ khi cấu hình đổi.
- Giao diện tiếng Việt responsive: TKB lớp/GV, PCCM, ca lớp, tiết đôi/phòng, cảnh báo, cấu hình, benchmark; Excel upload, CSV, backup V3 và nhập JSON V2 riêng.
- Gói ngoại tuyến Windows x64 kèm Python 3.12.10 và các wheel cp312 win_amd64 với hash. Không dùng Internet lúc cài/chạy.
- Giữ nguyên SOURCE. PRODUCTION READY = NO; chưa kiểm thử Windows thực tế; 111 tiết đặc biệt chưa có phân công không được tự sinh.
