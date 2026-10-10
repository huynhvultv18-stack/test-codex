# Hướng dẫn sử dụng SMART TKB V3.1.2

## 1. Mở phần mềm trên Windows

Giải nén toàn bộ SMART_TKB_THCS_V3_1_2_SESSION_CONFIG_CANDIDATE.zip vào thư mục có quyền ghi, ví dụ D:\SMART_TKB_SESSION. Mở START_WINDOWS.bat và giữ cửa sổ lệnh đang chạy. Trình duyệt mở http://127.0.0.1:8768. Không mở SOURCE HTML để chạy V3.1.2; đó là bản nguồn V2 giữ nguyên.

## 2. Kiểm tra phạm vi và lịch nền

Màn hình chọn sẵn khối 8 với cấu hình bạn yêu cầu:

| Ngày | Sáng | Chiều |
|---|---:|---:|
| Thứ Hai | 5 | 4 |
| Thứ Ba | 5 | 0 — NGHỈ |
| Thứ Tư | 5 | 4 |
| Thứ Năm | 5 | 0 — NGHỈ |
| Thứ Sáu | 5 | 4 |
| Thứ Bảy | 4 | 0 — NGHỈ |

Mỗi lớp có **9 buổi học, 41 ô tiết/tuần** (29 sáng +12 chiều), 3 buổi nghỉ. Cả 9 lớp: 81 buổi,369 ô,27 buổi nghỉ. Các ô là công suất, không bắt buộc lấp đầy. Chỉ khối được chọn được phép xếp lại.

Chọn **Chỉnh lịch buổi cho → Cả khối** để sửa lịch chung; chọn một lớp để tạo lịch riêng. Ô số tiết nhận0..5. **0=NGHỈ**, không có ô hay biến xếp tiết trong buổi đó. N tiết chỉ dùng1..N. Không tự tăng khi thiếu công suất. Giới hạn có thể mở rộng đến8; giới hạn lớp/GV trong phần bộ giải vẫn phải phù hợp.

**Áp dụng cho cả khối** lấy lịch đang hiển thị, thay lịch chung và các chỉnh riêng của khối đó. **Lớp dùng lịch chung** bỏ chỉnh riêng của lớp đang chọn. **Sao chép lịch lớp** sao chép nguyên7ngày từ lớp nguồn sang lớp đích trong cùng khối. Các khối khóa giữ nguyên.

**Lưu cấu hình buổi** ghi vào trình duyệt theo khối/danh mục lớp. **Khôi phục lần lưu** mở lại chính xác các số0 và chỉnh riêng. **Tải cấu hình JSON/Nạp cấu hình JSON** dùng khi đổi máy hoặc trình duyệt; tệp khác khối/danh mục lớp bị từ chối, không tự ánh xạ. Nhập lỗi giữ nguyên cấu hình cũ. Bật Chủ nhật khi cần; mặc định0/0. Muốn ẩn Chủ nhật, đặt cả hai buổi của lịch chung và mọi lớp về0 trước.

Bảng **Công suất** hiển thị số buổi, số ô, PCCM, buổi nghỉ và phần còn sau tiết cố định. Cảnh báo PCCM vượt công suất, tiết khóa rơi vào buổi nghỉ, xung đột GV/phòng với lịch khóa. Công suất là điều kiện cần, không chứng minh có nghiệm.

Chế độ học ở **Ràng buộc & tối ưu**: chỉ sáng, sáng–chiều, phân ca. Phân ca dùng ca từng lớp trong Dữ liệu PCCM. Chỉ sáng/ca lớp giới hạn buổi được sử dụng nhưng giữ nguyên các số đã nhập; bảng công suất và lịch dùng cấu hình hiệu lực.

Nếu thay số tiết làm một tiết đã xếp rơi vào buổi nghỉ hoặc vượt N, nhấn Xếp/Tối ưu sẽ mở hộp **Xác nhận và xếp lại**. Hủy giữ lịch cũ và đánh dấu lịch cũ so với cấu hình. Xác nhận chỉ giải khối đang chọn; không dịch tiết khóa của các khối khác. Quy tắc này vẫn áp dụng khi tắt warm start. Các tiết cố định của chính khối đang xếp không được tự chuyển: cấu hình mâu thuẫn trả INFEASIBLE.

Bảng khóa hiển thị khối 6, 7, 9, số tiết và hash từng khối. Danh sách GV liên khối dùng đúng mã PCCM, không tự gộp các tên giống nhau. Theo giáo viên hiển thị cả tiết của khối khác với nhãn LỊCH KHỐI KHÁC.

Gói có sẵn lịch **kiểm thử kỹ thuật** V3.1 gồm 738 tiết môn học ngoài khối 8. Lịch này chưa phải lịch được nhà trường nghiệm thu; còn 84 tiết đặc biệt lịch nền chưa có quy tắc. Với dữ liệu kèm gói, nút xếp mặc định trả BLOCKED. Không được coi những ô chưa biết là giờ rảnh đã xác minh.

Dùng Nạp lịch nền JSON để nhập lịch đã lưu của các khối khác. Định dạng:

```json
{
  "source_label": "Tên nguồn và tình trạng xác minh",
  "config": {"mode":"both","days":6,"periods":5},
  "lessons": [
    {"assignment":"MÃ_PCCM","teacher":"MÃ_GV","class_id":"MÃ_LỚP",
     "subject_id":"MÃ_MÔN:PHÂN_MÔN","day":0,"shift":"am","period":1,"length":1,"room":null}
  ]
}
```

Ví dụ trên chỉ mô tả cấu trúc, không phải dữ liệu để nhập. Mã phải tồn tại trong PCCM. Ngày0=thứ Hai, tiết0=tiết1; ca am=sáng, pm=chiều. Lịch sai mã, trùng giáo viên/lớp/phòng, sai số tiết đã ghi, vượt giới hạn hoặc vi phạm lịch nghỉ bị từ chối. Lịch nền có thể có chiều tiết5; những tiết đó vẫn giữ nguyên dù khối 8 chỉ được dùng 4 tiết chiều.

Nếu chỉ kiểm thử kỹ thuật, chọn Mô phỏng khi lịch nền chưa đủ và ghi rõ phần dữ liệu còn thiếu trong Nhãn giả định lịch nền. CROSS-GRADE vẫn BLOCKED. Không dùng mô phỏng làm lịch chính thức.

## 3. Đọc PCCM và cấu hình ràng buộc

Dữ liệu PCCM → Nhập Excel PCCM đọc trực tiếp 5 sheet. Kiểm tra giáo viên, lớp, PCCM và Cảnh báo. Chỉ các lớp/phân công của khối đang chọn được hiển thị để chỉnh ca học, số cặp tiết đôi hoặc danh sách phòng; tổng số tiết và mã giáo viên không được tự thay đổi.

Dữ liệu hiện tại khối 8 có 234 tiết môn học, 27 tiết đặc biệt PENDING và 26 định danh giáo viên chưa xác minh. Đối chiếu mã/họ tên với hồ sơ trường trước khi nghiệm thu. Không gộp mã theo nhãn tên.

Ràng buộc & tối ưu → JSON bổ sung:

```json
{
  "rooms":[{"id":"TIN01","name":"Phòng Tin"}],
  "unavailable":[{"kind":"teacher","id":"MÃ_GV_THỰC","day":0,"shift":"am"}],
  "fixed":[{"assignment":"MÃ_PCCM_THỰC","day":1,"shift":"am","period":0,"length":1}],
  "preferences":[{"kind":"teacher","id":"MÃ_GV_THỰC","day":4,"shift":"pm","weight":3}]
}
```

Thay mã minh họa bằng mã thực; giữ các trường JSON khác đang có. `unavailable` là HARD, `fixed` là HARD; `preferences` là ô muốn tránh, có thể vi phạm với điểm phạt. Phòng cần khai báo rồi gán trong dòng PCCM; không tự suy ra phòng từ môn. HARD không được nới để cải thiện SOFT.

Hoạt động đặc biệt chỉ kiểm kê khối đang xếp. STRICT giữ PENDING khi thiếu quy tắc; không tự gán GV hoặc tiết khóa. Quy tắc xác minh nằm trong special_overrides và cần verification_note. SCENARIO phải chọn rõ từng hoạt động, nhu cầu GV, chính sách độc lập/tập thể và nhãn giả định. CC/SHCN giữ nguyên tên ghép. Tiết SCENARIO được báo riêng; không cộng thành tiết chính thức đã xếp.

## 4. Xếp và tối ưu lại

Bấm Kiểm tra dữ liệu & liên khối, đọc cảnh báo, rồi Xếp TKB khối 8. Lần đầu có thể dùng 60 giây, 4 worker. Nghiệm tìm được luôn đủ toàn bộ tiết đủ điều kiện; không xuất lịch một phần khi UNKNOWN/INFEASIBLE.

Tối ưu lại khối 8 dùng lịch hiện tại đã hậu kiểm làm warm start. Ràng buộc mới có thể làm lịch cũ không hợp lệ; bộ giải không dùng lịch đó làm incumbent được bảo đảm. Khóa ngoài phạm vi cho phép nhập mã lớp/GV trong khối để tái tối ưu cục bộ; các khối khác vẫn khóa toàn bộ. Không được nhập mã lớp ngoài khối để mở khóa.

FEASIBLE: có nghiệm hợp lệ, chưa chứng minh hết mục tiêu. OPTIMAL: đã chứng minh trong phạm vi mô hình được ghi rõ, dưới lịch nền cố định. Nếu tối ưu cục bộ, chỉ chứng minh trong phạm vi cục bộ. UNKNOWN: chưa tìm được nghiệm trong ngân sách, có thể tăng thời gian. INFEASIBLE: ràng buộc không cho phép nghiệm; xem nguyên nhân và đề nghị người quản lý điều chỉnh, phần mềm không tự mở khóa.

Một lớp khối 8 có 26 tiết PCCM: nếu chỉ học chiều 4 tiết ×6 ngày =24 ô, kết quả đúng là INFEASIBLE. Không tự bỏ 2 tiết hoặc tăng số ô để tạo nghiệm.

## 5. Xem, xuất và mở lại

Theo lớp → chọn lớp khối 8; Theo giáo viên → xem cả lịch khóa liên khối. Chất lượng nghiệm hiển thị tiết cần/đã xếp, tiết trống, số buổi, buổi nền, số buổi tăng thêm, phân bố, thời gian, từng objective/best bound và phạm vi chứng minh.

Xuất CSV/Excel lịch chỉ chứa khối đang xếp; Excel có KIEM_CHUNG, HOAT_DONG_PENDING và LOCKED_HASH. Chỉ xuất lịch hiện hành, đã hậu kiểm với lịch nền. In lịch dùng chế độ in của trình duyệt.

Sao lưu JSON V3.1.2 giữ PCCM, cấu hình, lịch khối 8 và toàn bộ lịch nền. Hãy tải backup trước khi đổi máy, xóa dữ liệu trình duyệt hoặc đổi cổng. JSON nhập lại được kiểm tra độc lập và tính lại chỉ số; không kế thừa chứng minh tối ưu lịch sử. Hash lịch khóa không khớp thì báo CRITICAL và giữ dữ liệu hiện tại.

Ví dụ dùng thử: Dữ liệu PCCM → Khôi phục JSON → data/EXAMPLE_SESSION_TECHNICAL_BACKUP.json. Đây là mô phỏng 234 tiết, không phải nghiệm thu lịch thật. Backup V3.1 toàn trường nên được dùng qua Nạp lịch nền; lịch khối 8 cũ có thể vượt 4 tiết chiều nên cần xếp lại. JSON V2 chưa có grade phải bổ sung khối rõ ràng trước khi nhập; phần mềm không đoán khối từ tên lớp.

## 6. Dừng và nghiệm thu

Nhấn Ctrl+C ở cửa sổ lệnh để dừng. Đóng tab không tự dừng Python. Dữ liệu trình duyệt V3.1.2 lưu ở key smart_tkb_thcs_v3_1_2_session_candidate riêng, không ghi đè V2/V3.1/V3.1.1.

Chạy TEST_WINDOWS.bat trên máy Windows thực tế, thử nhập/xếp/khóa/xuất/khôi phục khi ngắt mạng và lập biên bản riêng. Bằng chứng hiện tại chạy trên Linux, chưa thể thay cho kiểm thử Windows.

GRADE8 SCHEDULING=PASS; LOCKED GRADES=PASS cho kiểm thử dữ liệu kèm gói. CROSS-GRADE CONFLICT=BLOCKED vì lịch nền đặc biệt còn thiếu. DATA ACCEPTED=NO; WINDOWS ACCEPTED=NO; PRODUCTION READY=NO.

## 8. Xuất lịch và buổi nghỉ

Excel có sheet TKB cùng LICH_BUOI (mỗi lớp/ngày/buổi, số0 và NGHỈ), CAU_HINH_BUOI, CONG_SUAT và LOCKED_HASH. CSV có record_type=LESSON cho tiết đã xếp, CALENDAR cho cấu hình kể cả buổi0. CALENDAR không phải tiết học. Nhập lại CSV/Excel kiểm tra lịch buổi khớp cấu hình hiện tại và hậu kiểm toàn bộ tiết; nạp cấu hình tương ứng trước khi nhập lịch khác cấu hình. CSV/Excel cũ vẫn được kiểm tra theo cấu hình đang mở.

Sao lưu JSON chỉ đính kèm nghiệm khi lịch hiện hành. Lịch cũ không được xuất như nghiệm mới. Dữ liệu hoạt động PENDING vẫn giữ nguyên, không biến thành tiết học giả.

## 9. Giới hạn nghiệm thu

Các lượt benchmark có lịch hợp lệ đều là FEASIBLE; không chứng minh tối ưu toàn cục. Khối8 có234tiết môn học,27tiết đặc biệt đang chờ,26mãGV chưa xác minh. Lịch nền738tiết có84tiết đặc biệt chưa biết. DATA ACCEPTED=NO, WINDOWS ACCEPTED=NO, PRODUCTION READY=NO. Nghiệm thử không thay thế lịch được nhà trường nghiệm thu.
