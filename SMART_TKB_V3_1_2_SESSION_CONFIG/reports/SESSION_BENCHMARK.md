# Benchmark khối8 · V3.1.2

Grade8 only; frozen grades6/7/9; Linux measurement; Windows untested

Source37lớp được nhập và kiểm tra; chỉ9lớp khối8 được giải.234tiết môn học,27tiết đặc biệt PENDING;26mãGV chưa xác minh. Lịch nền738tiết giữ nguyên,84tiết đặc biệt lịch nền chưa biết. Mô phỏng kỹ thuật có nhãn; school_conflicts=null. Không nghiệm thu lịch thực tế. Ngân sách30s cho4profile chính,10s cho2chế độ bổ sung; workers4,seed17. Lượt giải chạy tuần tự; đọc báo cáo và kiểm tra browser smoke ngắn có thể tạo nhiễu OS. Wall bao gồm overhead Python/hậu kiểm; không phải thời gianCP thuần.

| Cấu hình | Cần/đã xếp | Công suất | Buổi nghỉ* | Xung đột trong khối/đã biết liên khối | Trống GV** | Buổi GV** | Giây | Trạng thái |
|---|---:|---:|---:|---|---:|---:|---:|---|
| uniform5am4pm | 234/234 | 486 | 0 | 0/0 | 0 | 223 | 29.753 | FEASIBLE |
| variable_days | 234/234 | 378 | 0 | 0/0 | 3 | 228 | 29.731 | FEASIBLE |
| reference_rest_sessions | 234/234 | 369 | 27 | 0/0 | 3 | 224 | 29.691 | FEASIBLE |
| different_classes | 234/234 | 360 | 25 | 0/0 | 3 | 223 | 29.813 | FEASIBLE |
| reference_morning | 234/234 | 261 | 54 | 0/0 | 9 | 231 | 9.994 | FEASIBLE |
| reference_mixed | 234/234 | 261 | 54 | 0/0 | 9 | 230 | 10.000 | FEASIBLE |
| incomplete_background_default_blocked | 234/0 | 369 | 27 | —/— | — | — | 0.000 | BLOCKED |
| over_capacity_infeasible | 234/0 | 54 | 54 | —/— | — | — | 0.006 | INFEASIBLE |

*Buổi nghỉ cộng theo9lớp trên thứHai..thứBảy; chế độ morning/mixed tính cả buổi không được phép sử dụng. Sunday0/0 không cộng khi ẩn. **Trống/buổi GV tính trên hợp lịch nền đã biết và lịch khối8, không đếm buổi trống không có tiết. Buổi nền186; số tăng thêm có trong raw metrics.

Reference: sáng5/5/5/5/5/4;chiều4/0/4/0/4/0. Mỗi lớp41ô,9buổi; toàn khối369ô,81buổi học,27buổi nghỉ. different_classes giảm riêng1tiết sáng từng lớp và thay chiều của4lớp, giữ đúng lựa chọn. Variable_days có378ô; uniform5/4 có486ô.

6lượt có nghiệm đều234/234,0xungđột trong khối/đã biết với lịch khóa; independent verifier và raw-calendar/occupancy audit PASS. Mọi lịch giữ SHA khối khóa. Không có chứng minh tối ưu các mục tiêu sau; trạng thái FEASIBLE,global_optimal_proven=false. Không so chất lượng giữa bài toán có miền khác nhau như một phép A/B.

Mặc định thiếu nền:BLOCKED,solver_status=NOT_RUN,không có lịch và xung đột=null. Không gọi BLOCKED làINFEASIBLE. over_capacity:6ô/lớp<26tiết PCCM/lớp,INFEASIBLE bởi cận công suất; không tăng số tiết,không mở khóa. Chi tiết chẩn đoán:

```
Lớp 8A/1: cần 26, sức chứa 6 tiết
Lớp 8A/2: cần 26, sức chứa 6 tiết
Lớp 8A/3: cần 26, sức chứa 6 tiết
Lớp 8A/4: cần 26, sức chứa 6 tiết
Lớp 8A/5: cần 26, sức chứa 6 tiết
Lớp 8A/6: cần 26, sức chứa 6 tiết
Lớp 8A/7: cần 26, sức chứa 6 tiết
Lớp 8A/8: cần 26, sức chứa 6 tiết
Lớp 8A/9: cần 26, sức chứa 6 tiết
GV GV013 — Thầy Vũ: cần 10, sức chứa 5 tiết (am/pm)
GV GV014 — Cô K Anh: cần 8, sức chứa 5 tiết (am/pm)
GV GV020 — Cô Hưng: cần 10, sức chứa 5 tiết (am/pm)
GV GV022 — Thầy Thư: cần 9, sức chứa 6 tiết (am/pm)
GV GV033 — T. Thắng: cần 18, sức chứa 6 tiết (am/pm)
GV GV035 — Cô V Hằng: cần 9, sức chứa 6 tiết (am/pm)
GV GV042 — Cô PLiễu: cần 8, sức chứa 6 tiết (am/pm)
GV GV043 — Cô Thắng: cần 7, sức chứa 4 tiết (am/pm)
GV GV044 — Cô BThủy: cần 15, sức chứa 6 tiết (am/pm)
GV GV045 — Cô Nguyệt: cần 12, sức chứa 6 tiết (am/pm)
GV GV046 — Cô NThủy: cần 8, sức chứa 6 tiết (am/pm)
GV GV047 — Cô Cường: cần 20, sức chứa 6 tiết (am/pm)
GV GV048 — Thầy Tài: cần 20, sức chứa 6 tiết (am/pm)
GV GV049 — Cô Hạnh: cần 7, sức chứa 6 tiết (am/pm)
GV GV050 — Cô Huế: cần 7, sức chứa 3 tiết (am/pm)
GV GV051 — T. Trực: cần 9, sức chứa 6 tiết (am/pm)
GV GV052 — Cô Linh: cần 6, sức chứa 5 tiết (am/pm)
GV GV056 — T.T Tính: cần 18, sức chứa 6 tiết (am/pm)
GV GV062 — Cô Trân: cần 15, sức chứa 6 tiết (am/pm)
Giữ nguyên khối khóa. Có thể đề nghị người quản lý điều chỉnh lịch nền/phòng/giới hạn hoặc ngày học; phần mềm không tự mở khóa.
```

Raw các phases,objective/bounds/locks/model_scope và calendar nằm trong reports/sessions/*.json. SESSION_INDEPENDENT_VERIFICATION.json tính lại metrics và kiểm5fileUIexport. WINDOWS ACCEPTED=NO; DATA ACCEPTED=NO; PRODUCTION READY=NO.
