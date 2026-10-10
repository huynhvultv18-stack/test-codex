# Thuật toán V3.1.3 Candidate

Chỉ lớp thuộc `target_grade` tạo biến quyết định. Các dòng lịch nền được giữ nguyên mọi trường và kiểm tra bằng SHA-256 trước/sau. Đọc đầy đủ PCCM 37 lớp để kiểm tra nguồn và tài nguyên dùng chung; không chạy tối ưu 37 lớp trong bản nâng cấp này.

## Ba lớp bảo đảm

1. CP-SAT dùng biến boolean cho mỗi vị trí hợp lệ của bloc 1 hoặc 2 tiết. Mỗi phân công có đúng số tiết và cặp đôi. Mỗi ô lớp/GV/phòng có AtMostOne; phòng chức năng, ca học, buổi 0, số tiết N, lịch nghỉ, tiết cố định, tải tối đa và phạm vi cục bộ đều là HARD. Tiết đôi mở rộng chiếm cả hai ô. Vì dùng miền ô rời rạc, không cần thêm NoOverlap interval trùng chức năng. Đồng giảng khai báo `co_teacher_ids` rõ ràng; mỗi GV cùng chiếm tài nguyên. Sự kiện tập thể là một dòng có nhiều `class_ids`, không nhân bản thành những dòng gây trùng giả.
2. `conflicts.py` tạo hashmap theo mã tài nguyên + ngày + buổi + tiết trên lịch đã mở rộng. Kiểm tra cả khối chọn và nền khóa, trả lỗi kèm từng dòng liên quan, loại, mức độ, vị trí và đề xuất. Không đọc biến CP.
3. Hậu kiểm gọi `verify_grade`/`verify_schedule` độc lập để đối chiếu PCCM, số tiết, định danh, buổi, phòng, lịch nghỉ, cố định, đôi, tải và hash khóa. Không tin cờ PASS do client gửi. `confirm` luôn kiểm tra lại.

## Chỉ số thời gian

- `teacher_busy`: tập ô có giảng dạy, gồm GV chính và mã đồng giảng được khai báo.
- `teacher_present`: ngày/buổi có ít nhất một ô dạy; `day_present`: một ngày có ít nhất một buổi.
- Tiết trống = max(ô) − min(ô) + 1 − số ô dạy, tính riêng trong mỗi buổi. Không tính phần trước tiết đầu hoặc sau tiết cuối.
- Số buổi/ngày tính từ hợp của khối chọn với nền khóa; báo riêng tổng nền, tổng kết hợp và thay đổi so với nền. Lấp một lỗ nền có thể làm số tiết trống/cụm giảm, không được giả định phần tăng luôn không âm.
- Fragmentation = số cụm liên tiếp trong ngày/buổi. Fairness = số tiết trống tuần lớn nhất của một GV, định nghĩa công bố rõ; không phải tất cả khái niệm công bằng tải dạy.
- Chờ hai buổi chỉ có khi cùng GV dạy cả sáng và chiều cùng ngày. Có đủ `period_times` và `lunch_break`: tính phút từ hết tiết sáng cuối đến đầu tiết chiều đầu, trừ phần giao với nghỉ trưa quy định. Thiếu mốc: PROXY = số ô sau tiết sáng cuối trong chiều rộng lịch vật lý + số ô trước tiết chiều đầu. PROXY là ô đại diện, không phải phút; không thêm giờ nghỉ trưa giả định.

## Tối ưu từ điển và chứng minh

Mặc định HARD → gaps → visits → days → waiting (tùy bật) → fragmentation → distribution → preferences → fairness (tùy bật) → concentration → changes. Thứ tự đủ 10 mã, duy nhất, do người dùng chỉnh. Sáu mục tiêu tương thích cũ vẫn có bật/tắt/trọng số; trọng số trong một mức không biến thành tổng đánh đổi giữa các mức.

FAST giữ nghiệm khả thi đã kiểm tra. BALANCED chia ngân sách theo trọng số phase và thời gian còn lại; được khóa giá trị nghiệm đã kiểm tra khi chưa có chứng minh, nhưng mọi mức sau được gắn `conditional_on_incumbent_locks`. PROVE_OPTIMAL dành thời gian còn lại cho mức chưa chứng minh và dừng chuyển mức khi chưa OPTIMAL; có thể vẫn FEASIBLE/UNKNOWN, không đảm bảo chứng minh trong ngân sách.

V3.1.3 chỉ ghi mức vào `proven_priorities` khi phase CP báo OPTIMAL, dòng nghiệm vượt hậu kiểm và mọi mức trước đã được chứng minh. Mức bật nhưng bị bỏ vì ngân sách không cho phép ghi nhận chứng minh phía sau: BALANCED khóa incumbent và đánh dấu có điều kiện; chế độ không cho chuyển mức thì dừng. Khóa incumbent không phải khóa optimum. Không chuyển cận dưới/hint/heuristic thành CP OPTIMAL. Chế độ tương thích V3.1.2 giữ chứng minh cận dưới cũ và được ghi LEGACY riêng.

`selected_scope_optimal_proven` chỉ phạm vi đang giải với nền cố định. Xếp cục bộ chỉ chứng minh phạm vi cục bộ; `grade_optimal_proven` không được kế thừa. `global_optimal_proven` toàn trường luôn false ở lớp tích hợp khối.

## Hiệu năng

Miền vị trí lọc ca/buổi 0/phòng/nghỉ; kiểm tra cận công suất trước khi dựng mô hình; CP presolve; không dùng đối xứng hoán vị lớp hay GV vì không được chứng minh tương đương. Biến theo vị trí tránh tạo nhãn tùy ý cho từng tiết giống hệt.

Warm start chỉ giữ incumbent sau hậu kiểm HARD liên khối; thêm hints vị trí và các biến chất lượng/chiếm ô. CP portfolio/LNS do OR-Tools quản lý; `search_mode=lns` dùng LNS và vẫn không cam kết OPTIMAL. Neighborhood theo lớp/GV/ngày/buổi là hợp các phạm vi được chọn, giữ nguyên từng dòng ngoài phạm vi và tất cả nền khóa. Multi-seed tối đa 4 seed, chia ngân sách mỗi phase; chọn nghiệm tốt nhất đã kiểm tra cho cùng mục tiêu, dừng sớm nếu OPTIMAL. Không có một vòng LNS tự chế ngoài CP và không tuyên bố có adaptive neighborhood tự động.

Thời gian báo cả solver/phase và wall. Tạo mô hình, hậu kiểm, nhập/xuất cũng có chi phí; ngân sách CP không đảm bảo UI xong đúng tuyệt đối số giây nhập.

## Chứng nhận và trạng thái

Chứng nhận có engine_version và certificate_schema; đổi phiên bản cũng hết hiệu lực. Hash SHA-256 bao gồm dữ liệu khối, dữ liệu nền, cấu hình khối/nền, các dòng đang hiển thị, dòng khóa và thông tin phạm vi. PASS chỉ khi đủ nền, định danh, hoạt động và ràng buộc được kiểm tra. FAIL có lỗi HARD, chặn xác nhận. INCOMPLETE không có lỗi đã biết nhưng thiếu dữ liệu tin cậy, chỉ là bản nháp. STALE khi lịch/dữ liệu/cấu hình đổi sau chứng nhận; phải kiểm tra lại. Một PASS cũ hoặc tự sửa trạng thái trên JSON không làm `confirm` chấp nhận lịch lỗi.

Chỉnh tay/nhập lịch/lưu bản nháp/giải/tối ưu đều chạy hậu kiểm. Nhập CSV/XLSX sai HARD nhưng đúng cú pháp được giữ trong DRAFT kèm FAIL để sửa; dữ liệu sai cú pháp/PCCM/nền bị từ chối nguyên tử. Lịch xuất CSV/XLSX phải vượt verifier; bản INCOMPLETE ghi rõ chưa nghiệm thu. Excel lỗi dùng chuỗi literal chống công thức không chủ đích.
