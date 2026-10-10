# Kiểm kê hoạt động đặc biệt từ sheet 05

74 bản ghi, 111 tiết; 37 lớp × (2 HĐTN,HN + 1 CC/SHCN). Không có PCCM giáo viên hoặc quy tắc tổ chức để xác minh.

| Loại giữ theo nhãn nguồn | Bản ghi | Tiết | Trạng thái |
|---|---:|---:|---|
| Hoạt động trải nghiệm, hướng nghiệp | 37 | 74 | PENDING |
| Chào cờ / Sinh hoạt chủ nhiệm (nhãn ghép) | 37 | 37 | PENDING |

Không suy ra Chào cờ, SHCN, hoạt động tập thể riêng từ ảnh. verified=0, eligible STRICT=0, scheduled STRICT=0, pending=111. Các bản ghi nullable giữ teacher_required=None; không mặc định không cần GV.

STRICT: chỉ đưa hoạt động VERIFIED có verification_note và quy tắc đầy đủ vào mô hình. Quy tắc yêu cầu GV phải dùng teacher_id đã có; không cần GV thì teacher_id=None. Nhóm collective phải khai báo shared_teacher_group, đồng nhất số tiết/ngày/tiết/ca/GV/phòng và các lớp không trùng. SCENARIO dùng lựa chọn rõ từng activity_id và nhãn giả định; nguồn vẫn pending chính thức.

Ảnh hưởng: nếu xác minh hết sẽ thêm 111 ô lớp; nhóm tập thể tính nhiều ô lớp nhưng một sự kiện GV/phòng. Chỉ sáng vẫn vô nghiệm vì GV015 40 tiết >30, không được sửa GV015. Benchmark mở rộng giả định 111 hoạt động độc lập không cần GV do test harness chọn, chỉ kiểm thử kỹ thuật, không phải dữ liệu đã được nhà trường duyệt.

| Lớp | Tiết PCCM | HĐTN,HN pending | CC/SHCN pending | Tổng nguồn | Lý do |
|---|---:|---:|---:|---:|---|
| 6A/1 (C06A01) | 26 | 2 | 1 | 29 | Thiếu PCCM GV và quy tắc tổ chức đã xác minh |
| 6A/2 (C06A02) | 26 | 2 | 1 | 29 | Thiếu PCCM GV và quy tắc tổ chức đã xác minh |
| 6A/3 (C06A03) | 26 | 2 | 1 | 29 | Thiếu PCCM GV và quy tắc tổ chức đã xác minh |
| 6A/4 (C06A04) | 26 | 2 | 1 | 29 | Thiếu PCCM GV và quy tắc tổ chức đã xác minh |
| 6A/5 (C06A05) | 26 | 2 | 1 | 29 | Thiếu PCCM GV và quy tắc tổ chức đã xác minh |
| 6A/6 (C06A06) | 26 | 2 | 1 | 29 | Thiếu PCCM GV và quy tắc tổ chức đã xác minh |
| 6A/7 (C06A07) | 26 | 2 | 1 | 29 | Thiếu PCCM GV và quy tắc tổ chức đã xác minh |
| 6A/8 (C06A08) | 26 | 2 | 1 | 29 | Thiếu PCCM GV và quy tắc tổ chức đã xác minh |
| 6A/9 (C06A09) | 26 | 2 | 1 | 29 | Thiếu PCCM GV và quy tắc tổ chức đã xác minh |
| 7A/1 (C07A01) | 26 | 2 | 1 | 29 | Thiếu PCCM GV và quy tắc tổ chức đã xác minh |
| 7A/2 (C07A02) | 26 | 2 | 1 | 29 | Thiếu PCCM GV và quy tắc tổ chức đã xác minh |
| 7A/3 (C07A03) | 26 | 2 | 1 | 29 | Thiếu PCCM GV và quy tắc tổ chức đã xác minh |
| 7A/4 (C07A04) | 26 | 2 | 1 | 29 | Thiếu PCCM GV và quy tắc tổ chức đã xác minh |
| 7A/5 (C07A05) | 26 | 2 | 1 | 29 | Thiếu PCCM GV và quy tắc tổ chức đã xác minh |
| 7A/6 (C07A06) | 26 | 2 | 1 | 29 | Thiếu PCCM GV và quy tắc tổ chức đã xác minh |
| 7A/7 (C07A07) | 26 | 2 | 1 | 29 | Thiếu PCCM GV và quy tắc tổ chức đã xác minh |
| 7A/8 (C07A08) | 26 | 2 | 1 | 29 | Thiếu PCCM GV và quy tắc tổ chức đã xác minh |
| 7A/9 (C07A09) | 26 | 2 | 1 | 29 | Thiếu PCCM GV và quy tắc tổ chức đã xác minh |
| 8A/1 (C08A01) | 26 | 2 | 1 | 29 | Thiếu PCCM GV và quy tắc tổ chức đã xác minh |
| 8A/2 (C08A02) | 26 | 2 | 1 | 29 | Thiếu PCCM GV và quy tắc tổ chức đã xác minh |
| 8A/3 (C08A03) | 26 | 2 | 1 | 29 | Thiếu PCCM GV và quy tắc tổ chức đã xác minh |
| 8A/4 (C08A04) | 26 | 2 | 1 | 29 | Thiếu PCCM GV và quy tắc tổ chức đã xác minh |
| 8A/5 (C08A05) | 26 | 2 | 1 | 29 | Thiếu PCCM GV và quy tắc tổ chức đã xác minh |
| 8A/6 (C08A06) | 26 | 2 | 1 | 29 | Thiếu PCCM GV và quy tắc tổ chức đã xác minh |
| 8A/7 (C08A07) | 26 | 2 | 1 | 29 | Thiếu PCCM GV và quy tắc tổ chức đã xác minh |
| 8A/8 (C08A08) | 26 | 2 | 1 | 29 | Thiếu PCCM GV và quy tắc tổ chức đã xác minh |
| 8A/9 (C08A09) | 26 | 2 | 1 | 29 | Thiếu PCCM GV và quy tắc tổ chức đã xác minh |
| 9A/1 (C09A01) | 27 | 2 | 1 | 30 | Thiếu PCCM GV và quy tắc tổ chức đã xác minh |
| 9A/2 (C09A02) | 27 | 2 | 1 | 30 | Thiếu PCCM GV và quy tắc tổ chức đã xác minh |
| 9A/3 (C09A03) | 27 | 2 | 1 | 30 | Thiếu PCCM GV và quy tắc tổ chức đã xác minh |
| 9A/4 (C09A04) | 27 | 2 | 1 | 30 | Thiếu PCCM GV và quy tắc tổ chức đã xác minh |
| 9A/5 (C09A05) | 27 | 2 | 1 | 30 | Thiếu PCCM GV và quy tắc tổ chức đã xác minh |
| 9A/6 (C09A06) | 27 | 2 | 1 | 30 | Thiếu PCCM GV và quy tắc tổ chức đã xác minh |
| 9A/7 (C09A07) | 27 | 2 | 1 | 30 | Thiếu PCCM GV và quy tắc tổ chức đã xác minh |
| 9A/8 (C09A08) | 27 | 2 | 1 | 30 | Thiếu PCCM GV và quy tắc tổ chức đã xác minh |
| 9A/9 (C09A09) | 27 | 2 | 1 | 30 | Thiếu PCCM GV và quy tắc tổ chức đã xác minh |
| 9A/10 (C09A10) | 27 | 2 | 1 | 30 | Thiếu PCCM GV và quy tắc tổ chức đã xác minh |
