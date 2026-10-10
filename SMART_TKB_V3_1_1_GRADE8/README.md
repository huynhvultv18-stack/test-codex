# SMART TKB THCS V3.1.1 Grade8 Candidate

Nâng cấp tại chỗ từ V3.1 Optimized. Mặc định chỉ xếp **9 lớp khối 8, sáng 5 tiết, chiều 4 tiết, thứ Hai–thứ Bảy**. Lịch khối 6, 7, 9 là các hằng số khóa, không có biến xếp tiết trong mô hình CP-SAT. Giáo viên được đối chiếu bằng mã chính xác; phòng dùng chung và giới hạn buổi tính cả lịch khóa.

**GRADE8 SCHEDULING = PASS · CROSS-GRADE CONFLICT = BLOCKED · LOCKED GRADES = PASS.**

**DATA ACCEPTED = NO · WINDOWS ACCEPTED = NO · WINDOWS RUNTIME = UNTESTED · PRODUCTION READY = NO.**

Đã xếp 234/234 tiết môn học khối 8 trong mô phỏng kỹ thuật, giữ nguyên 738 tiết môn học của các khối khóa. 27 tiết đặc biệt khối 8 và 84 tiết đặc biệt lịch nền chưa có quy tắc; 26 mã giáo viên khối 8 chưa xác minh. Vì vậy chưa chứng nhận lịch thật hoặc 0 xung đột toàn trường. Mặc định ứng dụng chặn xếp khi lịch nền chưa đầy đủ; mô phỏng phải được chọn rõ và ghi nhãn giả định.

Windows 10/11 x64: giải nén toàn bộ ZIP, mở START_WINDOWS.bat. Python 3.12.10 và 12 wheel Windows có SHA-256 kèm sẵn, không cần Internet. Xem [hướng dẫn sử dụng](HUONG_DAN_SU_DUNG.md) và [cài đặt Windows](windows/WINDOWS_GUIDE.md).

Phát triển Linux:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m smart_tkb.server --open
.venv/bin/python tests/run_grade_regression.py
.venv/bin/python tests/verify_grade_evidence.py
```

Ứng dụng: http://127.0.0.1:8768. API và CLI công khai chỉ xếp một khối được chọn. Không có thao tác xếp toàn trường mặc định. Có ba chế độ, ngày học thực tế, số tiết sáng/chiều riêng, tiết đôi, phòng, lịch nghỉ, tiết cố định, SOFT/PREFERENCE, STRICT/SCENARIO, warm start/LNS và tái tối ưu cục bộ trong khối.

Benchmark chỉ theo khối:

```sh
python tests/grade_benchmark.py
python tests/verify_grade_evidence.py
```

Bộ hồi quy bỏ rõ 3 test cũ gọi giải toàn trường; thay bằng kiểm tra UNKNOWN/INFEASIBLE theo khối. Mã và bằng chứng baseline được giữ trong baseline_v3/, baseline_v31/ và reports/historical_v31_optimized/ để truy vết; không phải kết quả nghiệm thu phiên này. Không chạy các benchmark legacy 37 lớp cho quy trình mới.

Xem reports/GRADE8_BENCHMARK.md, GRADE8_REGRESSION.md, GRADE8_MISSING_DATA.json, GRADE8_ALGORITHM.md và GRADE8_ACCEPTANCE.json. SHA256SUMS.txt kiểm tra từng tệp; checksum ZIP ở tệp .zip.sha256 bên ngoài. Nhánh GitHub là Candidate riêng, không cập nhật main/Production.
