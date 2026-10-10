# A/B · V3.1 baseline → Optimized Candidate

Linux-6.18.44-x86_64-with-glibc2.41; Python 3.12.14; OR-Tools 9.15.6755; logical CPU=5. 26 lượt / 13 cặp, dữ liệu 37 lớp, 64 GV, 972 tiết PCCM. 18 lượt portfolio và 8 lượt LNS; seed 17/23/29, workers 4/1, time_limit 30 giây.

A là mã V3.1 từ ZIP SHA-256 a94c50bbe617c72210412ff5fa9b491d1bc2691fd6502fe7a35436ece04029e9; B là bản sửa. Mỗi cặp dùng cùng máy, JSON đầu vào được SHA, cấu hình, ngân sách, seed, worker và lịch warm nguồn. Chạy solver tuần tự trong process mới, không có solver khác chạy đồng thời. Các thao tác đọc báo cáo/browser ngắn trong thời gian đo có thể tạo nhiễu OS; nhiều worker không tất định, rerun có thể khác. Không dùng kết quả SCENARIO vào so sánh A/B 972 tiết. Tập benchmark nhỏ, không suy ra mọi dữ liệu.

Portfolio đo checkpoint sau sửa solver; các kiểm tra tổng nguồn/importer/UI bổ sung sau đó không thay đổi mô hình trên đầu vào hợp lệ này. LNS đo phiên bản mô hình/solver cuối; sau đó chỉnh nhãn UI và tách APPROVED trong báo cáo, không đổi mô hình hoặc search trên nguồn37 lớp. Model-ready được instrument giống nhau ở validate(); wall gồm chuẩn bị projection, tạo mô hình, giải và hậu kiểm, không gồm mở Excel. RSS là process kernel high water mark MiB. Budget nominal 30s có overhead, không gọi wall 30.4s là đúng 30.0s.

| Chế độ/profile | Gap A→B | Buổi A→B | Distribution A→B | Concentration A→B | Changes A→B | So từ điển B/A |
|---|---:|---:|---:|---:|---:|---|
| morning/cold_s17_w4_t30 | — | — | — | — | — | CAPACITY_PROOF |
| both/cold_s17_w4_t30 | 0 → 0 | 217 → 217 | 560 → 576 | 177 → 191 | 0 → 0 | WORSE |
| both/warm_s17_w4_t30 | 0 → 0 | 217 → 217 | 484 → 476 | 89 → 82 | 350 → 428 | BETTER |
| both/warm_s23_w4_t30 | 0 → 0 | 217 → 217 | 483 → 475 | 88 → 78 | 346 → 455 | BETTER |
| both/warm_s29_w1_t30 | 0 → 0 | 217 → 217 | 498 → 498 | 100 → 100 | 0 → 0 | EQUAL |
| mixed/cold_s17_w4_t30 | 0 → 0 | 245 → 243 | 639 → 642 | 277 → 275 | 0 → 0 | BETTER |
| mixed/warm_s17_w4_t30 | 0 → 0 | 239 → 239 | 604 → 606 | 249 → 249 | 311 → 99 | WORSE |
| mixed/warm_s23_w4_t30 | 0 → 0 | 239 → 239 | 606 → 609 | 250 → 253 | 306 → 81 | WORSE |
| mixed/warm_s29_w1_t30 | 0 → 0 | 239 → 239 | 615 → 615 | 256 → 256 | 244 → 0 | BETTER |
| both/warm_lns_s17_w4_t30 | 0 → 0 | 217 → 217 | 475 → 466 | 76 → 61 | 465 → 627 | BETTER |
| both/warm_lns_s23_w4_t30 | 0 → 0 | 217 → 217 | 462 → 472 | 58 → 67 | 569 → 611 | WORSE |
| mixed/warm_lns_s17_w4_t30 | 0 → 0 | 239 → 239 | 587 → 600 | 232 → 246 | 494 → 227 | WORSE |
| mixed/warm_lns_s23_w4_t30 | 0 → 0 | 239 → 239 | 604 → 596 | 248 → 239 | 406 → 316 | BETTER |

**6 cặp tốt hơn, 5 kém hơn, 1 bằng nhau; 1 cặp morning có cùng chứng minh vô nghiệm.** Không tính giảm changes là cải thiện khi distribution/visits ưu tiên cao hơn xấu đi. Tất cả 24 lịch khả thi đạt 972/972, 0 xung đột và 0 tiết trống, status FEASIBLE, không có chứng minh toàn cục. Chỉ sáng cả A/B: INFEASIBLE, 0/972, conflicts/metrics null, GV015 40 > 30 tiết công suất; không sửa giáo viên để ép nghiệm.

| Mode/profile | Model ready A/B s | Vars/constraints A/B | Wall A/B s | Peak RSS A/B MiB | CP calls A/B |
|---|---:|---|---:|---:|---:|
| morning/cold_s17_w4_t30 | — / — | — / — | 0.033 / 0.011 | 89.7 / 90.9 | 0 / 0 |
| both/cold_s17_w4_t30 | 0.756 / 0.619 | 51073/32150 / 51073/32150 | 29.346 / 29.307 | 805.3 / 831.6 | 5 / 5 |
| both/warm_s17_w4_t30 | 0.942 / 0.753 | 51073/32150 / 51073/32150 | 30.404 / 30.472 | 791.0 / 808.3 | 6 / 3 |
| both/warm_s23_w4_t30 | 0.966 / 0.874 | 51073/32150 / 51073/32150 | 30.341 / 30.468 | 788.4 / 871.1 | 6 / 3 |
| both/warm_s29_w1_t30 | 0.935 / 0.794 | 51073/32150 / 51073/32150 | 28.320 / 27.098 | 406.7 / 396.7 | 6 / 2 |
| mixed/cold_s17_w4_t30 | 0.429 / 0.408 | 34424/31040 / 34424/31040 | 29.503 / 29.512 | 572.9 / 571.0 | 5 / 5 |
| mixed/warm_s17_w4_t30 | 0.558 / 0.480 | 34424/31040 / 34424/31040 | 30.451 / 30.391 | 606.5 / 661.0 | 6 / 3 |
| mixed/warm_s23_w4_t30 | 0.530 / 0.465 | 34424/31040 / 34424/31040 | 30.438 / 30.386 | 652.0 / 630.7 | 6 / 3 |
| mixed/warm_s29_w1_t30 | 0.526 / 0.469 | 34424/31040 / 34424/31040 | 30.382 / 26.992 | 323.0 / 319.1 | 6 / 2 |
| both/warm_lns_s17_w4_t30 | 1.023 / 0.783 | 51073/32150 / 51073/32150 | 30.215 / 30.361 | 549.8 / 570.4 | 6 / 3 |
| both/warm_lns_s23_w4_t30 | 0.963 / 0.753 | 51073/32150 / 51073/32150 | 30.183 / 30.402 | 567.0 / 553.0 | 6 / 3 |
| mixed/warm_lns_s17_w4_t30 | 0.598 / 0.467 | 34424/31040 / 34424/31040 | 30.405 / 30.361 | 480.4 / 481.3 | 6 / 3 |
| mixed/warm_lns_s23_w4_t30 | 0.528 / 0.456 | 34424/31040 / 34424/31040 | 30.386 / 30.372 | 446.2 / 484.7 | 6 / 3 |

Raw CP calls và phases ghi objective, best_bound, relative_gap, proof_scope và giây. Không có scalar objective/bound chung cho toàn bộ chuỗi từ điển; gap phase không phải global optimality gap. UNKNOWN phase có objective/gap null, giữ incumbent cũ đã hậu kiểm. PROVEN_LOWER_BOUND và VERIFIED_INCUMBENT là trạng thái ứng dụng, solver_status=null; không đổi thành CP OPTIMAL. First CP success và first verified incumbent tách nhau.

Warm input cho both/mixed có gap=0 và buổi=217/239. Cận buổi được đạt bởi lịch hợp lệ nên hai mức đầu có chứng minh prefix, còn phân bố/dồn môn chưa chứng minh. Cold mixed B 243 < A245 nhưng chưa chạm cận239; không gọi 243 là tối ưu. Local37 khóa ngoài C06A01 đạt 0 thay đổi; proof_scope=local_frozen, global_optimal_proven=false.

| Result B chọn để minh họa, không phải cấu hình tối ưu cho mọi trường | Xếp/xung đột | Gap/buổi | Distribution/concentration | Giây/Peak MiB |
|---|---|---|---|---|
| both, warm LNS seed 17, w4,30s | 972/972, 0 | 0/217 | 466/61 (phạt /100 47.9424/10.7965) | 30.361/570.4 |
| mixed, warm LNS seed 23, w4,30s | 972/972, 0 | 0/239 | 596/239 (phạt /100 61.3169/42.3009) | 30.372/484.7 |

Best A trên các profile thử: both distribution462 (LNS seed23), mixed587 (LNS seed17); best B466/596. Không tuyên bố B vượt best-of-seeds baseline. Portfolio warm both seed17/23 cải thiện ở cả hai seed; LNS không cải thiện đều. Khuyến nghị dùng incumbent đã kiểm tra, giữ priorities phù hợp và thử LNS khi có thời gian; không đổi mặc định theo một seed thắng.

Mở rộng 37 lớp: SCENARIO both/mixed xếp972 tiết PCCM +111 mô phỏng, 0 xung đột; không công nhận1083 tiết chính thức. STRICT nguồn0 verified/approved,111 MISSING/PENDING. AB_INDEPENDENT_VERIFICATION.json kiểm26 kết quả và tính lại metrics bằng verifier hiện tại. EXTENDED_BENCHMARK.json tách fixture giả định.

**OPTIMIZATION = PASS theo tiêu chí có cải thiện đo được tại 6 profile và không làm xấu mục tiêu cao hơn trong những cặp đó. Phạm vi PASS có giới hạn; dominance mọi profile = FAIL (5 cặp kém hơn). Không chứng minh tối ưu toàn cục hoặc cấu hình thắng mọi seed.**
