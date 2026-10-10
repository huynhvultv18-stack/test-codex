# Changelog

## 3.1.1 Optimized Candidate · 2026-10-10

Nâng cấp tại chỗ từ V3.1 đã bàn giao, giữ nguyên SOURCE và baseline.

- Chặn bypass kiểm kê bằng marker JSON; bảo toàn 111 tiết và tổng nguồn.
- Từ chối ngày/tiết phân số, boolean và cấu hình nonfinite; bổ sung đối chiếu dòng tổng.
- Warm incumbent độc lập đã xác nhận; tránh clone/tìm lại feasibility; chứng minh lower bound tách CP status.
- Cache rule môn/khối, index lịch nghỉ; đo model, phase, first solution và peak RSS benchmark.
- CSV escape đảo ngược được, Excel literal; khôi phục JSON atomic và hậu kiểm lại.
- Giữ collective/fixed scenario rules; phân biệt VERIFIED/APPROVED/MISSING/CONFLICT; SCENARIO không thành nghiệm thu.
- LocalStorage riêng, khóa chỉnh cấu hình khi đang giải, tránh phản hồi inventory cũ; trước/sau và sửa tràn 390px.
- 26 lượt A/B baseline V3.1, ba seed, hai worker profiles, portfolio/LNS; giữ cả lượt kém hơn.
- Giữ toàn bộ test gốc; thêm unit/browser regressions. Windows runtime vẫn UNTESTED.

DATA ACCEPTED = NO · WINDOWS ACCEPTED = NO · PRODUCTION READY = NO.
