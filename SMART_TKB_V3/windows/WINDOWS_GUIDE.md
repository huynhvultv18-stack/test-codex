# Chạy ngoại tuyến trên Windows

**CANDIDATE ONLY — PRODUCTION READY = NO.** Chưa thực thi hoặc nghiệm thu trên máy Windows thực tế trong đợt bàn giao này.

1. Dùng Windows 10/11 **64-bit**, Chrome hoặc Edge. Giải nén toàn bộ ZIP vào một thư mục có quyền ghi, ví dụ `D:\SMART_TKB_V3`. Không chạy trực tiếp bên trong ZIP. Không để thư mục trong Program Files.
2. Mở `START_WINDOWS.bat`. Gói đã kèm Python 3.12.10 x64 của Python Software Foundation, OR-Tools và toàn bộ dependency Windows dưới dạng wheel. Không cần Python cài sẵn, quyền Administrator hoặc Internet. Lần đầu script cài thư viện từ `windows/wheels` vào Python đi kèm, có kiểm tra SHA-256; các lần sau pip kiểm tra các dependency đã có.
3. Trình duyệt mở ứng dụng trên máy tại cổng 8768. Cửa sổ lệnh phải còn mở để bộ giải hoạt động. Không mở HTML V3 bằng `file://`, vì CP-SAT chạy trong tiến trình Python.
4. Để dừng, nhấn Ctrl+C trong cửa sổ lệnh. Đóng trang trình duyệt không tự dừng Python. Nếu cổng 8768 đã dùng, đóng phiên SMART TKB của chính bạn hoặc chạy `windows\runtime\python.exe -m smart_tkb.server --port 8778 --open` từ thư mục gốc. Không tắt dịch vụ khác để chiếm cổng.
5. Ngắt mạng và chạy `TEST_WINDOWS.bat`, kiểm tra toàn bộ test thực sự chạy. Thử nhập Excel, giải, in, xuất CSV, sao lưu/khôi phục và xếp lại cục bộ trên máy thật. Ghi kết quả vào một bản báo cáo nghiệm thu riêng.

Nếu Windows Defender/SmartScreen yêu cầu kiểm tra, đối chiếu SHA-256 được bàn giao và chính sách của đơn vị; không tắt cơ chế bảo vệ Windows. Đây là mã Python/batch mở, không có trình cài EXE đã ký của đơn vị.

## Luồng sử dụng

- Gói mở sẵn workbook SOURCE để kiểm thử. `Dữ liệu PCCM` → nhập Excel theo đúng 5 sheet hiện có; các dòng tổng được đối chiếu, không biến thành phân công.
- Kiểm tra 69 cảnh báo: 64 mã GV tạm, 3 ký hiệu L/H/S, 111 tiết đặc biệt thiếu phân công, 34 ô nguồn đánh dấu trùng giờ. Chưa có họ tên đầy đủ; không tự gộp giáo viên, đặc biệt GV015 có 40 tiết.
- `Ràng buộc & tối ưu` → chọn chế độ, ngày, tiết, giới hạn/buổi. `Phân ca` phải chọn ca từng lớp ở Dữ liệu. Gói không quyết định ca học thực tế cho nhà trường.
- Bảng PCCM cho phép đặt **số cặp tiết đôi**, giữ nguyên tổng tiết, và danh sách phòng hợp lệ. JSON bổ sung cấu hình `rooms`, `unavailable`, `fixed`, `preferences`. Ngày/tiết đếm từ 0, ca `am`/`pm`. Nguyện vọng là ô muốn tránh, không phải lịch nghỉ bắt buộc.
- Xếp lịch; không có lịch một phần nếu không tìm được nghiệm. `INFEASIBLE` cần xem nguyên nhân; `UNKNOWN` có thể cần tăng thời gian. Chỉ xuất lịch còn hiện hành so với cấu hình/dữ liệu.
- `Dùng lịch hiện tại` cung cấp warm start. `Khóa ngoài phạm vi` giữ nguyên từng bloc ngoài các mã lớp/GV nhập; nếu các khóa mới mâu thuẫn, không tự bỏ khóa.
- Mọi dữ liệu lưu dưới key V3 riêng. V2 không bị ghi đè. Chuyển V2 bằng file sao lưu JSON; lịch V2 cũ không tự được công nhận hợp lệ. Luôn xuất backup JSON trước khi xóa dữ liệu trình duyệt hoặc đổi máy/cổng.

## Giới hạn cần nghiệm thu

Tổng 1.083 ô lịch nguồn gồm 972 tiết có PCCM và 111 tiết đặc biệt chưa phân công. Gói chỉ giải 972 tiết đã có giáo viên; **không phải lịch đầy đủ của trường**. Cần PCCM bổ sung các hoạt động, định danh đầy đủ, phòng thực tế, ngày nghỉ, tiết cố định, quy định tiết đôi và giới hạn/buổi trước khi nghiệm thu. Bộ giải hỗ trợ khi dữ liệu được cung cấp; không tự suy ra các yêu cầu này từ ảnh.

Benchmark 37 lớp phân ca dùng các lớp xen kẽ sáng/chiều để kiểm thử kỹ thuật, không phải ca học đã phê duyệt. Hai buổi được giả định không chồng giờ; phiên bản này chưa mô hình phút bắt đầu/kết thúc, thời gian di chuyển giữa cơ sở, dạy đồng thời nhiều lớp hoặc đồng giảng nhiều GV trong một tiết.

## Nguồn runtime và giấy phép

Python lấy từ package `python` 3.12.10 của **Python Software Foundation** trên NuGet; SHA-512 đã đối chiếu catalog chính thức. Xem `PYTHON_PROVENANCE.json` và `runtime/LICENSE.txt`. OR-Tools 9.15.6755 và dependency lấy qua PyPI bằng TLS, giữ giấy phép/METADATA trong wheel. Xem `THIRD_PARTY.md`. Python 3.12.10 là bản Windows được ghim để phù hợp ABI cp312; đánh giá cập nhật bảo mật trước triển khai chính thức.
