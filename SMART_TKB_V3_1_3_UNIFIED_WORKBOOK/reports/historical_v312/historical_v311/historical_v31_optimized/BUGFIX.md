# BUGFIX · V3.1 Optimized Candidate

14 phát hiện đã xử lý; không xóa test gốc hoặc tắt assertion. Bằng chứng tái hiện A/B có trong BUG_REPRODUCTIONS.json; các kiểm tra mới ở tests/test_audit.py và tests/browser_audit.cjs.

| Mã | Mức | Lỗi và thay đổi | Bằng chứng |
|---|---|---|---|
| A01 | CRITICAL | JSON giả _special_prepared bỏ qua kiểm kê và quy tắc. **Sửa:** PreparedData nội bộ; từ chối dấu nội bộ từ JSON (special.py) | BUG_REPRODUCTIONS.json + test_public_markers_cannot_bypass_inventory |
| A02 | HIGH | Verifier chấp nhận ngày phân số ngoài ô lịch nguyên. **Sửa:** Kiểm kiểu nguyên nghiêm ngặt trước tính toán; định dạng dòng/list (validation.py) | BUG_REPRODUCTIONS.json + 4 malformed schedule tests |
| A03 | HIGH | special_activities có thể bỏ một bản ghi nguồn, còn 110 thay 111. **Sửa:** Khớp bất biến loại/lớp/định mức và tổng nguồn/định mức từng lớp (special.py/validation.py) | BUG_REPRODUCTIONS.json + inventory/metadata tests |
| A04 | HIGH | Nhập Excel dùng int() làm tròn ngày 0.5 thành 0. **Sửa:** Chỉ nhận số nguyên hoặc chuỗi nguyên đúng định dạng (exchange.py) | BUG_REPRODUCTIONS.json + Excel fractional test |
| A05 | HIGH | Khôi phục JSON thay data/config trước yêu cầu hậu kiểm thứ hai. **Sửa:** Một yêu cầu kiểm cả cấu hình và lịch; apply sau khi thành công (web/app.js) | UI_AUDIT_TESTS.json: failed restore giữ 37 lớp |
| A06 | MEDIUM | Warm start hợp lệ phải tìm lại nghiệm, có thể mất khi ngân sách rất nhỏ. **Sửa:** Hậu kiểm nghiệm trước; dùng làm incumbent, bỏ clone/call feasibility (solver.py) | test_warm_valid_schedule_survives_tiny_budget + A/B |
| A07 | MEDIUM | CSV bảo vệ công thức làm mất dấu apostrophe/không đảo ngược ID. **Sửa:** Escape đảo ngược được; Excel ghi literal text, không ghi formula (exchange.py) | test_csv_formula_escape_is_reversible |
| A08 | MEDIUM | NaN phase fractions/bool weight hoặc cấu hình sai kiểu được nhận. **Sửa:** Số hữu hạn/kiểu chính xác; request JSON object, từ chối NaN/Infinity (validation.py/server.py) | BUG_REPRODUCTIONS.json + API/browser tests |
| A09 | MEDIUM | UI ghi đè collective/fixed rules thành independent khi readConfig. **Sửa:** Giữ cấu hình special_scenario; thêm chọn policy và mã nhóm (web/app.js) | UI_AUDIT_TESTS.json |
| A10 | MEDIUM | UI ô priorities gây trang tràn ở 390 px; async inventory có thể về sai thứ tự. **Sửa:** Giới hạn rộng select; bỏ phản hồi cũ bằng request generation (web/style.css/app.js) | UI_AUDIT_TESTS.json: 4 tabs × 3 viewports |
| A11 | MEDIUM | Kiểm kê chưa phân biệt quy tắc phê duyệt, thiếu và mâu thuẫn. **Sửa:** audit_status VERIFIED/APPROVED/MISSING/CONFLICT; giữ PENDING nguồn (special.py) | test_approved_rule_requires_explicit_note + conflict/missing test |
| A12 | MEDIUM | Importer không cảnh báo thiếu/trùng dòng tổng. **Sửa:** Cần đúng một dòng tổng sheet 04 và 05; giữ đối chiếu chi tiết (importer.py) | duplicate/missing total row tests |
| A13 | LOW | Lặp lookup môn/khối và lịch nghỉ ở hàng chục nghìn placement; chỉ mục không dùng. **Sửa:** Cache rule theo lớp/môn; index nghỉ; bỏ daily index/dead hints (quality.py/solver.py) | BASELINE_MODEL_PROFILE.txt + A/B model_ready |
| A14 | LOW | Thiếu đo mô hình và quá ít phạm vi kiểm tra mobile. **Sửa:** Timing/vars/constraints, CPU phase, peak RSS fresh-process, browser nhiều viewport (solver.py/tests) | AB_BENCHMARK.json + UI_AUDIT_TESTS.json |

Hồi quy theo nhóm: FIX_GROUP1_REGRESSION.txt, FIX_GROUP2_REGRESSION.txt, FIX_GROUP3_REGRESSION.txt; mỗi nhóm vẫn đạt 45 test gốc. UNIT_REGRESSION.txt là lượt cuối đầy đủ. CRITICAL/HIGH tồn đọng đã biết trong phạm vi rà soát: 0. Windows thực thi và nghiệm thu dữ liệu còn BLOCKED, không coi là đã sửa/đã kiểm tra.
