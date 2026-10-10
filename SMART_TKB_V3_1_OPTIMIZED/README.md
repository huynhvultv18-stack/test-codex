# SMART TKB THCS V3.1 Optimized Candidate

Bản rà soát và sửa tại chỗ trên V3.1 đã bàn giao: Google OR-Tools CP-SAT, UI tiếng Việt, 5-sheet PCCM import, independent verifier, warm start/LNS, xếp lại cục bộ, JSON/CSV/Excel. SOURCE HTML/XLSX và các Candidate gốc giữ nguyên.

**DATA ACCEPTED = NO · WINDOWS ACCEPTED = NO · PRODUCTION READY = NO. WINDOWS RUNTIME = UNTESTED.**

Windows 10/11 x64: giải nén toàn bộ ZIP vào thư mục có quyền ghi, mở START_WINDOWS.bat. Python 3.12.10 và 12 wheel ghim SHA-256 kèm sẵn, không cần Internet. Xem windows/WINDOWS_GUIDE.md; lần đầu cần kiểm thử trên máy Windows thật.

Linux development:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m smart_tkb.server --open
.venv/bin/python -m unittest discover -s tests -v
```

Ứng dụng chạy tại http://127.0.0.1:8768. Không CDN, telemetry hoặc cloud solver. Nhập PCCM bằng nút Excel PCCM, nhập lịch bằng nút CSV/Excel lịch; JSON V2/V3/V3.1 được chuyển sang trạng thái Optimized riêng. Lịch nhập được hậu kiểm và tính lại chỉ số, không kế thừa chứng minh tối ưu.

Nguồn có 37 lớp, 64 ID giáo viên cần xác minh, 972 tiết PCCM và 111 tiết đặc biệt PENDING. STRICT chỉ dùng quy tắc xác minh/phê duyệt rõ; SCENARIO cần chọn từng hoạt động và nhãn giả định. Không tự tách CC/SHCN hoặc gán GV/phòng/tiết cố định. Ba chế độ được hỗ trợ, nhưng chỉ sáng với 6 ngày × 5 tiết vô nghiệm vì GV015 có 40 tiết. Ca phân lớp trong benchmark là fixture xen kẽ, không phải ca đã phê duyệt.

Đọc reports/FULL_AUDIT.md, BUGFIX.md, OPTIMIZATION.md, AB_BENCHMARK.md, REGRESSION.md và ACCEPTANCE.json. Lịch tốt ban đầu là warm start hữu ích; FEASIBLE không phải tối ưu toàn cục, và bản sửa không tốt hơn baseline ở mọi seed. Không dùng PASS lịch sử trong reports/historical_v31 làm kết quả lần này.

Tái kiểm benchmark (Linux, khoảng nhiều phút):

```sh
python tests/ab_audit_benchmark.py
python tests/ab_lns_benchmark.py
python tests/verify_ab_evidence.py
python tests/extended_benchmark.py
```

Baseline V3.1 code nằm ở baseline_v31/ chỉ cho A/B; baseline_v3/ là lịch sử V3. Browser development cần Node, Playwright và Chromium (không phải dependency chạy Windows). Có tests/browser.cjs và browser_audit.cjs; dùng TKB_BASE để đổi cổng. CLI hỗ trợ --config, --previous, --scope; mode mixed cần class_shifts rõ từng lớp.

SHA256SUMS.txt kiểm tra nội dung; checksum ZIP ở tệp .zip.sha256 bên ngoài. GitHub chứa source và reports; ZIP dist chứa runtime/wheel Windows đầy đủ.
