# FULL AUDIT · SMART TKB THCS V3.1 Optimized Candidate

AUDIT = PASS trong phạm vi code, mô hình, API, UI, nhập/xuất và bằng chứng thực thi Linux. WINDOWS RUNTIME = UNTESTED. DATA ACCEPTED = NO; WINDOWS ACCEPTED = NO; PRODUCTION READY = NO.

## Nguồn và phạm vi

Chọn ZIP V3.1 đã bàn giao với commit ac9b34b06ddd13c016a52449a5f7c9e7ea2036c5, SHA-256 a94c50bbe617c72210412ff5fa9b491d1bc2691fd6502fe7a35436ece04029e9. CRC và manifest gốc đạt. Làm việc trên thư mục riêng OPTIMIZED; không kết hợp nhánh. SOURCE_LOCK.json ghi danh tính. Baseline A để chạy test là bản giải nén riêng; archive và thư mục V3.1 bàn giao bất biến. Bản gốc HTML/XLSX giữ nguyên byte. Không sửa main/Production.

| Thành phần | Rà soát và bằng chứng | Kết luận |
|---|---|---|
| Kiến trúc | 9 module smart_tkb, 3 web assets, CLI, scripts, runtime Windows; importer → projection → solver → verifier → exchange/API | PASS; không xây lại ứng dụng |
| PCCM | Đọc trực tiếp 5 sheet; ID riêng, NFC, chống trùng, nhãn/khối, định mức, truy vết, tổng giáo viên/lớp; 37 lớp, 64 GV, 555 phân công, 972 tiết | PASS kỹ thuật; 69 cảnh báo nguồn vẫn giữ |
| Solver HARD | Khối 1/2 tiết; bằng tổng PCCM; AtMostOne cho teacher/class/room; ca/khóa/nghỉ/công suất; phòng opt-in; subject hard limits opt-in | PASS; tests xung đột, infeasible và hậu kiểm mọi lịch A/B |
| Tiết trống | before/after trong cùng teacher/day/shift; gap iff both and !occupied; không đếm nghỉ giữa sáng/chiều | PASS; fixture am 0,2 + pm 0,1 chỉ có 1 gap/2 visits |
| Số buổi | Biến max(occ); tải/ca lower bound; không suy bound thành lịch; nghiệm đạt bound sau hậu kiểm mới chứng minh mức | PASS; 217/239 ở warm 37 lớp, phạm vi prefix |
| Phân bố/dồn môn | Min/max ngày theo môn gốc; excess, adjacency miễn tiết đôi, heavy runs opt-in; soft theo khối; independent metrics | PASS; công thức ALGORITHM.md, unit grade/weights/preferences |
| Warm/LNS/local | Nghiệm trước hậu kiểm, hint toàn biến; frozen ngoài scope; khóa proven/incumbent báo riêng | PASS chức năng; chất lượng biến động theo seed, xem OPTIMIZATION.md |
| SpecialActivity | 74 bản ghi/111 tiết; giữ nhãn CC/SHCN ghép; STRICT/SCENARIO; approved/missing/conflict; tập thể một tài nguyên GV/phòng nhiều lớp | PASS; không gán thiếu dữ liệu hoặc cộng pending vào placed |
| API cục bộ | Bind 127.0.0.1; Host/Origin/CSRF; CSP self; body size; ZIP expansion bound; finite JSON; serialized jobs | PASS trong local threat model; không phải pen-test/kiểm định bảo mật toàn diện |
| Nhập/xuất/lưu | PCCM XLSX, V2/V3/V3.1 JSON, CSV/XLSX schedules, backup; hậu kiểm lại, không kế thừa optimality; restore atomic | PASS; roundtrip browser/unit, ID và dữ liệu nguồn giữ nguyên |
| UI | 5 tabs, tiến độ, 6 mục tiêu, ca theo lớp, đặc biệt, thống kê, in/backup/chart, trước/sau; localStorage key riêng | PASS Chromium Linux; 390/768/1366 và baseline 1440 px |
| Windows/offline | Runtime PSF x64 Python 3.12.10, 12 wheel, lock hash, no-index launcher, all source hash | STATIC/OFFLINE RESOLUTION PASS; thực thi Windows BLOCKED |
| Regression/packaging | Giữ toàn bộ 45 unit/20 browser gốc; bổ sung test lỗi; manifest/CRC/extract/extracted tests | Xem REGRESSION.md và PACKAGE_VERIFICATION.json |

## Kết quả lỗi và rủi ro còn lại

14 phát hiện A01–A14 trong BUGFIX.md: 1 CRITICAL, 4 HIGH, 7 MEDIUM, 2 LOW. Không còn lỗi CRITICAL/HIGH đã biết chưa xử lý trong phạm vi kiểm tra. Linux không chứng minh chạy được trên Windows. 64 định danh GV chưa xác minh, 3 ký hiệu phân môn chưa chú giải, 111 tiết thiếu quy tắc, 34 ô nguồn đánh dấu xung đột vẫn là dữ liệu cần nhà trường xác nhận.

Hai ca được mô hình theo ô rời; không mô hình phút, di chuyển giữa cơ sở, đồng giảng nhiều GV hoặc lịch nhiều tuần. Không tạo phòng/tiết khóa/GV để biến morning thành có nghiệm: GV015 40 > 30. Trạng thái INFEASIBLE có proof công suất, UNKNOWN không có lịch có metrics/conflicts null. Toàn bộ lịch benchmark khả thi là FEASIBLE; không tuyên bố tối ưu toàn cục. Tiêu chí nghiệm thu và các giới hạn kết quả được ghi riêng ở ACCEPTANCE.json.
