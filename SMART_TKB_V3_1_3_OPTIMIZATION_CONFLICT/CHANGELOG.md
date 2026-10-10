# V3.1.3 Optimization + Conflict Candidate

- Thêm mô hình và thống kê thời gian GV trên lịch kết hợp nền bất biến: tiết trống nội bộ, buổi, ngày, chờ sáng–chiều, cụm tiết, công bằng.
- Ba hồ sơ FAST/BALANCED/PROVE_OPTIMAL, thứ tự mục tiêu tùy chỉnh, clock thực tế/nghỉ trưa hoặc PROXY rõ ràng, warm start/LNS, neighborhood lớp/GV/ngày/buổi và tối đa4seed.
- Chỉ ghi chứng minh V3.1.3 khi CP OPTIMAL và hậu kiểm; mục tiêu sau khóa incumbent/bỏ phase bật chỉ có điều kiện.
- Thêm hashmap xung đột, verifier độc lập, chứng nhận theo hash bao gồm cấu hình/dữ liệu nền, PASS/FAIL/INCOMPLETE/STALE. Xác nhận server không tin trạng thái client.
- Chỉnh tay trong khối, nhập/sửa/lưu DRAFT có hậu kiểm, định vị lỗi, Excel literal và in lỗi, bảng từng GV trước/sau.
- Đồng giảng theo mã khai báo rõ ràng và sự kiện tập thể chuẩn hóa một dòng; mọi GV/lớp/phòng bị chiếm đúng tài nguyên, mở rộng đôi để kiểm tra.
- CSV/XLSX mới thêm co_teacher_ids, vẫn đọc định dạng cũ. Giữ nguyên test/assertion hồi quy; sửa hai lỗi thấy qua test mới: mã phân công sai kiểu làm detector lỗi, nút xác nhận sau solve chưa được mở lại. Sửa overflow hash trên màn hình nhỏ.
- Giữ SOURCE và V3.1.2 nguyên vẹn. Kèm benchmark A/B riêng khối8, oracle exhaustive độc lập, kiểm thử trình duyệt, hướng dẫn Windows và SHA-256. Chưa nghiệm thu Windows/PCCM thực tế; không nâng Production.
