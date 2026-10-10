# Benchmark riêng khối 8

Dữ liệu thực: 9 lớp, 234 tiết môn học, 27 tiết đặc biệt PENDING, 26 mã GV chưa xác minh. Lịch nền V3.1 có 738 tiết môn học; 84 tiết đặc biệt của khối khóa chưa có quy tắc. Các lượt dữ liệu thực là mô phỏng kỹ thuật có nhãn, CROSS-GRADE = BLOCKED. Không phải lịch được trường nghiệm thu.

| Lượt | Trạng thái | Đã xếp | Trống GV (cả nền) | Buổi GV (cả nền) | Buổi tăng | Phân bố | Giây |
|---|---|---:|---:|---:|---:|---:|---:|
| default_strict_blocked | BLOCKED | 0/234 | — | — | — | — | 0 |
| both_cold_s17_t30 | FEASIBLE | 234/234 | 0 | 222 | 36 | 112 | 29.665 |
| both_warm_s17_t30 | FEASIBLE | 234/234 | 0 | 221 | 35 | 112 | 30.109 |
| both_local_C08A01_t10 | OPTIMAL | 234/234 | 0 | 221 | 35 | 112 | 1.171 |
| morning_cold_s17_t10 | FEASIBLE | 234/234 | 9 | 229 | 43 | 118 | 9.959 |
| mixed_am_cold_s17_t10 | FEASIBLE | 234/234 | 9 | 229 | 43 | 126 | 9.976 |
| mixed_pm_capacity_infeasible | INFEASIBLE | 0/234 | — | — | — | — | 0.006 |
| complete_background_synthetic_fixture | OPTIMAL | 3/3 | 0 | 4 | 1 | 1 | 0.013 |

Số buổi nền là 186. Buổi tăng tính theo tập buổi có GV, không cộng riêng số buổi khối 8. Tiết trống tính trên lịch hợp nhất, chỉ giữa các tiết trong cùng buổi; không tính khoảng nghỉ trưa. Những GV không dạy khối 8 đóng góp hằng số vào tổng nền. Điểm phân bố/dồn môn chỉ xét khối 8.

Cold và warm cùng PCCM, lịch nền, 5 sáng/4 chiều/6 ngày, seed17,4 worker,30 giây ngân sách. Warm bắt đầu từ nghiệm cold và dùng LNS. Thời gian wall gồm tạo mô hình và hậu kiểm, có thể vượt ngân sách giải vài phần giây. Worker4 có thể cho nghiệm khác khi chạy lại.

OPTIMAL trong lượt local chỉ chứng minh dưới khóa các lớp còn lại của khối 8 và toàn bộ khối khác. OPTIMAL fixture là dữ liệu tổng hợp 1 lớp khối 8 với lịch nền đầy đủ; không phải nghiệm tối ưu của dữ liệu thực. Mọi kết quả giữ GLOBAL OPTIMAL PROVEN = NO đối với toàn trường.

Mục tiêu, best bound, cận tương đối, các mức đã chứng minh và mức chỉ có điều kiện nằm trong GRADE8_BENCHMARK.json và từng reports/grade8/*.json. Không so trực tiếp với benchmark 37 lớp. Các báo cáo V3.1 trước đây được giữ trong historical_v31_optimized/ và không được chạy lại trong phạm vi này.
