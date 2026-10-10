# Baseline bất biến và regression gốc

ZIP V3 gốc: SHA-256 `7374bde2f3ac23b4fdd1735e606c808b0dc9efc778beee44b4e10038b39a543f`, 62405988 bytes; CRC toàn bộ PASS. SOURCE HTML/XLSX V3.1 đối chiếu từng byte với ZIP V3: PASS. V3 gốc không thay đổi.

Chạy lại bản giải nén riêng: 23 unit tests PASS, 12 browser checks PASS; logs `V3_BASELINE_UNIT_RERUN.txt`, `V3_BASELINE_UI_TESTS.json`. Không dùng log cũ làm kết quả V3.1. `baseline_v3/smart_tkb/` sao chép mã V3 từ baseline bất biến, hai reference schedule kèm làm common warm start cho cả hai phiên bản.

5 sheet,37 lớp,64 GV,555 phân công,972 tiết và111 pending. GV015 40 tiết vượt30 ô chỉ sáng, cả V3/V3.1 INFEASIBLE. Các định danh chưa xác minh giữ nguyên. Main và V3 Candidate không bị ghi đè; V3.1 bàn giao nhánh riêng.
