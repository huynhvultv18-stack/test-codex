# SMART TKB THCS V3.1 Optimization Candidate

Nâng cấp trên V3 Candidate bất biến: CP-SAT, warm start/LNS, tối ưu số buổi giáo viên và tiêu chí môn học có cấu hình. Có mã nguồn, giao diện tiếng Việt, bộ nhập 5 sheet PCCM, hậu kiểm độc lập và benchmark so sánh. Không sửa SOURCE hay định danh giáo viên.

**DATA ACCEPTED = NO · WINDOWS ACCEPTED = NO · PRODUCTION READY = NO.**

Windows x64: giải nén toàn bộ ZIP, mở `START_WINDOWS.bat`. Python 3.12 x64 và các wheel đã kèm để cài ngoại tuyến. Xem `windows/WINDOWS_GUIDE.md`. Chưa chạy trên Windows thực tế.

Phát triển trên Linux/macOS:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m smart_tkb.server --open
.venv/bin/python -m unittest discover -s tests -v
```

UI chạy tại http://127.0.0.1:8768, không dùng CDN hay dịch vụ mạng. Chỉ lắng nghe loopback; kiểm Host, Origin và token phiên. JSON V2/V3 được nhập vào trạng thái V3.1 riêng, không ghi đè localStorage V3. Lịch nhập JSON/CSV/Excel đều được hậu kiểm, tính lại chỉ số; không kế thừa chứng minh tối ưu từ tệp nhập.

972 tiết có PCCM, 111 tiết đặc biệt chưa xác minh. STRICT giữ các hoạt động thiếu quy tắc ở PENDING. SCENARIO cần chọn từng activity_id và nhãn giả định; tiết mô phỏng không được cộng vào số tiết đã xác minh. Không tự tách nhãn ghép CC/SHCN, gán giáo viên chủ nhiệm, phòng hay giáo viên giả. Xem `reports/SPECIAL_ACTIVITIES.md`.

Cấu hình môn học mặc định không thêm quy định chuyên môn: `subject_hard_limits` là HARD opt-in; `subject_rules` là SOFT theo môn/khối; `preferences` và tiết ưu tiên môn là PREFERENCE. Bật/tắt và trọng số mục tiêu trong UI, cấu hình chi tiết qua JSON. Công thức và cách đọc chứng minh ở `reports/ALGORITHM.md`.

```sh
python -m smart_tkb.cli SOURCE/PCCM_INPUT_CODEX_5_NHOM.xlsx --mode both --seconds 30 --out result.json
python tests/fair_benchmark.py
python tests/extended_benchmark.py
```

Phân ca cần `class_shifts` trong JSON CLI; không tự chọn ca thực tế. `--previous` dùng lịch cũ, `--scope` khóa ngoài các lớp/GV được chọn. Benchmark phân ca xen kẽ là fixture kỹ thuật.

Đọc `reports/BENCHMARK.md`, `reports/FAIR_BENCHMARK.json`, `reports/REGRESSION.md` và các log thực thi. Baseline V3 có trong `baseline_v3/` để chạy lại so sánh; ZIP V3 gốc không bị thay đổi. `SHA256SUMS.txt` kiểm tra nội dung; SHA của ZIP nằm ở tệp bên cạnh ZIP. 64 định danh GV và quy tắc hoạt động cần nhà trường xác minh trước nghiệm thu.

Bản mã nguồn trên GitHub không nhân đôi runtime/wheel dung lượng lớn; tải ZIP Candidate trong `dist/` để chạy Windows ngoại tuyến đầy đủ.
