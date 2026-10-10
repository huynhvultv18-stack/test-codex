# SMART TKB THCS V3.1.3 — Unified Workbook Candidate

Một file Excel 11 sheet để chuẩn bị và nhập toàn bộ dữ liệu xếp TKB. **PRODUCTION READY = NO.** Bản này nằm trong thư mục riêng; SOURCE, baseline và main không bị ghi đè.

- Mẫu thật: [MAU_DU_LIEU_SMART_TKB_THCS.xlsx](MAU_DU_LIEU_SMART_TKB_THCS.xlsx).
- [Hướng dẫn nhập–xuất, xem trước và khôi phục](HUONG_DAN_SU_DUNG_WORKBOOK.md).
- [Hướng dẫn Windows ngoại tuyến](windows/WINDOWS_GUIDE.md); chạy START_WINDOWS.bat / TEST_WINDOWS.bat.
- [Báo cáo kiểm thử hiện tại](reports/UNIFIED_WORKBOOK_TEST_REPORT.md).
- [Workbook 37 lớp tham khảo, chưa nghiệm thu](data/DU_LIEU_PCCM_37_LOP_THAM_KHAO.xlsx).

Nhập workbook là giao dịch thay toàn bộ module sau xem trước và xác nhận; lỗi có sheet/dòng/cột và tải Excel báo cáo. Bản trước nhập được lưu trên trình duyệt để khôi phục. Mã GV chưa xác minh được cảnh báo, không tự gộp hoặc sửa. Ngày–buổi của lịch XEP và KHOA độc lập; 0 tiết là nghỉ.

Bộ giải grade-only CP-SAT V3.1.3 giữ nguyên thuật toán: warm start, tối ưu nhiều mục tiêu, tái tối ưu cục bộ, khóa các khối khác và hậu kiểm độc lập. Workbook không mang theo chứng minh tối ưu của lịch. Benchmark mới đọc đủ PCCM 37 lớp, xếp 9 lớp khối 8/234 tiết trong ba chế độ, giữ lịch các khối khác.

## Phát triển trên Linux

Python 3.12 với dependencies trong requirements.txt; có thể dùng môi trường đã chuẩn bị `/workspace/smart-tkb-tools/bin/python`. Chạy từ thư mục này:

```bash
python -m smart_tkb.server --port 8768
python tests/run_grade_regression.py
python tests/unified_benchmark.py
```

Kiểm thử browser dùng Node/Playwright và Chromium; đặt `TKB_BASE` theo cổng server và `TKB_PYTHON` theo Python có openpyxl. Môi trường cloud đã có Playwright tại `/opt/codex/runtimes/cua/lib/node_modules`:

```bash
NODE_PATH=/opt/codex/runtimes/cua/lib/node_modules TKB_BASE=http://127.0.0.1:8768 TKB_PYTHON=/workspace/smart-tkb-tools/bin/python node tests/workbook_browser.cjs
```

Các tests grade_browser.cjs, session_browser.cjs và time_conflict_browser.cjs tiếp tục kiểm tra chức năng cũ. 3 bài giải toàn trường 37 lớp trong regression được ghi rõ là ngoài phạm vi grade-only; không xóa hay vô hiệu hóa các kiểm tra cũ. Chưa kiểm thử runtime Windows hoặc Microsoft Excel thực tế.

## Truy vết baseline

[README của baseline V3.1.3 tối ưu](README_V313_OPTIMIZATION_BASELINE.md), các báo cáo A/B TIME_CONFLICT_BENCHMARK và báo cáo historical_* là lịch sử kế thừa, không phải lần benchmark workbook mới. Báo cáo hiện tại có tiền tố UNIFIED_; regression và browser cũ được chạy lại cho Candidate này và ghi lại receipt tương ứng.
