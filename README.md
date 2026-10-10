## SMART TKB THCS V3.1.3 Unified Workbook Candidate

**Một file Excel 11 sheet cho toàn bộ dữ liệu**, nhập có xem trước/xác nhận/khôi phục, báo lỗi theo sheet–dòng–cột và xuất lại dữ liệu hiện có. Giữ nguyên grade-only CP-SAT, khóa lịch các khối khác và hậu kiểm.

- [Tải ZIP Windows ngoại tuyến](https://github.com/huynhvultv18-stack/test-codex/raw/refs/heads/smart-tkb-v3-1-3-unified-workbook-candidate/dist/SMART_TKB_THCS_V3_1_3_UNIFIED_WORKBOOK_CANDIDATE.zip)
- [Tải mẫu Excel tổng hợp](https://github.com/huynhvultv18-stack/test-codex/raw/refs/heads/smart-tkb-v3-1-3-unified-workbook-candidate/SMART_TKB_V3_1_3_UNIFIED_WORKBOOK/MAU_DU_LIEU_SMART_TKB_THCS.xlsx)
- [Hướng dẫn sử dụng workbook](SMART_TKB_V3_1_3_UNIFIED_WORKBOOK/HUONG_DAN_SU_DUNG_WORKBOOK.md)
- [Mã nguồn](SMART_TKB_V3_1_3_UNIFIED_WORKBOOK) · [Báo cáo kiểm thử](SMART_TKB_V3_1_3_UNIFIED_WORKBOOK/reports/UNIFIED_WORKBOOK_TEST_REPORT.md)
- [SHA-256 ZIP](dist/SMART_TKB_THCS_V3_1_3_UNIFIED_WORKBOOK_CANDIDATE.zip.sha256)

206 kiểm thử Python + 71 kiểm tra browser đạt; workbook 37 lớp mở/lưu bằng LibreOffice rồi nhập lại không đổi dữ liệu. Ba chế độ xếp khối 8 đủ 234/234 tiết FEASIBLE, 0 xung đột đã biết, giữ hash lịch khóa. Nguồn chưa xác minh/thiếu hoạt động đặc biệt nên hậu kiểm INCOMPLETE, không chứng minh tối ưu toàn cục hay 0 xung đột toàn trường. **PRODUCTION READY = NO**; Microsoft Excel/Windows thực tế chưa nghiệm thu. Không ghi đè baseline/SOURCE, không merge main.

Các Candidate trước giữ nguyên:

## SMART TKB THCS V3.1.3 Optimization + Conflict Candidate

CP-SAT tối ưu thời gian GV; hậu kiểm độc lập GV/lớp/phòng với PASS/FAIL/INCOMPLETE/STALE theo hash/version. Chỉ giải khối chọn, giữ nguyên khối khóa. FAST/BALANCED/PROVE_OPTIMAL, tiết trống/buổi/ngày/chờ, warm/LNS/neighborhood/multi-seed, chỉnh tay và báo cáo lỗi.

- [Tải ZIP Windows ngoại tuyến](https://github.com/huynhvultv18-stack/test-codex/raw/refs/heads/smart-tkb-v3-1-3-optimization-conflict-candidate/dist/SMART_TKB_THCS_V3_1_3_OPTIMIZATION_CONFLICT_CANDIDATE.zip)
- [Hướng dẫn sử dụng](SMART_TKB_V3_1_3_OPTIMIZATION_CONFLICT/HUONG_DAN_SU_DUNG.md)
- [Mã nguồn](SMART_TKB_V3_1_3_OPTIMIZATION_CONFLICT) · [Benchmark A/B](SMART_TKB_V3_1_3_OPTIMIZATION_CONFLICT/reports/TIME_CONFLICT_BENCHMARK.md)
- [SHA-256](dist/SMART_TKB_THCS_V3_1_3_OPTIMIZATION_CONFLICT_CANDIDATE.zip.sha256) · [Kiểm tra gói](dist/SMART_TKB_THCS_V3_1_3_PACKAGE_VERIFICATION.json)

163 kiểm thử Python +55checks trình duyệt đạt;288lịch synthetic được exhaustive độc lập đối chiếu CP-SAT OPTIMAL.8lượt benchmark khối8 xếp234/234tiết,0xungđột đã biết,738tiết khóa không đổi. A/B cùng input/budget/worker/seed: Candidate giảm ngày201/203→193, giữ3tiết trống/224buổi; chờ PROXY tăng21/22→28/27, không tuyên bố mọi mục tiêu cải thiện.

PCCM thực tế và nền thiếu dữ liệu: INCOMPLETE, chưa chứng minh tối ưu đầy đủ. DATA ACCEPTED=NO; WINDOWS ACCEPTED=NO; PRODUCTION READY=NO. SOURCE/V3.1.2 giữ nguyên; không merge main hoặc Production. Source Git không kèm runtime/wheels, dùng ZIP đầy đủ để chạy ngoại tuyến Windows.

Các phiên bản trước giữ nguyên để truy xuất:

## SMART TKB THCS V3.1.2 Session Config Candidate

**0tiết=NGHỈ · lịch riêng ngày/buổi/lớp · khối8 mặc định41ô/9buổi · giữ lịch các khối khóa.**

- [Tải ZIP Windows ngoại tuyến](https://github.com/huynhvultv18-stack/test-codex/raw/refs/heads/smart-tkb-v3-1-2-session-config-candidate/dist/SMART_TKB_THCS_V3_1_2_SESSION_CONFIG_CANDIDATE.zip)
- [Hướng dẫn sử dụng](SMART_TKB_V3_1_2_SESSION_CONFIG/HUONG_DAN_SU_DUNG.md)
- [Mã nguồn](SMART_TKB_V3_1_2_SESSION_CONFIG) · [Benchmark](SMART_TKB_V3_1_2_SESSION_CONFIG/reports/SESSION_BENCHMARK.md)
- [SHA-256](dist/SMART_TKB_THCS_V3_1_2_SESSION_CONFIG_CANDIDATE.zip.sha256) · [Kiểm tra ZIP](dist/SMART_TKB_THCS_V3_1_2_PACKAGE_VERIFICATION.json)

121testPython +36browser checks đạt.6nghiệm benchmark khối8 xếp234/234tiết; các khối khóa738tiết giữ nguyên.6nghiệm và5filexuấtUI qua kiểm tra độc lập. Source và baseline V3.1.1 không đổi. Lịch nền thiếu84tiết đặc biệt,khối8 có27tiết PENDING và26mãGV chưa xác minh; CROSS-GRADE cònBLOCKED. DATA/WINDOWS ACCEPTED=NO; PRODUCTION READY=NO. Không merge main/Production.

Các phiên bản dưới đây được giữ để truy xuất:

## SMART TKB THCS V3.1.1 Grade8 Candidate

**Chỉ xếp khối8 · 5tiết sáng/4tiết chiều · 6ngày · khóa khối6/7/9.**

- [Tải ZIP Windows ngoại tuyến](https://github.com/huynhvultv18-stack/test-codex/raw/refs/heads/smart-tkb-v3-1-1-grade8-candidate/dist/SMART_TKB_THCS_V3_1_1_GRADE8_CANDIDATE.zip)
- [Hướng dẫn sử dụng](SMART_TKB_V3_1_1_GRADE8/HUONG_DAN_SU_DUNG.md)
- [Mã nguồn và benchmark](SMART_TKB_V3_1_1_GRADE8)
- [SHA-256 ZIP](dist/SMART_TKB_THCS_V3_1_1_GRADE8_CANDIDATE.zip.sha256)

234/234tiết môn học khối8 đã xếp trong mô phỏng kỹ thuật,738tiết nền không thay đổi.93regression và20browser checks đạt,6lịch benchmark đã hậu kiểm độc lập.27tiết đặc biệt khối8 và84tiết đặc biệt nền còn thiếu quy tắc;26mã GV chưa xác minh. CROSS-GRADE=BLOCKED; DATA/WINDOWS ACCEPTED=NO; PRODUCTION READY=NO. Chưa nghiệm thu Windows thực tế.

Các bản dưới đây là lịch sử, giữ nguyên SOURCE và package:

## SMART TKB THCS V3.1 Optimized Candidate

Bản rà soát/sửa tại chỗ V3.1: [mã nguồn](SMART_TKB_V3_1_OPTIMIZED), [ZIP Windows ngoại tuyến](dist/SMART_TKB_THCS_V3_1_OPTIMIZED_CANDIDATE.zip), [SHA-256](dist/SMART_TKB_THCS_V3_1_OPTIMIZED_CANDIDATE.zip.sha256), [FULL AUDIT](SMART_TKB_V3_1_OPTIMIZED/reports/FULL_AUDIT.md), [A/B benchmark](SMART_TKB_V3_1_OPTIMIZED/reports/AB_BENCHMARK.md), [tiêu chí nghiệm thu](SMART_TKB_V3_1_OPTIMIZED/reports/ACCEPTANCE.json).

71 unit và28 browser checks PASS trên Linux, gồm chạy từ ZIP giải nén mới. A/B26 lượt có6/12 cặp khả thi tốt hơn,5 kém hơn,1 bằng; không bảo đảm bản sửa luôn tốt hơn baseline. Chỉ sáng vô nghiệm với GV01540>30;111 tiết hoạt động nguồn vẫn PENDING. WINDOWS RUNTIME=UNTESTED; DATA ACCEPTED=NO; WINDOWS ACCEPTED=NO; PRODUCTION READY=NO.

# test-codex