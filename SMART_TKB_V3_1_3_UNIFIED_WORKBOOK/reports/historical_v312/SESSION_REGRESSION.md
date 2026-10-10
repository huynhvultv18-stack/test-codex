# Regression V3.1.2

PASS: **121 kiểm thử Python** (93 hồi quy +28lịch buổi), **20 kiểm tra browser hồi quy** và **16 kiểm tra browser lịch buổi** trên Linux Chromium. Không xóa test gốc/tắt assertion. Lỗi trong quá trình phát triển đã được sửa và chạy lại; log hiện tại là lượt hoàn tất.

- Miền0..5 và mở rộng6/Sunday,buổi0/cả ngày0,khác ngày/lớp,công suất thiếu,tiết đôi tràn/nối buổi,khóa nghỉ,phòng/GV liên khối và giới hạn tải cộng nền.
- Rawcounts giữ nguyên; cấu hình sai/mã ngoài khối/bool/phân số bị từ chối. Metadata lịch buổi trong Excel không được làm tròn.
- Special STRICT/PENDING/SCENARIO/collective vẫn giữ; không sinh hoạt động vào buổi nghỉ hoặc tự xóa pending.
- Warm/incumbent/local,UNKNOWN ngân sách nhỏ,INFEASIBLE core/capacity; soft không đánh đổi HARD; scope chỉ khối.
- Confirmation trướcCP khi đổi số tiết ảnh hưởng lịch; fingerprint cũ bị từ chối,tắt warm vẫn cần xác nhận,hủy giữ lịch,đổi cấu hình+reload vẫn giữ trạng thái cũ có nhãn.
- UI grade/class/copy/apply/reset/save/restore/JSON/Sunday/capacity; không có ôN+1,NGHỈ shading; asyncimport khóa thao tác để tránh phản hồi cũ ghi đè; mở lại chỉnh buổi sau khi solver hoàn tất.
- 20luồng hồi quy gồm bootstrap9/234/26,bg738/84,CSRF/Host/CSP,backup lỗi atomic,lịch3chếđộ/234warm,CSV/XLSX/JSON/hash,đổi khối tương lai giữ lịch8 không giải9,mobile390/768/1366px,noJSerrors.
- 8benchmark được audit độc lập,6nghiệm234/234;5UIexports qua hậu kiểm,bao gồm Excel khối8thật.
- Baseline ZIP/tree1593file giữ nguyên; SOURCE và1336fileWindows runtime/wheel/provenance byte-identical. Chưa chạy Windows thật.

3testlegacy whole-school vẫn giữ nguyên trong source và chỉ loại khỏi runner riêng khối để tuân thủ phạm vi: test_solver.SolverTests.test_morning_37_class_capacity_diagnosis, test_solver.SolverTests.test_unknown_is_not_infeasible, test_v3_1.V31Tests.test_unknown_no_conflict_claim. Không chạy mô hình37lớp; UNKNOWN/công suất được cover theo khối8. Benchmark lịch sử không thay thế kiểm thử hiện tại.

Evidence: SESSION_REGRESSION.json/SESSION_REGRESSION_RUN.txt,SESSION_BROWSER_REGRESSION.json,SESSION_BROWSER.json,SESSION_INDEPENDENT_VERIFICATION.json,SESSION_SOURCE_IMMUTABILITY.json. Chi tiết số test/chạy/chưa chạy có trong JSON.

WINDOWS ACCEPTED=NO · DATA ACCEPTED=NO · PRODUCTION READY=NO.
