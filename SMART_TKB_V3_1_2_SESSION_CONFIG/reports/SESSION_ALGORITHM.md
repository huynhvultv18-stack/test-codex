# Mô hình lịch buổi V3.1.2

`session_config`:schema_version1,max_periods1..8(default5),include_sunday(false),week7ngày(each am/pm integer0..max),class_weeks keyed exact lớp. Không ép kiểu, làm tròn, clamp, đổi mã hay tăng số tiết. Chủ nhật có tiết cần bật rõ. Cấu hình riêng ngoài khối đang chọn bị từ chối. Legacy chưa có session_config giữ nguyên lịch đồng nhất để nhập backup V3.1.1.

Cấu hình hiệu lực N(lớp,ngày,buổi) là lịch riêng hoặc lịch chung, rồi áp chế độ morning/both/mixed. Không đổi số nhập. Assignment có nhiều lớp dùng minN của các lớp. CP-SAT chỉ tạo x[a,length,d,s,p,room] khi0<=p<=N-length. N=0 không tạo biến quyết định hay ô lịch. Tiết đôi length2 liền trong cùng buổi/phòng, không nối buổi hoặc vượtN. Quy tắc hoạt động đặc biệt đi qua cùng miền này; PENDING giữ nguyên.

Exactly-count theo PCCM và all-different giáo viên/lớp/phòng là HARD. Lịch nghỉ,ca,tiết cố định,room whitelist,teacher/class load limits cũng là HARD. Một tiết cố định rơi ngoàiN có tập match rỗng, CP-SAT giải thích qua assumption/core; không tự dời. Cận công suất lớp=sum min(số ô không nghỉ,max_class_session); GV hợp các ô của chính lớp mình dạy, trừ bận/lịch nghỉ/phòng và giới hạn tải sau lịch khóa. Công suất là điều kiện cần, không đủ.

Khối khác không có biến quyết định. Các dòng khóa được deepcopy và SHA-256 canonical toàn bộ trường trước/sau. Bận GV/phòng và tải GV từ lịch khóa là hằng số. Miền vật lý có thể rộng hơn miền khối đang xếp để tính đủ lịch nền; không mở thêm ô cho lớp. Đổi khối ở phiên sau tạo lịch nền với lịch hiệu lực riêng từng lớp thay vì mở rộng đồng nhất. Thiếu lịch nền vẫn UNKNOWN; mặc định BLOCKED hoặc mô phỏng có nhãn, school_conflicts=null.

Tối ưu từ điển giữ nguyên V3.1.1:gap GV→buổi GV→phân bố→nguyện vọng→dồn môn→thay đổi. Mục tiêu chỉ được khóa bằng chứng minh hoặc incumbent có nhãn phân biệt. Ngân sách hết trả incumbent đã hậu kiểm; cold UNKNOWN không sinh lịch giả. Không có chứng minh các mức sau thì toàn lịch FEASIBLE. Local giữ ngoài scope trong khối; lịch ngoài khối luôn khóa. Không tuyên bố tối ưu toàn trường.

Gap tính các ô trống giữa tiết đầu/cuối của GV trong cùng buổi, trên lịch nền+khối mới; nghỉ không có tiết không tạo buổi GV. Visit là tập(teacher,day,shift) có tiết; không tính buổi nghỉ như visit. Phân bố môn dùng những ngày có ít nhất một buổi học của từng lớp. Cận còn sau cố định chỉ trừ những ô cố định hợp lệ; cảnh báo mâu thuẫn vẫn giữ nguyên.

`confirmation` là SHA của target_grade,lịch hiệu lực và toàn bộ lịch hiện tại. Nếu đổi lịch làm tiết hiện tại vượtN thì API/core BLOCKED trước CP khi không có fingerprint phù hợp. UI modal cho hủy/xác nhận; tắt warm không bỏ qua xác nhận. Token cũ hết giá trị khi cấu hình/lịch thay đổi. Xác nhận cho phép giải lại, không cho phép phá HARD hoặc di chuyển tiết cố định.

Hậu kiểm độc lập không đọc biến CP; kiểm đúngID/count/teacher/subject/room, miềntiết/cabound/doubles/specials/load/fixed/holidays và giao với lịch khóa. Script evidence còn tính trực tiếp raw-calendar, occupancy/collision/gaps/visits, đối chiếu SHA và xuất CSV/XLSX. Thử nghiệm hiện tại có9lớp/234tiết; source37lớp chỉ để nhập/audit, không giải đồng loạt.
