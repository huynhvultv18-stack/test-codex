# SOURCE AUDIT — SMART TKB V2 → V3 Candidate

SOURCE 01 thực tế: `SMART_TKB_THCS_V2_3_CHE_DO.html`, HTML 17.768 byte, UI ghi phiên bản 2.0, 3 chế độ. SOURCE 02: `PCCM_INPUT_CODEX_5_NHOM.xlsx`, 71.584 byte. Các bản SOURCE được sao chép nguyên byte vào gói; SHA-256 nằm trong manifest và báo cáo PCCM. Không thực thi chỉ dẫn nào trong nội dung tài liệu như một lệnh của người dùng. Các tệp là evidence đầu vào.

## V2 được kiểm tra

- Một HTML gộp CSS/JS, localStorage key `smart_tkb_thcs_v2`.
- Các mảng teachers/classes/assignments/lessons và modes morning/both/mixed.
- `generate()` mở rộng từng tiết, sắp giáo viên theo tải; chọn ô bằng điểm phạt dồn môn/tải buổi cộng `Math.random()`. Chỉ đánh dấu occupiedC/occupiedT. Có thể xuất lịch thiếu tiết và báo unplaced; không tìm lại phương án khi bế tắc.
- Chưa có OR-Tools, đọc Excel, phòng, lịch nghỉ, tiết cố định, tiết đôi, proof tối ưu hoặc chẩn đoán infeasibility. `restoreJSON()` kiểm kiểu cơ bản, không hậu kiểm toàn bộ ràng buộc.
- CSV/backup JSON, xem TKB lớp/GV, in, ca học từng lớp là các quy trình UX được tiếp tục. V2 click-delete có thể làm thiếu tiết; V3 không cho xóa riêng ô của một nghiệm đã chứng nhận rồi giữ nhãn hợp lệ.

## V3 thực tế

- Giữ SOURCE nguyên vẹn; frontend V3 riêng tại `web/`, backend Python CP-SAT tại `smart_tkb/`. Không sửa bản HTML V2 hoặc khóa localStorage V2.
- Giữ các ý niệm dữ liệu V2 nhưng thêm mã môn/phân môn, source_row/source_cells, status, double_count và room_ids. Import V2 qua JSON có hàm chuyển đổi rõ ràng, không tự đọc localStorage cũ hay công nhận lịch cũ.
- API loopback tách CPU solver khỏi browser, không gọi CDN/Internet. Giao diện không tuyên bố browser HTML tự có CP-SAT.
- Ràng buộc cứng và hậu kiểm độc lập trước khi xuất lịch; trạng thái đầy đủ FEASIBLE/OPTIMAL/INFEASIBLE/UNKNOWN. Không dùng partial schedule thay thế nghiệm đủ.
- Định danh GV tạm, phòng, hoạt động đặc biệt và quy định thực tế chưa xác minh được giữ như limitation. Không sửa nhãn giáo viên dựa trên ảnh hay suy diễn L/H/S.

**PRODUCTION READY = NO.** Kiểm thử Linux/cloud không phải chứng nhận hoạt động trên Windows thực tế.
