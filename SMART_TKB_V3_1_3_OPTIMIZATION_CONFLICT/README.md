# SMART TKB THCS V3.1.3 Optimization + Conflict Candidate

Tối ưu thời gian giáo viên bằng Google OR-Tools CP-SAT và hậu kiểm GV/lớp/phòng sau xếp, tối ưu, chỉnh tay, nhập, lưu và xác nhận. Chỉ giải khối chọn; các khối nền giữ nguyên. Giữ lịch buổi V3.1.2: 0 tiết = NGHỈ, lịch từng lớp/ngày/buổi, cả ba chế độ học.

FAST / BALANCED / PROVE_OPTIMAL; ưu tiên từ điển tiết trống, buổi, ngày, chờ hai buổi, cụm tiết và chất lượng môn. Warm start, LNS, neighborhood lớp/GV/ngày/buổi, multi-seed. Chỉ ghi chứng minh CP OPTIMAL sau hậu kiểm; khóa incumbent được ghi riêng có điều kiện. Không tuyên bố tối ưu toàn trường.

Hậu kiểm PASS / FAIL / INCOMPLETE / STALE gắn SHA-256 với dữ liệu/cấu hình/lịch hiện hành. FAIL chặn xác nhận; INCOMPLETE chỉ bản nháp. Báo cáo lỗi có định vị, Excel và in; bảng thời gian từng GV ghi rõ REAL_MINUTES hoặc PROXY.

Windows ngoại tuyến: tải ZIP đầy đủ trong `dist`, giải nén riêng rồi mở `START_WINDOWS.bat`. Có Python3.12.10 x64, 12wheel và khóa SHA-256; source GitHub không chứa runtime/wheels. [Hướng dẫn sử dụng](HUONG_DAN_SU_DUNG.md), [Windows](windows/WINDOWS_GUIDE.md), [thuật toán](reports/TIME_CONFLICT_ALGORITHM.md), [benchmark](reports/TIME_CONFLICT_BENCHMARK.md), [hồi quy](reports/TIME_CONFLICT_REGRESSION.json), [nghiệm thu](reports/TIME_CONFLICT_ACCEPTANCE.json).

Phát triển Linux:

```bash
/workspace/smart-tkb-tools/bin/python -m smart_tkb.server --port 8768
/workspace/smart-tkb-tools/bin/python tests/run_grade_regression.py
```

Python mới: tạo venv và cài `requirements.txt`. Browser dùng Playwright + Chromium, chạy tuần tự `tests/grade_browser.cjs`, `tests/session_browser.cjs`, `tests/time_conflict_browser.cjs`. Benchmark A/B chỉ khối8, cần một bản giải nén V3.1.2 riêng; không chạy lại baseline gốc hoặc các benchmark 37 lớp lịch sử.

Nguồn có37lớp; khối8 có234tiết môn,27tiết đặc biệt PENDING,26mãGV chưa xác minh. Nền khóa738tiết vẫn thiếu84tiết đặc biệt. Mặc định BLOCKED; mô phỏng có nhãn chỉ thử kỹ thuật INCOMPLETE, không nghiệm thu lịch thực tế. SOURCE, ZIP/baseline V3.1.2 và main giữ nguyên. Báo cáo cũ trong `reports/historical_v312` chỉ để truy xuất.

**DATA ACCEPTED = NO · WINDOWS ACCEPTED = NO · PRODUCTION READY = NO.**
