> **Tải bản đầy đủ cho Windows:** [SMART_TKB_THCS_V3_CANDIDATE.zip](https://raw.githubusercontent.com/huynhvultv18-stack/test-codex/smart-tkb-v3-candidate/SMART_TKB_V3/dist/SMART_TKB_THCS_V3_CANDIDATE.zip) · [SHA-256](dist/SMART_TKB_THCS_V3_CANDIDATE.zip.sha256).
>
> Thư mục GitHub này hiển thị mã nguồn và báo cáo. Runtime Python và wheel Windows nằm trong ZIP để tránh lưu trùng các binary lớn. Để chạy Windows ngoại tuyến, tải và giải nén **ZIP đầy đủ**, rồi mở `START_WINDOWS.bat`. Để phát triển từ source GitHub, cài `requirements.txt` theo hướng dẫn Linux/Python bên dưới.
>
> **PRODUCTION READY = NO.** Không có thay đổi Production.

# SMART TKB THCS V3.0 Candidate

Nâng cấp SOURCE V2.0 bằng backend Google OR-Tools CP-SAT và giao diện tiếng Việt ngoại tuyến. SOURCE giữ nguyên ở `SOURCE/`, có SHA-256 truy vết. Không ghi đè V2, không đổi localStorage V2, không nâng Production.

**PRODUCTION READY = NO.** Có nghiệm kỹ thuật cho phần PCCM đã phân công; chưa đủ dữ liệu để nghiệm thu lịch thực tế.

## Chạy

Windows x64: giải nén và mở `START_WINDOWS.bat`. Runtime Python và 12 wheel dependency đã kèm, cài và chạy không cần mạng. Xem `windows/WINDOWS_GUIDE.md`. Windows chưa được kiểm thử trực tiếp.

Linux/macOS để phát triển:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m smart_tkb.server --open
.venv/bin/python -m unittest discover -s tests -v
```

Ứng dụng là web cục bộ + Python, không phải HTML đơn tệp tự chạy CP-SAT. Máy chỉ lắng nghe loopback, kiểm Host/Origin/token, không dùng CDN hay API đám mây. Dữ liệu trong phiên trình duyệt và backup do người dùng tải; server không ghi đè SOURCE.

CLI:

```sh
python -m smart_tkb.cli SOURCE/PCCM_INPUT_CODEX_5_NHOM.xlsx --mode both --seconds 30 --out result.json
```

Phân ca CLI cần JSON config có `class_shifts`, ánh xạ đủ mã lớp sang `am` hoặc `pm`. Dùng `--previous`, `--scope` cho warm start/xếp lại cục bộ. Chế độ thực tế, tiết nghỉ/khóa/phòng cần đơn vị cung cấp; ví dụ benchmark không phải quyết định nghiệp vụ.

## Dữ liệu và bằng chứng

- `data/pccm_normalized.json`: 37 lớp, 64 GV tạm, 17 môn/phân môn, 555 phân công; 972 tiết có PCCM, 111 tiết đặc biệt chưa có GV, tổng nguồn 1.083.
- `reports/SOURCE_AUDIT.md`, `reports/PCCM_AUDIT.md`: khác biệt V2/V3 và trạng thái dữ liệu.
- `reports/BENCHMARK.md`, `reports/benchmark.json`: cấu hình, máy, thời gian, trạng thái, cận mục tiêu và số tiết. Không gọi FEASIBLE là tối ưu toàn cục.
- `reports/UNIT_TESTS.txt`, `reports/UI_TESTS.json`: kiểm thử thực thi; test mã nguồn và browser harness ở `tests/`.
- `data/EXAMPLE_BOTH_V3_BACKUP.json`, `data/EXAMPLE_MIXED_V3_BACKUP.json`: lịch kỹ thuật 37 lớp đã giải và hậu kiểm, có thể nhập bằng chức năng khôi phục V3; không phải lịch nghiệp vụ đã nghiệm thu.
- `reports/ALGORITHM.md`: mô hình và ý nghĩa các mục tiêu.
- `SHA256SUMS.txt`: hash các tệp đóng gói, trừ chính manifest và cache. File ZIP có hash riêng đặt cạnh ZIP.

Gói gồm mã nguồn, solver, UI, importer, validator độc lập, test, runtime và wheel Windows, hướng dẫn và báo cáo. Giữ Candidate đến khi kiểm thử offline và nghiệp vụ trên Windows thực tế.
