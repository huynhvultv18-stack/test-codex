# Kiểm thử V3.1.3 Unified Workbook Candidate

**Kết quả: PASS trên Linux; PRODUCTION READY = NO.** Ngày kiểm thử 10/10/2026. Python 3.12, OR-Tools 9.15.6755, openpyxl 3.1.5, Chromium/Playwright và LibreOfficeDev 26.8.0.0.alpha0. Chưa chạy Python Windows đi kèm hoặc mở bằng Microsoft Excel trên Windows thực tế.

## Các kiểm tra đã thực hiện

- **206 kiểm thử Python đạt**: 163 kiểm thử kế thừa và 43 kiểm thử workbook mới. Kiểm tra nguồn 37 lớp, roundtrip chính xác toàn bộ data/config/background, các lỗi mã/tham chiếu/số tiết/tiết đôi/metadata/công thức, lịch 0 buổi, lịch nền và quy tắc, cảnh báo GV, token/expiry/stale/single-use, báo cáo XLSX và CP ba chế độ trên fixture tổng hợp.
- **71 kiểm tra browser đạt**: 20 grade-only + 16 lịch buổi + 19 thời gian GV/hậu kiểm + 16 workbook. Tải XLSX thật, nhập mẫu trống không nhận ví dụ, xem trước không ghi dữ liệu, hủy/xác nhận, xuất dữ liệu 37 lớp/nhập lại, báo lỗi PCCM G2, từ chối ngữ cảnh xem trước cũ, lưu và khôi phục sau reload, phục hồi lịch/hậu kiểm, lỗi quota không thay một phần phiên, responsive 390/768/1366 và không lỗi JavaScript.
- **LibreOffice đã mở và lưu lại** mẫu và workbook 37 lớp. Workbook sau lưu nhập lại thành công; data/config/background bằng đúng trước lưu. Đây là kiểm tra tương thích định dạng XLSX, không thay nghiệm thu Microsoft Excel/Windows.
- SOURCE HTML/Excel, 1334 file runtime/wheels Windows kế thừa giữ nguyên byte. Candidate mới nằm riêng. ZIP được kiểm tra CRC, giải nén toàn bộ và đối chiếu từng mục SHA-256; xem receipt PACKAGE_VERIFICATION.json cạnh ZIP.

3 kiểm thử solver toàn trường 37 lớp cũ ngoài phạm vi grade-only được runner liệt kê rõ trong scope_exclusions, không xóa assertion. Chỉ số 206 không bao gồm 3 bài này. Các kiểm tra CP-SAT của khối, khóa liên khối, local scope, warm start, các mục tiêu/proof, hậu kiểm/khôi phục và định danh cũ vẫn chạy.

## Dữ liệu nguồn và benchmark mới

Đọc trực tiếp đủ 5 sheet PCCM nguồn rồi xuất workbook tổng hợp: **37 lớp, 64 mã GV, 17 mã môn/phân môn, 555 phân công, 972 tiết môn và 111 tiết đặc biệt chưa đủ quy tắc**. Có 64 mã GV chưa xác minh; không tự gộp tên. Workbook tham khảo chưa có phòng được yêu cầu trong PCCM, không tự tạo phòng chức năng. Nguồn có 208 cảnh báo nhập tổng hợp, gồm cảnh báo từng định danh/hoạt động và các ghi nhận nguồn lịch sử; 0 lỗi cấu trúc/cứng. Số cảnh báo không đồng nghĩa 208 giáo viên hay 208 xung đột.

Benchmark đọc workbook vừa nhập và xếp **riêng 9 lớp khối 8: 234 tiết môn**, khóa 738 tiết môn đã biết của khối 6/7/9. Không chạy lại bài toán 37 lớp toàn trường. Chọn FAST, 4 workers, seed 17, trần 15 giây, dùng lịch cũ làm gợi ý; cấu hình lịch buổi và thay đổi cần xác nhận đều được khai báo rõ. FAST ưu tiên nghiệm hợp lệ, không chứng minh tối ưu.

| Chế độ | Cần / đã xếp | Xung đột đã biết trong khối / liên khối | Tiết trống GV | Buổi GV | Thời gian giải (s) | Solver / hậu kiểm |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Sáng | 234 / 234 | 0 / 0 | 36 | 258 | 0.420 | FEASIBLE / INCOMPLETE |
| Sáng–chiều | 234 / 234 | 0 / 0 | 3 | 224 | 0.449 | FEASIBLE / INCOMPLETE |
| Phân ca theo lớp | 234 / 234 | 0 / 0 | 36 | 258 | 0.414 | FEASIBLE / INCOMPLETE |

Tiết trống/buổi GV đo trên lịch kết hợp khối đang xếp và các dòng khóa đã biết, theo cùng công thức V3.1.3. Hash lịch nền trước/sau bằng nhau trong cả ba lượt. 27 tiết đặc biệt của khối 8 và 84 tiết đặc biệt ngoài khối còn thiếu; lịch đầy đủ của trường chưa được xác minh. `school_conflicts = null` cho cả ba, không tuyên bố 0 xung đột toàn trường và không tuyên bố tối ưu toàn cục. Các kiểm thử synthetic đầy đủ có PASS/OPTIMAL riêng để kiểm tra proof policy; không phải nghiệm thu lịch thực.

## Bằng chứng và khả năng tái kiểm tra

| File | Nội dung |
| --- | --- |
| UNIFIED_RELEASE_EVIDENCE.json | Tổng kiểm thử, scope exclusions, runtime/SOURCE giữ nguyên |
| TIME_CONFLICT_REGRESSION.json | 206 bài Python, failures/errors, các bài ngoài phạm vi |
| UNIFIED_WORKBOOK_BROWSER.json | 16 kiểm tra UI workbook |
| SESSION_BROWSER_REGRESSION.json / SESSION_BROWSER.json / TIME_CONFLICT_BROWSER.json | 55 kiểm tra UI kế thừa, chạy lại |
| UNIFIED_LIBREOFFICE.json | SHA file hiện tại, mở/lưu/nhập lại; Windows Excel chưa test |
| UNIFIED_SOURCE_VALIDATION.json / UNIFIED_SOURCE_WARNINGS.xlsx | Kiểm tra 37 lớp và cảnh báo theo ô |
| UNIFIED_BENCHMARK.json / UNIFIED_SOLVE_*.json | Chỉ số và đầu vào/kết quả thực của ba chế độ |
| UNIFIED_TEMPLATE_UI.xlsx / UNIFIED_CURRENT_UI.xlsx / UNIFIED_IMPORT_ERRORS_UI.xlsx | File tải thực từ giao diện |
| UNIFIED_WORKBOOK_UI.png | Giao diện workbook |

Báo cáo A/B TIME_CONFLICT_BENCHMARK và historical_* là kết quả nền kế thừa, không được tính là benchmark workbook mới. Công cụ verify_time_conflict_evidence.py cũng đã kiểm tra lại 8 lịch đo lịch sử, 6 bản xuất UI hợp lệ và bản nháp/report có lỗi, không gọi CP.

Trước khi sử dụng thực tế: chạy START_WINDOWS.bat và TEST_WINDOWS.bat trên Windows x64, mở/lưu mẫu bằng Microsoft Excel, đối chiếu toàn bộ GV/PCCM/phòng/quy tắc hoạt động/lịch nền với nhà trường, nhập–xuất/khôi phục, xếp từng khối và hậu kiểm. Chỉ nghiệm thu sau khi các bước này được thực hiện trên dữ liệu đã xác minh.
