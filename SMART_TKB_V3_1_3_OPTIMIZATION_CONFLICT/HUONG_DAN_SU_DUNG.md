# Hướng dẫn SMART TKB THCS V3.1.3 Candidate

## Mở trên Windows

Tải ZIP đầy đủ, kiểm tra SHA-256 bên cạnh ZIP, giải nén toàn bộ vào thư mục riêng, rồi mở `START_WINDOWS.bat`. Không chạy bên trong ZIP. Gói kèm Python 3.12.10 x64 và wheel OR-Tools/openpyxl; cài đặt không dùng Internet, không cần quyền quản trị. Trình duyệt mở `http://127.0.0.1:8768`. Giữ cửa sổ chương trình mở; Ctrl+C để dừng. Windows thực tế chưa được nghiệm thu: DATA ACCEPTED = NO, WINDOWS ACCEPTED = NO, PRODUCTION READY = NO.

Mã nguồn trong GitHub không kèm bộ Python/wheel; muốn chạy Windows ngoại tuyến cần ZIP trong `dist`. Có Python riêng: `python -m venv .venv`, cài `requirements.txt` rồi `python -m smart_tkb.server --open`.

## Xếp khối 8, giữ các khối khóa

1. Chọn khối cần xếp. Mặc định khối 8, chỉ các lớp khối 8 có biến xếp; nền khối 6/7/9 giữ nguyên từng dòng. Nạp lịch nền JSON của trường ở mục phạm vi. Xem khối thiếu và GV nhiều khối trước khi giải.
2. Nhập Excel PCCM bằng nút riêng; xem mã, nhãn, định danh, số tiết, các cảnh báo. Không đổi mã GV chưa xác minh để giảm xung đột. Bổ sung dữ liệu qua JSON có đối chiếu từ trường; phần mềm không gộp theo tên.
3. Chọn số tiết theo ngày/buổi cho cả khối hoặc từng lớp. Tham khảo: Hai 5/4, Ba 5/0, Tư 5/4, Năm 5/0, Sáu 5/4, Bảy 4/0; Chủ nhật 0/0. **0 = NGHỈ**, không tạo ô trong buổi nghỉ. Chế độ chỉ sáng/sáng–chiều/phân ca còn giới hạn ca được phép, giữ nguyên số tiết bạn đã nhập. Khi đổi số tiết ảnh hưởng lịch cũ, hộp thoại trong phần mềm yêu cầu xác nhận xếp lại; hủy vẫn giữ lịch và cấu hình đang chỉnh.
4. Ở Ràng buộc & tối ưu, bật V3.1.3 và chọn FAST, BALANCED hoặc PROVE_OPTIMAL, ngân sách giây, worker, seed. BALANCED là mặc định. PROVE_OPTIMAL không hứa có chứng minh trong thời gian đã chọn. Muốn giữ lịch cũ, bật Dùng lịch hiện tại; solver chỉ giữ incumbent nếu hậu kiểm đạt.
5. Mặc định ưu tiên tiết trống → buổi → ngày → chờ (nếu bật) → cụm tiết → phân bố → nguyện vọng → công bằng → dồn môn → thay đổi. Có thể sửa chuỗi 10 mã trong giao diện; phải đủ và không lặp. Checkbox bật/tắt các mục tiêu tương thích nằm phía dưới. Bật chờ và công bằng khi phù hợp.
6. Để báo chờ bằng phút, điền giờ đủ tất cả ô có thể xếp và ô nền bận: `[{"day":0,"shift":"am","period":0,"start":420,"end":465},...]`; điền nghỉ trưa `{"start":720,"end":780}`. Các số chỉ minh họa cú pháp, **không phải giờ trường đã xác minh**. Ngày 0=Hai, tiết 0=tiết 1; start/end là phút từ 00:00. Thiếu giờ hay nghỉ trưa sẽ báo PROXY, không tự đoán thời gian.
7. Đặt tiết đôi/phòng trong bảng PCCM, khai báo mã phòng và lịch nghỉ/cố định ở JSON bổ sung. Đồng giảng có thể nhập `co_teacher_ids` vào phân công JSON; dùng đúng mã GV, mỗi GV bị khóa tài nguyên riêng. Không sửa SOURCE đính kèm.
8. Bấm Xếp TKB hoặc Tối ưu lại. Xem số tiết đã xếp, trạng thái CP, từng phase objective/bound/gap, các mức có chứng minh và những khóa chỉ có điều kiện. FEASIBLE đủ HARD trong phạm vi dữ liệu đã biết; không phải tối ưu toàn trường. UNKNOWN khác INFEASIBLE.

PCCM hiện tại có 37 lớp; khối 8 có 234 tiết môn, 27 tiết đặc biệt PENDING, 26 mã GV chưa xác minh. Nền khóa có 738 tiết môn, còn thiếu 84 tiết đặc biệt. Mặc định BLOCKED. Để thử kỹ thuật, bật mô phỏng và ghi rõ dữ liệu thiếu/giả định; kết quả vẫn INCOMPLETE, không phải lịch được trường nghiệm thu.

## Kiểm tra, chỉnh và lưu

- **KIỂM TRA TRÙNG TIẾT** kiểm tra GV/lớp/phòng trên lịch kết hợp với nền; có số lỗi liên khối, buổi 0, quá số tiết, vi phạm HARD và cảnh báo dữ liệu. Bấm Định vị để tìm ô lỗi. Một lỗi có thể có nhiều dòng liên quan; không tự chuyển các dòng khóa.
- Nhấp ô tiết của khối đang chọn để chuyển ngày/buổi/tiết/phòng. PCCM, GV, lớp, môn, độ dài giữ nguyên. Sau chuyển, hậu kiểm tự chạy; nếu FAIL, sửa hoặc lưu DRAFT. Không sửa ô nền bị khóa.
- Xuất Excel kiểm tra gồm KIEM_TRA, XUNG_DOT, CANH_BAO; In báo cáo lỗi dành riêng phần hậu kiểm. Chỉ số tiết trong CSV/Excel dữ liệu dùng chỉ số 0; giao diện hiển thị tiết 1 trở đi.
- **PASS**: dữ liệu đầy đủ trong phạm vi kiểm tra và HARD đạt, có thể bấm Xác nhận hợp lệ. Xác nhận luôn kiểm tra lại hash và HARD ở server. PASS không là Production approval hay nghiệm thu Windows.
- **FAIL**: có lỗi HARD, chặn xác nhận. **INCOMPLETE**: thiếu nền/định danh/hoạt động/cảnh báo nguồn; chỉ lưu bản nháp. **STALE**: lịch, dữ liệu hoặc cấu hình đổi, chứng nhận cũ hết hiệu lực; bấm kiểm tra lại.
- Lưu bản nháp JSON luôn hậu kiểm và gắn nhãn DRAFT. CSV/Excel lịch được kiểm tra trước khi xuất. Khôi phục V3.1.3 DRAFT hoặc nhập CSV/Excel tự hậu kiểm; lịch sai HARD được giữ có cờ FAIL để sửa. Chứng minh tối ưu cũ không được kế thừa từ bản nhập. Backup V2/V3/V3.1/V3.1.1/V3.1.2 vẫn được kiểm tra theo quy tắc tương thích.
- Xem Chất lượng nghiệm: tổng nền và tổng kết hợp, bảng từng GV trước/sau về tiết trống/buổi/ngày/chờ/cụm. Chờ ghi REAL_MINUTES hoặc PROXY; công bằng hiện tại là số tiết trống tuần lớn nhất của một GV.
- Xếp cục bộ: bật lịch hiện tại + Khóa ngoài phạm vi, nhập mã lớp/GV hoặc `day:0`, `session:0:pm`, phân cách dấu phẩy. Các phạm vi là hợp nhau; mọi dòng ngoài phạm vi và các khối khóa giữ nguyên. Chứng minh chỉ cho phạm vi được chọn.
- Đổi sang khối khác chỉ đóng băng lịch hiện hành đã kiểm tra và chuẩn bị phiên mới; không tự chạy giải. Nếu lịch cũ sai hoặc STALE, kiểm tra/giải lại trước khi đổi.

## Kiểm thử phát triển

`python tests/run_grade_regression.py` chạy hồi quy riêng khối và các kiểm thử mới. Ba test toàn trường lịch sử được giữ nguyên nhưng runner loại khỏi phạm vi; tên/lý do có trong báo cáo. Không dùng các benchmark 37 lớp cũ để nghiệm thu V3.1.3.

Khởi động server trước rồi chạy `tests/grade_browser.cjs`, `tests/session_browser.cjs`, `tests/time_conflict_browser.cjs` với Playwright/Chromium và biến `TKB_BASE`. Chạy tuần tự. A/B: `python tests/time_conflict_benchmark.py --baseline <thu_muc_giai_nen_V3.1.2_rieng>`; baseline gốc chỉ đọc, số liệu lưu trong Candidate. `python tests/verify_time_conflict_evidence.py` kiểm tra bằng chứng không chạy solver.

Xem báo cáo `reports/TIME_CONFLICT_BENCHMARK.md`, `TIME_CONFLICT_REGRESSION.json`, `TIME_CONFLICT_INDEPENDENT_VERIFICATION.json`, `TIME_CONFLICT_ALGORITHM.md`, `TIME_CONFLICT_ACCEPTANCE.json`. Báo cáo V3.1.2/cũ nằm trong `reports/historical_v312`, không là nghiệm thu bản này.
