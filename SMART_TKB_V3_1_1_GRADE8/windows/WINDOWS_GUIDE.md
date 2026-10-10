# Cài đặt Windows ngoại tuyến · V3.1.1 Grade8 Candidate

Windows 10/11 x64, Chrome hoặc Edge. Giải nén toàn bộ ZIP vào thư mục có quyền ghi, ví dụ D:\SMART_TKB_GRADE8. Không chạy bên trong ZIP hoặc Program Files.

Mở START_WINDOWS.bat. Script kiểm tra SHA-256, dùng Python 3.12.10 x64 kèm gói, cài 12 wheel từ windows/wheels bằng --no-index --require-hashes. Không cần Internet, Python cài sẵn hoặc quyền Administrator. Giữ cửa sổ lệnh mở; trình duyệt dùng http://127.0.0.1:8768.

Không mở SOURCE HTML bằng file:// để chạy CP-SAT. Nếu cổng đã dùng, chọn cổng khác: windows\runtime\python.exe -m smart_tkb.server --port 8778 --open. Dừng bằng Ctrl+C.

Đọc ../HUONG_DAN_SU_DUNG.md. Mặc định khối8,5sáng/4chiều/6ngày; khối6/7/9 khóa. Lịch nền kèm gói chỉ là kiểm thử kỹ thuật, còn 84 tiết đặc biệt thiếu quy tắc. Mặc định BLOCKED; muốn thử phải chọn mô phỏng có nhãn. Không chứng nhận 0 xung đột toàn trường khi thiếu nền.

TEST_WINDOWS.bat chạy tests/run_grade_regression.py, không tạo bài toán 37 lớp. Chạy khi ngắt mạng trên máy thật; thử nhập PCCM, lịch nền, giải khối8, warm/local, xuất CSV/Excel/JSON, mở lại và xác nhận hash khối khóa. Ghi biên bản Windows riêng trước nghiệm thu.

Python từ NuGet python3.12.10 của Python Software Foundation; provenance, license, wheel METADATA và SHA được giữ nguyên từ baseline. Xem PYTHON_PROVENANCE.json và THIRD_PARTY.md. Thư viện runtime/wheel đã đối chiếu byte và dependency ngoại tuyến trên Linux; chưa chạy trên Windows.

**WINDOWS RUNTIME=UNTESTED · WINDOWS ACCEPTED=NO · DATA ACCEPTED=NO · PRODUCTION READY=NO.**
