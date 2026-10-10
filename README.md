## SMART TKB THCS V3.1 Optimized Candidate

Bản rà soát/sửa tại chỗ V3.1: [mã nguồn](SMART_TKB_V3_1_OPTIMIZED), [ZIP Windows ngoại tuyến](dist/SMART_TKB_THCS_V3_1_OPTIMIZED_CANDIDATE.zip), [SHA-256](dist/SMART_TKB_THCS_V3_1_OPTIMIZED_CANDIDATE.zip.sha256), [FULL AUDIT](SMART_TKB_V3_1_OPTIMIZED/reports/FULL_AUDIT.md), [A/B benchmark](SMART_TKB_V3_1_OPTIMIZED/reports/AB_BENCHMARK.md), [tiêu chí nghiệm thu](SMART_TKB_V3_1_OPTIMIZED/reports/ACCEPTANCE.json).

71 unit và28 browser checks PASS trên Linux, gồm chạy từ ZIP giải nén mới. A/B26 lượt có6/12 cặp khả thi tốt hơn,5 kém hơn,1 bằng; không bảo đảm bản sửa luôn tốt hơn baseline. Chỉ sáng vô nghiệm với GV01540>30;111 tiết hoạt động nguồn vẫn PENDING. WINDOWS RUNTIME=UNTESTED; DATA ACCEPTED=NO; WINDOWS ACCEPTED=NO; PRODUCTION READY=NO.

# test-codex