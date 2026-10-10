# Benchmark V3.1.3 Candidate · khối 8

Identical input JSON, hardware and serial wall budget; new default has days/waiting/fragmentation/fairness beyond baseline6 goals. Compare common gaps/visits prefix and measured indicators, not whole lex vectors across policies. Independent small exhaustive oracle proves new full vector separately.

Ngân sách A/B20giây,4worker,seed17/23; FAST/PROVE_OPTIMAL10giây; morning/mixed10giây. Đo tuần tự cùng máy Linux, cả A và B nhận input JSON cùng SHA, cùng warm schedule và nền. Bản A17 cuối đo riêng sau khi hồi quy kết thúc; các file input/output và phase trong JSON đủ để đối chiếu. OR-Tools 9.15.6755, Python 3.12.14.

| Lượt | Phiên bản | Tiết | Trống trước→sau | Buổi trước→sau | Ngày trước→sau | Chờ PROXY trước→sau | Giây giải | Trạng thái / hậu kiểm |
|---|---|---|---|---|---|---|---|---|
| ab_reference_s17 | A_V312 | 234/234 | 3→3 | 224→224 | 204→201 | 18→21 | 20.126 | FEASIBLE / INCOMPLETE |
| ab_reference_s17 | B_V313 | 234/234 | 3→3 | 224→224 | 204→193 | 18→28 | 20.058 | FEASIBLE / INCOMPLETE |
| ab_reference_s23 | A_V312 | 234/234 | 3→3 | 224→224 | 204→203 | 18→22 | 20.121 | FEASIBLE / INCOMPLETE |
| ab_reference_s23 | B_V313 | 234/234 | 3→3 | 224→224 | 204→193 | 18→27 | 20.064 | FEASIBLE / INCOMPLETE |
| profile_morning | B_V313 | 234/234 | 9→9 | 231→230 | 211→204 | 15→28 | 10.027 | FEASIBLE / INCOMPLETE |
| profile_mixed | B_V313 | 234/234 | 9→9 | 230→230 | 210→205 | 16→34 | 10.056 | FEASIBLE / INCOMPLETE |
| profile_fast | B_V313 | 234/234 | 3→3 | 224→224 | 204→204 | 18→18 | 0.595 | FEASIBLE / INCOMPLETE |
| profile_prove_optimal | B_V313 | 234/234 | 3→3 | 224→224 | 204→203 | 18→20 | 10.055 | FEASIBLE / INCOMPLETE |

Tất cả8lượt xếp234/234tiết,0xungđột trong lịch đã biết,738tiết khối6/7/9 giữ nguyên; xung đột toàn trường = UNKNOWN. Các lượt Candidate có chứng minh prefix gaps bằng CP, các khóa/mức khác xem từng phase; không có chứng minh tối ưu đầy đủ khối8. FAST không chứng minh; PROVE_OPTIMAL vẫn FEASIBLE trong10giây.

B tối ưu thêm ngày và cụm nên cách dùng phase khác A. Không so sánh một tổng objective giữa hai chính sách. Hai lượt B có193ngày kết hợp so với A201/203, giữ3tiết trống và224buổi; chỉ số chờ PROXY tăng21/22→28/27. Phân bố/dồn môn có thể kém hơn A vì nằm sau các mục tiêu thời gian. Không tuyên bố mọi tiêu chí tốt hơn hoặc tối ưu toàn cục.

Bài synthetic nhỏ có288lịch khả thi được exhaustive độc lập: vector10mức (0,4,4,0,4,1,0,0,1,0) trùng CP-SAT OPTIMAL; PASS chỉ phạm vi fixture đầy đủ, không là dữ liệu trường. Xem TIME_CONFLICT_EXHAUSTIVE_PROOF.json.

163kiểm thử Python (121hồi quy +42mới),55checks trình duyệt (20hồi quy +16lịch buổi +19mới).6filexuất lịch và Excel lỗi/bản nháp FAIL hậu kiểm độc lập. Ba test37lớp lịch sử giữ nguyên nhưng loại khỏi runner riêng khối, tên/lý do ghi trong TIME_CONFLICT_REGRESSION.json.

PCCM đọc5sheet:37lớp,64mãGV,555phân công,972tiết môn,111PENDING. Khối8:9lớp,234tiết môn,27PENDING,26mãGV chưa xác minh. Nền thiếu84tiết đặc biệt. Không tự sửa mã/nguồn. DATA ACCEPTED=NO; WINDOWS ACCEPTED=NO; PRODUCTION READY=NO.
