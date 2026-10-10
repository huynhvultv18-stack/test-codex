# SMART TKB V3.1.3 — workbook tổng hợp

**Candidate; PRODUCTION READY = NO.** Mã nguồn và SOURCE cũ giữ nguyên trong baseline; bản này chạy trong thư mục riêng.

## 1. Khởi động và tải mẫu

Trên Windows x64, giải nén toàn bộ ZIP rồi chạy `START_WINDOWS.bat`. Vào **Dữ liệu PCCM**, chọn **TẢI FILE EXCEL MẪU TỔNG HỢP**. Đây là file `MAU_DU_LIEU_SMART_TKB_THCS.xlsx` thật gồm đúng 11 sheet; không cần tải nhiều mẫu dữ liệu.

Nếu đã có dữ liệu trong ứng dụng, chọn **Tải dữ liệu hiện có để chỉnh sửa**. File xuất có cùng cấu trúc mẫu, bảo toàn mã và truy vết, lịch nền, lịch buổi, CP-SAT và các tùy chọn. Lịch đang xem và chứng minh tối ưu không nằm trong workbook dữ liệu: lưu bản nháp JSON hoặc xuất Excel lịch khi cần giữ chúng.

## 2. Điền các sheet

Dòng 1 là tiêu đề; dữ liệu chính thức bắt đầu từ dòng 2. Ví dụ chỉ ở `HUONG_DAN` và không được bộ nhập coi là dữ liệu. Không đổi tên sheet/cột hoặc chèn công thức. Các mã là chuỗi, phân biệt hoa/thường, không có khoảng trắng đầu/cuối; dùng chữ ASCII, số, `_ . : / -`. Không gộp giáo viên theo nhãn tên.

| Sheet | Nội dung |
| --- | --- |
| HUONG_DAN | Cách dùng, ví dụ và metadata nguồn; giữ nguyên metadata khi sửa file xuất |
| DANH_SACH_LOP | Mã lớp, tên, khối 6..9, ca Sáng/Chiều |
| DANH_SACH_GV | Mã GV, nhãn, họ tên xác minh, VERIFIED/REVIEW/UNVERIFIED |
| DANH_MUC_MON | Mã môn đầy đủ và gốc; ví dụ M01:NONE, gốc M01, phân môn NONE |
| PCCM | Mã phân công, lớp/GV/môn, số tiết nguyên dương, số cặp đôi và phòng cho phép |
| NGAY_BUOI_TIET | Lịch chung `*` và lịch từng lớp, đủ 7 ngày; sáng/chiều riêng, 0 = nghỉ |
| TKB_LIEN_KHOI | Lịch nền các khối, gồm mã phân công, lớp/GV/môn/ngày/buổi/tiết/phòng |
| PHONG_HOC | Mã phòng dùng chung, tên, loại và thông tin thêm |
| RANG_BUOC | Cấu hình CP-SAT, lịch nghỉ, tiết cố định, quy tắc môn HARD/SOFT |
| TIET_DAC_BIET | Hoạt động, số tiết, GV/quy tắc/xác minh; không tự suy ra GV chủ nhiệm |
| NGUYEN_VONG_GV | Các ô muốn tránh, trọng số 0..1000; nguyện vọng là SOFT |

Giáo viên VERIFIED chỉ khi đã xác minh và có họ tên; thiếu xác minh vẫn cảnh báo, không tự đổi mã. Môn có phân môn dùng mã đầy đủ, ví dụ `M13:L`; các quy tắc môn dùng mã gốc `M13`. Phòng cho phép và GV đồng giảng trong PCCM dùng danh sách mã cách nhau dấu phẩy, **không có khoảng trắng**. Một cặp đôi chiếm 2 tiết; số cặp không vượt một nửa tổng tiết.

Cột JSON bổ sung bảo toàn thông tin nguồn và tùy chọn nâng cao. Để trống khi thêm dòng mới; giữ nguyên khi sửa file xuất. JSON không được ghi đè các cột chính. Các tổng số tiết của dữ liệu/lớp được tính lại từ các dòng nhập; khi khác tổng nguồn cũ, xem trước sẽ cảnh báo thay đổi, không sửa SOURCE.

## 3. Lịch ngày–buổi

`XEP` là lịch chuẩn bị để xếp; `KHOA` là lịch buổi của lịch nền. Hai phạm vi độc lập. Chỉnh XEP không tự sửa KHOA hoặc dịch chuyển tiết đã khóa. Lịch riêng của lớp ngoài khối đang chọn được lưu để dùng khi chuyển khối; chỉ khối đang chọn có biến CP-SAT. `*` là lịch chung; thêm đủ 7 dòng cho lớp khi muốn chỉnh riêng. Tên ngày chọn trong danh sách; tiết bắt đầu ở các sheet lịch/quy tắc là **1..8**, không dùng chỉ số 0 của cấu hình kỹ thuật.

Cấu hình tham khảo khối 8:

| Ngày | Sáng | Chiều |
| --- | ---: | ---: |
| Thứ Hai | 5 | 4 |
| Thứ Ba | 5 | 0 |
| Thứ Tư | 5 | 4 |
| Thứ Năm | 5 | 0 |
| Thứ Sáu | 5 | 4 |
| Thứ Bảy | 4 | 0 |
| Chủ nhật | 0 | 0 |

0 = buổi nghỉ; chỉ tạo các ô 1..N khi N > 0. Chế độ `morning` chỉ dùng sáng; `both` dùng cả hai; `mixed` dùng ca của mỗi lớp. Số đã nhập không bị tự tăng. Chủ nhật có tiết trong khối đang chọn/lịch nền phải bật `include_sunday` trong CONFIG `session_config`. Số tiết không vượt `max_periods` (1..8).

## 4. Ràng buộc và hoạt động

Trong RANG_BUOC:

- `CONFIG`: nhập khóa và JSON ở cột K. Ví dụ `mode` / `"both"`, `target_grade` / `8`, `time_limit` / `60`; giữ các dòng cấu hình nâng cao đã xuất. Không dùng CONFIG thay các module phòng/lịch nghỉ/tiết cố định/nguyện vọng/hoạt động.
- `NGHI`: loại đối tượng `teacher`, `class` hoặc `room`, mã, ngày và buổi. Trống tiết = nghỉ cả buổi.
- `CO_DINH`: mã phân công, ngày/buổi/tiết bắt đầu, độ dài 1 hoặc 2; phòng nếu cần. Không đặt vào buổi nghỉ hoặc ngoài công suất lớp.
- `MON_SOFT`/`MON_HARD`: JSON quy tắc môn, ví dụ `{"subject":"M01","daily_soft_max":2}` hoặc `{"subject":"M01","max_daily":3}`. Quy tắc HARD không bị đánh đổi để cải thiện SOFT.

Hoạt động có mã `SP_<mã lớp>_<mã môn gốc>`. Loại `CC_SHCN_COMBINED` cho nhãn Chào cờ / Sinh hoạt chủ nhiệm, `EXPERIENTIAL_CAREER` cho Hoạt động trải nghiệm, hướng nghiệp, `SOURCE_OTHER` cho nhãn khác. PENDING và UNRESOLVED giữ đúng tình trạng thiếu quy tắc. VERIFIED cần ghi chú xác minh, lựa chọn cần GV rõ ràng và chính sách independent/collective. Collective cần mã nhóm dùng chung GV. Các hoạt động chưa xác minh không được tự coi đã xếp đủ.

## 5. Nhập an toàn và khôi phục

1. Tải bản nháp JSON nếu cần giữ cả lịch đang xem lâu dài.
2. Chọn **Nhập workbook tổng hợp**. Bộ nhập kiểm tra 11 sheet, mã, tham chiếu, số tiết, phòng, lịch nghỉ, lịch nền và quy tắc. Workbook thiếu/sai bị từ chối; dữ liệu phiên giữ nguyên.
3. Xem số lớp/GV/môn/tiết và danh sách thêm–xóa–sửa. Kiểm tra cảnh báo định danh, thay đổi cấu hình và hash lịch nền trước/sau. Chọn **Tải báo cáo lỗi Excel** để xem đúng sheet, dòng, cột, ô.
4. Đánh dấu đã xem thay đổi/cảnh báo rồi chọn **Xác nhận nhập toàn bộ workbook**. Có thể hủy để giữ nguyên phiên. Nếu phiên đổi sau xem trước hoặc xem trước hết hạn 15 phút, chọn lại file.
5. Xác nhận thay toàn bộ module trong phiên và lưu bản trước nhập trên trình duyệt. Lịch đang xem được lưu trong bản khôi phục, rồi bỏ khỏi phiên hiện hành để không kế thừa chứng minh cũ. Không ghi SOURCE hay baseline. Nếu lưu trình duyệt thất bại, không thay một phần dữ liệu.
6. Khi cần, chọn **Khôi phục trước lần nhập gần nhất** và xác nhận. Dữ liệu, cấu hình, lịch nền và lịch đang xem trước nhập được phục hồi; lịch được hậu kiểm lại. Chỉ giữ một bản trước lần nhập gần nhất. Khôi phục thay các chỉnh sửa sau lần nhập; xuất dữ liệu trước nếu muốn giữ chúng.

Dữ liệu/bản khôi phục gắn với trình duyệt và cổng ứng dụng. Tải lại trang vẫn còn, nhưng xóa bộ nhớ trình duyệt hoặc đổi cổng có thể mất bản lưu. Sao lưu JSON riêng trước các thay đổi lớn.

## 6. Xếp lịch và nghiệm thu

Chọn khối và chế độ, kiểm tra lịch nền; xếp bằng CP-SAT hoặc tối ưu lại/warm start/cục bộ. Khối khác bị khóa, hậu kiểm chạy sau khi xếp. FEASIBLE không chứng minh tối ưu toàn cục. Chỉ PASS đầy đủ với dữ liệu và nền đủ tin cậy mới cho xác nhận hợp lệ; INCOMPLETE giữ cảnh báo.

`data/DU_LIEU_PCCM_37_LOP_THAM_KHAO.xlsx` là dữ liệu kiểm thử nguồn thực, 37 lớp/972 tiết PCCM/111 tiết đặc biệt chưa đủ quy tắc và 64 mã GV chưa xác minh; **không phải lịch nghiệm thu**. Benchmark hiện tại xếp riêng 9 lớp khối 8 (234 tiết), khóa lịch các khối khác. Chưa nghiệm thu Microsoft Excel/Windows thực tế. Xem `reports/UNIFIED_WORKBOOK_TEST_REPORT.md`.
