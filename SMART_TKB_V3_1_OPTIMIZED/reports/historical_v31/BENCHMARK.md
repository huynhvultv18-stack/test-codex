# Benchmark V3 / V3.1 thực thi

Máy Linux-6.18.44-x86_64-with-glibc2.41, Python 3.12.14, OR-Tools 9.15.6755, logical CPU=5. Chạy tuần tự14 lượt, 425.764 giây.

## A. So sánh công bằng

Cùng972 tiết,37 lớp,64 GV,6 ngày,5 tiết/buổi,giới hạn5. Mỗi cặp có cùng dữ liệu, seed, worker, ngân sách và cùng warm incumbent. V3.1 phase allocation/cuts/search là phần đánh giá. Không chạy solver khác đồng thời trong phần A.

| Chế độ | Profile (seed/worker/giây) | V3 buổi | V3.1 buổi | V3 phân bố | V3.1 phân bố | V3 dồn môn | V3.1 dồn môn |
|---|---|---:|---:|---:|---:|---:|---:|
| both | cold_s17_w4_t30 | 218 | 217 | 624 | 537 | 238 | 157 |
| both | warm_s23_w4_t45 | 217 | 217 | 639 | 498 | 251 | 100 |
| both | warm_s29_w1_t30 | 218 | 217 | 638 | 634 | 251 | 247 |
| mixed | cold_s17_w4_t30 | 240 | 248 | 703 | 644 | 319 | 273 |
| mixed | warm_s23_w4_t45 | 240 | 239 | 686 | 615 | 306 | 256 |
| mixed | warm_s29_w1_t30 | 240 | 240 | 694 | 694 | 311 | 311 |

12 lượt có lịch:972/972,0 xung đột,0 tiết trống,FEASIBLE. Chỉ sáng ở cả hai:INFEASIBLE,0/972,không có lịch; GV01540>30 ô. Không lấy conflicts=0 trong log V3 cũ làm bằng chứng có lịch; V3.1 conflicts=null khi không có nghiệm.

Sáng–chiều cold218→217, phân bố624→537. Warm45 giây cả hai217 nhưng phân bố639→498 và dồn môn251→100. Phân ca warm45 giây240→239, phân bố686→615. Phân ca cold30 giây V3.1 kém hơn240→248; warm worker1 giữ240, không cải thiện. Không bảo đảm một lượt ngắn bất kỳ tốt hơn V3. Nên dùng lịch hợp lệ làm warm start và đọc bound/phase. Multiworker có biến động; rerun có thể khác. Tập thử nhỏ, không khẳng định cải thiện mọi dữ liệu.

217 và239 chạm cận dưới buổi suy từ tải/ca. Các lượt warm45 giây có CP-SAT phase gaps/visits OPTIMAL; distribution/concentration FEASIBLE. Chỉ hai mức đầu đã chứng minh. Toàn lịch FEASIBLE, global_optimal_proven=false. Khóa incumbent không phải chứng minh.

Objective,best_bound,seconds,status,proof_scope từng phase ghi đầy đủ trong FAIR_BENCHMARK.json và reports/fair/*.json. INDEPENDENT_EVIDENCE_CHECK.json hậu kiểm14 kết quả và tính lại chỉ số, không đọc biến CP-SAT.

| V3.1 bàn giao | Profile | Phân bố /100 | Dồn môn /100 | Giây | Chứng minh |
|---|---|---:|---:|---:|---|
| both | warm_s23_w4_t45 | 51.2346 | 17.6991 | 45.392 | gaps,visits; toàn lịch FEASIBLE |
| mixed | warm_s23_w4_t45 | 63.2716 | 45.3097 | 45.318 | gaps,visits; toàn lịch FEASIBLE |

## B. Mở rộng hoạt động

Nguồn có0 tiết đặc biệt đủ quy tắc STRICT;111 pending. Phần A STRICT không công nhận1083 tiết chính thức. Fixture phần B chọn rõ74 activity_ids/111 tiết, giả định độc lập không cần GV; giả định do test harness chọn, lưu nguyên văn. Không tạo GV hoặc sửa workbook.

| SCENARIO | PCCM xếp | Giả định | Xung đột | Trống | Buổi GV | Trạng thái |
|---|---:|---:|---:|---:|---:|---|
| morning | 0/972 | 0 | Không có lịch | — | — | INFEASIBLE |
| both | 972/972 | 111 | 0 | 0 | 217 | FEASIBLE |
| mixed | 972/972 | 111 | 0 | 0 | 262 | FEASIBLE |

Hai chế độ có lịch:972 PCCM +111 mô phỏng=1083 ô lớp kỹ thuật; verified=0,pending chính thức=111,official_complete=false. Không công bố1083/1083 lịch xác minh. Kết quả phần B không dùng so chất lượng với phần A vì tập ô lớp khác. Xếp lại cục bộ37 lớp khóa ngoài C06A01 giữ0 thay đổi,0 trống,217 buổi; global_optimal_proven=false.

**OPTIMIZATION=PASS theo tiêu chí có cải thiện đo được trong benchmark công bằng; không bảo đảm mọi lượt cải thiện. DATA ACCEPTED=NO; WINDOWS ACCEPTED=NO; PRODUCTION READY=NO.**
