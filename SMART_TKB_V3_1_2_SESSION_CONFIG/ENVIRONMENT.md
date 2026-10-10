# Môi trường phát triển đám mây

Dùng checkout hiện có `/workspace/test-codex`; không tạo worktree nếu người dùng chưa yêu cầu. Bản nâng cấp nằm trong `SMART_TKB_V3_1_2_SESSION_CONFIG` trên nhánh Candidate. Python virtualenv hiện có `/workspace/smart-tkb-tools` với OR-Tools9.15.6755 và openpyxl3.1.5; Node24, Chromium/Playwright của môi trường.

Từ thư mục mã nguồn V3.1.2, chạy `/workspace/smart-tkb-tools/bin/python -m smart_tkb.server --port 8768`. Tiến trình cần khởi động lại ở phiên mới. Kiểm tra nội bộ GET `/api/bootstrap`:9lớp,234tiết PCCM,41ô/lớp,3buổi nghỉ/lớp; HTTP200 và CSRF token trong phiên. Không công bố địa chỉ loopback như preview cho người dùng.

Chạy `tests/run_grade_regression.py`:121kiểm thử, không tạo mô hình37lớp. Browser dùng `NODE_PATH=/opt/codex/runtimes/cua/lib/node_modules`, `TKB_BASE` theo cổng server, Chromium `/usr/bin/chromium`. Benchmark riêng `tests/session_benchmark.py` chạy tuần tự để đo thời gian. Không cần Docker/VPN/credential mới. Native Git HTTPS dùng xác thực proxy sẵn có; không yêu cầu hoặc in token.

Cấu hình khởi động lưu trong draft môi trường bằng skill cloud-environment-onboarding:setup. Lưu draft không phải xuất bản snapshot; chưa xác nhận khôi phục phiên mới hoặc chạy Windows thật.
