# OPTIMIZATION · đo thực tế

PASS có phạm vi: 6/12 cặp khả thi cải thiện theo đúng thứ tự từ điển, 5 kém hơn, 1 bằng; không bảo đảm bản sửa luôn thắng hoặc thắng best-of-seeds baseline. B/A từng lượt ở AB_BENCHMARK.md. Hai mức ưu tiên đầu (0 gap, 217/239 visits warm) được giữ. Cold mixed 245→243 visits là cải thiện thật, cùng0 gap và972/972 tiết qua independent verifier.

Model-ready giảm trong cả12 cặp khả thi, median giảm 14.4%; không giảm số biến hay ràng buộc, không giảm peak memory đồng đều. Cache rule môn/khối và index unavailable loại bỏ lặp lookup, bỏ chỉ mục Python không dùng. BASELINE_MODEL_PROFILE.txt ghi bottleneck trước thay đổi.

Warm full schedule qua independent verifier được dùng làm incumbent ngay; tránh clone và CP feasibility, phase này chỉ mất thời gian verifier. Khi đạt cận phổ quát, gap/visits không cần chạy lại CP; objective=bound và proof riêng, solver_status=null. Warm portfolio w4 giảm6 CP calls còn3; worker1 giảm6 còn2. Thời gian tiết kiệm cấp cho các mục tiêu sau, nhưng thay quỹ đạo search có thể làm distribution cuối kém hơn A. Kiểm thử ngân sách0.001s giữ lịch warm hợp lệ; cold cùng ngân sách UNKNOWN không bị giả thành lịch.

LNS được thử A/B seed17/23,workers4,time30 với cùng warm input. Both seed17: distribution475→466,concentration76→61; seed23:462→472,58→67 (kém). Mixed seed17:587→600 (kém); seed23:604→596 (tốt). Không chọn default chỉ vì một seed. B minh họa both466/mixed596 vẫn kém best A462/587 trên toàn tập cấu hình.

Công thức và scope chứng minh ở ALGORITHM.md. 26 lượt A/B đều lưu raw phase status, objective, best bound, gap, timing, model size, peak RSS. Các kết quả toàn lịch là FEASIBLE; đạt cận visits không chứng minh chất lượng các mức sau. Lower bound không có incumbent không được dùng thay nghiệm.

OPTIMIZATION = PASS theo tiêu chí cải thiện có đo tại các profile nêu rõ; BASELINE DOMINANCE ALL PROFILES = FAIL. DATA ACCEPTED = NO; WINDOWS ACCEPTED = NO; PRODUCTION READY = NO.
