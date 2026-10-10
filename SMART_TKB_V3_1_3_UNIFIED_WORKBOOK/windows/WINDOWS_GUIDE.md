# Windows x64 — V3.1.3 Unified Workbook Candidate

Giải nén toàn bộ ZIP vào thư mục riêng. Chạy `START_WINDOWS.bat`; Python 3.12 và các wheel đã đi kèm, không cần Internet. Không dùng thư mục baseline để giải nén bản mới. Chạy `TEST_WINDOWS.bat` để kiểm tra manifest SHA-256 và kiểm thử Python trước khi sử dụng.

Trong giao diện, mở **Dữ liệu PCCM → TẢI FILE EXCEL MẪU TỔNG HỢP**. Điền 11 sheet theo `HUONG_DAN_SU_DUNG_WORKBOOK.md`, nhập workbook, xem lỗi/cảnh báo và xác nhận. Nếu nhập nhầm, chọn **Khôi phục trước lần nhập gần nhất**; tải bản sao JSON trước khi xóa bộ nhớ trình duyệt.

Giữ cùng cổng khi mở lại để truy cập dữ liệu đã lưu trong trình duyệt. Bản khôi phục gần nhất nằm ở cùng trình duyệt/cổng. Dữ liệu không tự ghi vào SOURCE. File Excel cần lưu định dạng `.xlsx`, không bật macro và không dùng công thức trong ô dữ liệu.

**PRODUCTION READY = NO.** Đã kiểm thử trên Linux và mở/lưu workbook bằng LibreOffice; chưa chạy runtime Windows hoặc Microsoft Excel thực tế. Khi nghiệm thu trên máy Windows của trường, cần chạy batch, tải mẫu từ UI, mở/lưu bằng Excel, nhập–xuất lại 11 sheet, thử khôi phục và hậu kiểm lịch liên khối.

## Hướng dẫn kỹ thuật nền kế thừa

# Cài đặt Windows ngoại tuyến · V3.1.3 Optimization + Conflict Candidate

Windows 10/11 x64, Chrome hoặc Edge. Giải nén toàn bộ ZIP vào thư mục có quyền ghi, ví dụ D:\SMART_TKB_V313. Không chạy bên trong ZIP hoặc Program Files.

Mở START_WINDOWS.bat. Script kiểm tra SHA-256, dùng Python 3.12.10 x64 kèm gói, cài 12 wheel từ windows/wheels bằng --no-index --require-hashes. Không cần Internet, Python cài sẵn hoặc quyền Administrator. Giữ cửa sổ lệnh mở; trình duyệt dùng http://127.0.0.1:8768.

Không mở SOURCE HTML bằng file:// để chạy CP-SAT. Nếu cổng đã dùng, chọn cổng khác: windows\runtime\python.exe -m smart_tkb.server --port 8778 --open. Dừng bằng Ctrl+C.

Đọc ../HUONG_DAN_SU_DUNG.md. Mặc định khối8,41ô/9buổi mỗi lớp theo bảng trong hướng dẫn; chiều thứBa/thứNăm/thứBảy0tiết=nghỉ; khối6/7/9 khóa. Lịch nền kèm gói chỉ là kiểm thử kỹ thuật, còn 84 tiết đặc biệt thiếu quy tắc. Mặc định BLOCKED; muốn thử phải chọn mô phỏng có nhãn. Không chứng nhận 0 xung đột toàn trường khi thiếu nền.

TEST_WINDOWS.bat chạy tests/run_grade_regression.py, không tạo bài toán 37 lớp. Chạy khi ngắt mạng trên máy thật; thử nhập PCCM, lịch nền, giải khối8, warm/local, xuất CSV/Excel/JSON, mở lại và xác nhận hash khối khóa. Ghi biên bản Windows riêng trước nghiệm thu.

Python từ NuGet python3.12.10 của Python Software Foundation; provenance, license, wheel METADATA và SHA được giữ nguyên từ baseline. Xem PYTHON_PROVENANCE.json và THIRD_PARTY.md. Thư viện runtime/wheel đã đối chiếu byte và dependency ngoại tuyến trên Linux; chưa chạy trên Windows.

**WINDOWS RUNTIME=UNTESTED · WINDOWS ACCEPTED=NO · DATA ACCEPTED=NO · PRODUCTION READY=NO.**

Kiểm thử Windows thêm: sáng0,chiều0,cả ngày0;1..5 tiết; lịch khác từng lớp; copy/lưu/khôi phục; xác nhận/hủy sau đổi lịch; Excel LICH_BUOI/CSV CALENDAR và Chủ nhật. Chưa thực hiện những kiểm thử này trên máy Windows thật.

V3.1.3: thử cả FAST/BALANCED/PROVE_OPTIMAL; đồng giảng/tập thể, chờ thực tế/PROXY, hậu kiểm PASS/FAIL/INCOMPLETE/STALE; chỉnh tay gây trùng liên khối rồi sửa; Excel lỗi và in; PASS cũ phải hết hiệu lực sau sửa/nhập dữ liệu, lưu nháp lỗi và mở lại; xác nhận lỗi phải bị chặn. Chưa có biên bản các bước này trên Windows thật.
