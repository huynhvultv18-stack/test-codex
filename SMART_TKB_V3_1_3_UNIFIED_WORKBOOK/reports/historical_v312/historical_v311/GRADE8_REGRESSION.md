# Regression V3.1.1 Grade8

93/93 kiểm thử Python đạt trên Linux Python3.12. Gồm 25 kiểm thử mới theo khối và 68 kiểm thử V3.1 liên quan: import5sheet/tổng/thiếu/trùng mã, HARD/SOFT/PREFERENCE, tiết đôi/phòng, lịch nghỉ/khóa/giới hạn, STRICT/SCENARIO/APPROVED, không tin JSON giả nội bộ, exact identity, warm/LNS/incumbent, proof bounds, CSV/Excel formula escaping và hậu kiểm độc lập.

3 kiểm thử cũ gọi giải toàn trường được ghi NOT_RUN_SCOPE trong GRADE8_REGRESSION.json: morning37capacity và 2UNKNOWN37. Không chạy mô hình37lớp; UNKNOWN/INFEASIBLE được kiểm tra theo khối. Không dùng PASS lịch sử để thay kết quả mới.

20/20 kiểm tra Chromium/Playwright đạt: mặc định9lớp234tiết/26GV,5sáng4chiều6ngày;3khối khóa/17GVliênkhối/84special nền; chỉ27special khối8; CSRF/Host/CSP; JSON hỏng/nội bộ giả; thiếu nền BLOCKED; restore lỗi giữ nguyên dữ liệu; fixture nền đầy đủ CROSSGRADE PASS; solve/warm; xem GV cả tiết khóa; tảiCSV/XLSX/JSON; reload/import hậu kiểm không kế thừa proof; tamper hashCRITICAL; backup234tiết thật; warm234tiết thật; xuấtExcel thật; đổi khối phiên sau giữ lịchkhối8mới nhất nhưng không solvekhối9; responsive390/768/1366; không lỗiJS. Chi tiết trong GRADE8_BROWSER.json; screenshot GRADE8_UI.png.

6 lịch có nghiệm của benchmark được kiểm tra độc lập, khớp toàn bộ số tiết/giới hạn/slot/teacher/room, metrics và cận đã chứng minh. Local giữ các lớp khối8ngoài phạm vi, mọi lượt giữ hash738dòng các khối khóa. INFEASIBLE/UNKNOWN/BLOCKED không khai0xungđột nếu không có lịch. Xem GRADE8_INDEPENDENT_VERIFICATION.json.

SOURCE HTML/XLSX,1546tệp baseline và1336tệp runtime/wheel được đối chiếu SHA. Windows x64 ABI/cp312/dependency payload được kế thừa nguyên byte; chưa thực thi máy Windows. DATA ACCEPTED=NO; WINDOWS ACCEPTED=NO; PRODUCTION READY=NO.

Chạy: python tests/run_grade_regression.py; python tests/verify_grade_evidence.py. Browser development cần Playwright+Chromium, dùng TKB_BASE để đổi cổng; không phải dependency chạy phần mềm Windows. TEST_WINDOWS.bat dùng runner theo khối.
