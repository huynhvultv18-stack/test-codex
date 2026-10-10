# PCCM IMPORT — đọc trực tiếp 5 sheet

| Sheet | Dòng dữ liệu thực tế | Kết quả |
|---|---:|---|
| 01_DANH_SACH_LOP | 37 | 9 lớp khối 6, 9 lớp khối 7, 9 lớp khối 8, 10 lớp khối 9 |
| 02_DANH_SACH_GV | 64 | Giữ nguyên GV001..GV064; tất cả REVIEW, họ tên đầy đủ để trống |
| 03_DANH_MUC_MON | 17 | Khóa composite mã môn:phân môn, giữ riêng Sử/Địa, L/H/S, Nhạc/MT |
| 04_PCCM_TOAN_TRUONG | 555 + 1 dòng tổng | 972 tiết đã phân công; dòng TỔNG CỘNG chỉ đối chiếu, không nhập thành phân công |
| 05_SO_TIET_THEO_LOP | 481 + 1 dòng tổng | 1.083 tiết/ô có lịch; dòng tổng chỉ đối chiếu |

### Chuẩn hóa và kiểm tra

Chuẩn hóa Unicode NFC và khoảng trắng ở biên; giữ nguyên nhãn nguồn, ID tạm và phân môn. Không gộp các giáo viên có tên gần nhau: Thầy Độ/T. Thắng/T. Tính/T.T Tính/... đều là mã riêng theo workbook. Không đổi L/H/S thành tên khoa học chưa có chú giải chính thức. Composite subject_id ngăn các dòng cùng mã môn nhưng khác phân môn bị coi là trùng.

Đã đối chiếu số tiết từng lớp/môn giữa sheet 04/05, tổng tiết môn học từng lớp với sheet 01, tải GV với sheet 02, nhãn và khối với mã tham chiếu. Trong phần môn học, **0 lỗi ERROR, 0 ID/phân công trùng**. SOURCE sheet 04 đánh dấu tổng 34 ô trùng giờ; giữ evidence nhưng không khóa mặc định các ô lịch quan sát. Source schedule không phải nghiệm warm start hợp lệ.

### 69 cảnh báo, không tự sửa

- 64 `TEACHER_ID_REVIEW`: thiếu họ tên/định danh chính thức.
- 3 `SUBJECT_REVIEW`: KHTN L/H/S chờ chú giải.
- 1 `SPECIAL_UNASSIGNED`: 111 tiết HĐTN&HN/CC-SHCN trong sheet 05 chưa có phân công ở sheet 04.
- 1 `SOURCE_CONFLICTS`: 34 ô nguồn đánh dấu trùng giờ. Đây là số ô đánh dấu, không phải khẳng định số xung đột duy nhất.

Mỗi lớp có 3 tiết hoạt động đặc biệt chưa phân công (37 × 3 = 111); 27 lớp khối 6–8 có 26 tiết môn học, 10 lớp khối 9 có 27 tiết môn học; 27 × 26 + 10 × 27 = 972. Tổng 972 + 111 = 1.083.

### Điều kiện benchmark

Chỉ dùng **972 tiết có PCCM giáo viên** để kiểm thử kỹ thuật, không loại bỏ một tiết nào của sheet 04. 111 tiết đặc biệt vẫn pending, không thêm giáo viên giả, không đặt hoạt động vào lịch ngầm. Thiếu phòng thực tế, nghỉ, tiết khóa và quy định tiết đôi: benchmark nguồn không tự tạo các ràng buộc nghiệp vụ này. Các fixture phòng/tiết đôi ở unit test chỉ chứng minh khả năng kỹ thuật.

GV015 — Thầy Độ có 40 tiết môn học/tuần. Chỉ sáng 6 ngày × 5 tiết có 30 ô GV, nên INFEASIBLE được chứng minh bằng capacity bound. Không chia mã GV hoặc giảm số tiết để làm báo cáo PASS.

**DATA ACCEPTED = NO; PRODUCTION READY = NO.** Cần bổ sung phân công hoạt động đặc biệt, danh tính GV và quy định vận hành trước nghiệm thu lịch thực tế.
