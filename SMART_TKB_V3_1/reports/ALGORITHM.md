# CP-SAT V3.1 và các mức chứng minh

Mỗi biến Bool là một khối phân công × ngày × ca × tiết bắt đầu × phòng × độ dài 1/2. Tổng khối đúng số tiết và số cặp tiết đôi; các ô phủ của GV/lớp/phòng có AtMostOne. Nghỉ, khóa, ca, phòng và giới hạn tiết/buổi là HARD. Chỉ cấu hình rõ mới thêm HARD giới hạn môn/ngày. Không nới HARD khi tối ưu.

Nghiệm đầu lấy từ mô hình HARD; mô hình tối ưu bổ sung biến có mặt, tiết trống và chất lượng. Nghiệm trước được dùng làm hint toàn bộ biến/auxiliary; chọn nghiệm trước nếu hợp lệ và tốt hơn theo mục tiêu đang bật. LNS/portfolio có seed/worker cấu hình. Xếp cục bộ biến mọi khối ngoài scope thành tiết khóa; chỉ chứng minh trong tập lịch có các khóa này, không gọi tối ưu toàn trường.

Buổi GV = số (teacher_id, ngày, ca) có ít nhất một tiết. Tiết trống = số ô trống nằm giữa tiết đầu và cuối trong cùng buổi. Với giới hạn L = min(tiết/buổi, max_GV/buổi), cận dưới cho mỗi GV là max(ceil(tổng tải/L), ceil(tải buộc sáng/L)+ceil(tải buộc chiều/L)). Tổng cận là 217 cho sáng–chiều, 239 cho phân ca xen kẽ. Đây là ràng buộc suy ra từ HARD hiện có; không loại bỏ lịch hợp lệ. Tải nhóm tập thể tính một lần cho GV, đồng thời một tiết cho mỗi lớp.

Ưu tiên mặc định: tiết trống → buổi GV → phân bố → dồn môn → nguyện vọng → thay đổi. Tỷ phần thời gian còn lại mặc định 25/50/16/6/2/1; mỗi phase được cấp phần của thời gian còn lại dựa trên các tỷ phần chưa chạy, nên phase kết thúc sớm nhường thời gian cho các phase sau. Có thể bật/tắt mục tiêu, đổi thứ tự hoặc tỷ phần. Weight của một mức từ điển dương chỉ nhân objective/bound; không đổi đánh đổi với mức khác. Trọng số môn trong cùng mức mới đổi đánh đổi giữa môn.

Nếu phase OPTIMAL, khóa giá trị đã chứng minh. Nếu chưa chứng minh, `advance_on_incumbent=true` cho phép khóa giá trị nghiệm tốt nhất và tiếp tục mục tiêu sau. `incumbent_locks` ghi rõ khóa này; các OPTIMAL sau đó chỉ có điều kiện và ghi ở `conditional_optimal_priorities`. Không làm xấu giá trị mục tiêu đã khóa. Cắt objective <= giá trị nghiệm hợp lệ bảo đảm phase ngắn không trả nghiệm xấu hơn ở mục tiêu hiện tại và không loại bỏ optimum tốt hơn. Tắt advance_on_incumbent để dùng chuỗi chứng minh nghiêm ngặt như V3.

FEASIBLE của kết quả nghĩa là lịch đầy đủ qua hậu kiểm, chưa chứng minh tất cả mức đang bật. OPTIMAL chỉ khi mọi mức đang bật đã được chứng minh và không có khóa incumbent chưa chứng minh. OPTIMAL của phase feasibility có objective hằng 0 chỉ chứng minh có lịch, không chứng minh chất lượng lịch. UNKNOWN giữ nghiệm đã có nếu có; không có nghiệm thì conflicts=null, metrics=null. INFEASIBLE do cận công suất hoặc CP-SAT; core giả định là tập đủ gây vô nghiệm, không nhất thiết tối thiểu.

## Điểm môn học (thấp tốt hơn)

Gộp phân môn theo mã môn gốc; không tính HD vào điểm sư phạm môn học. n(c,s,d) là tiết của lớp c, môn s, ngày d; N(c,s) là tổng tuần; P là tiết/buổi.

- Distribution D = sum wD(c,s) × (max_d n − min_d n). Upper UD = sum wD × min(N,2P). Phạt /100 = 100 D/UD (0 nếu UD=0).
- Dồn môn cơ bản = sum wC × max(0,n − daily_soft_max). Mặc định soft max=1 là tiêu chí tối ưu kế thừa V3, không phải quy định bắt buộc của trường.
- Liên tiếp không cần thiết = sum wA × cặp ô kề cùng môn, trừ cặp thuộc khối tiết đôi đã cấu hình. Giữa hai ca không tính kề nhau.
- Chuỗi nặng = heavy_weight × số cửa sổ dài heavy_run_limit+1 toàn môn được chọn là nặng trong cùng buổi. Mặc định không chọn môn nặng.
- Concentration C = dồn môn cơ bản + liên tiếp + chuỗi nặng. Upper UC bảo thủ = sum[wC max(0,N−soft_max)+wA N] + heavy_weight × số lớp × ngày × 2 × max(0,P−heavy_run_limit). /100 = 100 C/UC.
- PREFERENCE: ô muốn tránh GV/lớp/phòng có weight cấu hình; tiết ưu tiên môn phạt từng tiết nằm ngoài preferred_periods × period_weight. Hai khoản cộng ở mức preferences, không chuyển thành HARD.
- Changes = số khối lịch trước mất chữ ký (assignment, ngày, ca, tiết, độ dài, phòng). Không đo số ô học sinh đổi theo cách khác.

Mọi điểm nguyên được tính độc lập từ lịch, không đọc giá trị biến CP-SAT. Tests có fixture phân bố trước/sau, quy tắc khối, tiết đôi miễn phạt liên tiếp, trọng số, HARD giới hạn ngày và bật/tắt. Điểm /100 dùng cận bảo thủ cho cùng cấu hình; khi đổi cấu hình/weight thì không so trực tiếp hai điểm /100 như cùng thang nghiệp vụ.
