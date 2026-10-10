# Regression V3.1 thực thi

SOLVER REGRESSION = PASS. OPTIMIZATION = PASS (có cải thiện đo được; xem cả lượt kém hơn). SPECIAL ACTIVITIES = PASS (kiểm kê/giữ pending, không suy đoán).

- Baseline ZIP V3 bất biến: chạy lại23 unit tests PASS,12 browser checks PASS.
- V3.1:45 unit tests PASS (23 regression gốc +22 mở rộng),20 browser checks PASS trên Chromium Linux. Logs UNIT_TESTS.txt,UI_TESTS.json,BROWSER_RUN.txt.
- 14 kết quả benchmark37 lớp,3 chế độ được hậu kiểm độc lập và tính lại metrics:PASS. 12 lịch khả thi972/972,0 xung đột,0 trống;2 trường hợp chỉ sáng vô nghiệm có chứng minh40>30.
- Warm start nhiều seed/worker/time, giữ nguyên ngoài phạm vi C06A01 trong lịch37 lớp:PASS,0 thay đổi. Không gọi tối ưu cục bộ là tối ưu toàn trường.
- HARD số tiết/phân công/ca/giới hạn/phòng/khóa/nghỉ/tiết đôi, xung đột GV/lớp/phòng, scope:PASS. Subject HARD opt-in, soft grade rules, bật/tắt/trọng số/phạt chuẩn hóa, ảnh hưởng phân bố trước/sau, tiết đôi miễn phạt, PREFERENCE tách dồn môn:PASS.
- Special STRICT thiếu GV/rule giữpending; VERIFIED fixture không GV, nhóm tập thể GV thực và nhóm lớp, khóa/phòng/công suất, teacher conflict không bị nới; SCENARIO cần lựa chọn và nhãn, giữpending chính thức:PASS.
- UI nhập PCCM Excel thật5 sheet, JSON V2/V3/V3.1, CSV/Excel schedule roundtrip, backup/restore với hậu kiểm, biểu đồ/thống kê/đối chiếu, live SCENARIO label:PASS. Không có native browser errors hoặc external requests. Host/Origin/CSRF checks:PASS. Không báo0 xung đột cho trường hợp không có lịch.
- Ngưỡng thời gian cực ngắn UNKNOWN không bị đổi INFEASIBLE hoặc tạo lịch một phần:PASS.

Windows runtime/wheel/lock kế thừa và kiểm tra tính toàn vẹn; dependency resolution win_amd64/cp312 ngoại tuyến kiểm tra riêng. Đây không phải thực thi ứng dụng trên Windows. WINDOWS ACCEPTED = NO. Không có máy Windows thực tế trong môi trường này.

DATA ACCEPTED = NO:64 định danh GV tạm, ký hiệu phân môn và111 hoạt động chưa được nhà trường xác minh. PRODUCTION READY = NO.

Bản ZIP giải nén riêng: chạy lại45 unit tests và20 browser checks PASS; log PACKAGE_UNIT_TESTS.txt,PACKAGE_BROWSER_RUN.txt. Runtime/wheel resolution ngoại tuyến PASS, vẫn chưa kiểm thử Windows thực tế.
