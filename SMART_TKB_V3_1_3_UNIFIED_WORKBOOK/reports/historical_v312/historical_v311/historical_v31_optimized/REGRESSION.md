# REGRESSION · Optimized Candidate

REGRESSION = PASS trên Linux; không còn CRITICAL/HIGH đã biết chưa xử lý trong phạm vi rà soát. WINDOWS RUNTIME = UNTESTED.

- Baseline V3.1 đã chạy lại45 unit/20 browser PASS: BASELINE_UNIT_RERUN.txt, BASELINE_BROWSER_RERUN.txt.
- Bản sửa71 unit PASS (45 gốc +26 audit),28 browser checks PASS (20 gốc +8 audit). UNIT_REGRESSION.txt, UI_TESTS.json, UI_AUDIT_TESTS.json; không xóa test hoặc tắt assertion.
- 26 lượt A/B37 lớp được hậu kiểm bằng verifier hiện tại, SHA đầu vào và metrics tính lại: AB_INDEPENDENT_VERIFICATION.json PASS. 24 lịch972/972,0 conflicts/0 gaps; morning2 trường hợp INFEASIBLE với proof40>30.
- Unit cover HARD GV/lớp/phòng/PCCM/ca/nghỉ/khóa/tiết đôi/giới hạn; status OPTIMAL nhỏ, FEASIBLE37, INFEASIBLE proof/core, UNKNOWN không fake lịch; warm hợp lệ/không hợp lệ, local freeze/khóa mâu thuẫn, objective/bound/weight/grade/soft/hard/prefs.
- Audit: forged marker, source inventory bỏ/sửa, pending totals, fractional/bool time, malformed list/row, CSV literal formula/reversible ID, Excel fraction/columns, finite config, approved rule note/missing/conflict, không mutate SOURCE, dòng tổng thiếu/trùng.
- Integration/browser: Excel nguồn5 sheet, JSON V2/V3/V3.1, backup atomic khi mạng lỗi, CSV/XLSX roundtrip, ca từng lớp, live solve và live SCENARIO; giữ collective/fixed rules; bảng buổi/biểu đồ/lịch/so sánh, tiến độ,6 mục tiêu; mobile/tablet/desktop.
- Host/Origin/CSRF và CSP self, không có request ngoại mạng, không có native browser errors, JSON NaN bị từ chối. Không có nghiệm thì không hiển thị0 xung đột.
- Extended37: STRICT111 pending nguồn; SCENARIO chỉ fixture với lựa chọn74activity_ids/111 tiết và nhãn giả định, both/mixed xếp972+111 kỹ thuật; local37 ngoàiC06A01 giữ0 changes và global proof=false. EXTENDED_BENCHMARK.json.
- Offline Windows dependency resolution win_amd64/cp312 với no-index/hash đạt; runtime/wheel byte kiểm với baseline. WINDOWS_INTEGRITY.json và WINDOWS_OFFLINE_RESOLUTION.json. Không chạy PE/Windows batch trên Linux.

PACKAGING = PASS: ZIP đã giải nén vào thư mục tạm mới, chạy lại71 unit và28 browser checks đạt. PACKAGE_EXTRACTED_UNIT_TESTS.txt, PACKAGE_EXTRACTED_BROWSER_TESTS.txt, PACKAGE_EXTRACTED_BROWSER_AUDIT.txt, PACKAGE_EXTRACTED_MANIFEST.txt; 1394 release files kiểm SHA. Final reports thêm sau lượt kiểm tra không sửa runtime/code đã test. Không dùng log PACKAGE_UNIT_TESTS cũ ở historical_v31 như nghiệm thu hiện tại.

DATA ACCEPTED = NO · WINDOWS ACCEPTED = NO · PRODUCTION READY = NO.
