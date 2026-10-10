# SMART TKB THCS V3.1.2 Session Config Candidate

Cấu hình từng ngày, buổi và số tiết cho khối/lớp; **0 tiết=NGHỈ**. Nâng cấp trực tiếp từ V3.1.1; SOURCE và baseline giữ nguyên. Chỉ giải khối được chọn, dùng lịch các khối khác làm ràng buộc bận bất biến.

Khối8 mặc định: sáng5/5/5/5/5/4; chiều4/0/4/0/4/0 (thứHai..thứBảy). **41 ô,9buổi mỗi lớp**. Chủ nhật mặc định0/0, có thể bật. Hỗ trợ3chế độ học, chỉnh/copy từng lớp, áp dụng cả khối, lưu/khôi phục/JSON; CP-SAT, warm start, best verified incumbent và xếp lại cục bộ. Đổi số tiết ảnh hưởng lịch hiện tại cần xác nhận trong ứng dụng, vẫn giữ tiết khóa.

Windows ngoại tuyến: tải ZIP đầy đủ, giải nén, mở `START_WINDOWS.bat`. Gói có Python3.12.10 x64 và12wheel với SHA; không cần Internet/Admin. Xem [Hướng dẫn sử dụng](HUONG_DAN_SU_DUNG.md) và [Windows](windows/WINDOWS_GUIDE.md). Mã nguồn GitHub không kèm runtime/wheels; dùng ZIP trong `dist/` để chạy ngoại tuyến.

Linux phát triển:

```bash
python3 -m venv /workspace/smart-tkb-tools
/workspace/smart-tkb-tools/bin/python -m pip install -r requirements.txt
/workspace/smart-tkb-tools/bin/python -m smart_tkb.server --port 8768
/workspace/smart-tkb-tools/bin/python tests/run_grade_regression.py
```

Trình duyệt phát triển: khởi động server, cài Playwright/Chromium hoặc dùng các công cụ có sẵn trong môi trường; chạy `tests/grade_browser.cjs` (20hồi quy) và `tests/session_browser.cjs` (16lịch buổi). Đặt `TKB_BASE` theo cổng, `NODE_PATH` theo thư mục Playwright. `tests/session_benchmark.py` chỉ giải khối8; `tests/verify_session_evidence.py` hậu kiểm, không giải. Không chạy các benchmark toàn trường lịch sử để thay kiểm thử hiện tại.

Bằng chứng hiện tại: [benchmark](reports/SESSION_BENCHMARK.md), [hồi quy](reports/SESSION_REGRESSION.md), [thuật toán](reports/SESSION_ALGORITHM.md), [nghiệm thu](reports/SESSION_ACCEPTANCE.json), [kiểm tra độc lập](reports/SESSION_INDEPENDENT_VERIFICATION.json). Báo cáo V3.1.1/phiên bản cũ nằm trong `reports/historical_v311`, giữ để truy xuất; không phải nghiệm thu V3.1.2. Ba kiểm thử legacy tạo mô hình37lớp được loại khỏi runner riêng khối, tên/lý do ghi rõ trong báo cáo; giữ nguyên test/assertion và thay bằng kiểm thử UNKNOWN/công suất khối8 tương ứng.

Nguồn37lớp được đọc/kiểm tra đầy đủ; khối8 có234tiết môn học,27tiết đặc biệt PENDING và26mãGV chưa xác minh. Lịch nền738tiết vẫn thiếu84tiết đặc biệt. Mặc định giải BLOCKED; muốn kiểm thử có điều kiện phải bật mô phỏng và ghi nhãn. Không tự sửa mã GV, không coi lịch chưa biết là giờ rảnh, không báo0xungđột toàn trường khi thiếu nền.

**DATA ACCEPTED=NO · WINDOWS ACCEPTED=NO · PRODUCTION READY=NO.** Nghiệm FEASIBLE qua hậu kiểm không là chứng minh tối ưu toàn cục. Windows thực tế cần biên bản nghiệm thu riêng.
