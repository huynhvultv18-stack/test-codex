# Mô hình theo khối và hậu kiểm

PCCM đầy đủ được kiểm tra trước, rồi lọc classes/assignments của target_grade. Mặc định có 9 lớp,135 phân công,234 tiết. Không tự sửa số tiết, giáo viên, môn hoặc định danh. filter_data tạo bản sao; SOURCE và baseline bất biến.

prepare_grade phân lịch đã lưu thành warm rows của khối đang xếp và frozen rows các khối còn lại. Dòng khóa giữ nguyên mọi trường và thứ tự. Hash canonical JSON SHA-256 chụp toàn bộ trường từng dòng, cả metadata, và từng khối. Không có biến xếp tiết cho các khối khóa; model_scope ghi class_ids,assignment_ids,decision_placements và locked_lesson_decision_variables=0.

Biến Bool chỉ cho mỗi placement (phân công,ngày,ca,tiết bắt đầu,độ dài,phòng) của khối đang xếp. Đủ số bloc đơn/đôi; resource capacity1 giáo viên/lớp/phòng; giới hạn buổi; HARD môn/ngày opt-in. Loại placement giao với thời gian bận giáo viên/phòng lịch khóa. Tải giáo viên/buổi cộng cả nền. Tiết cố định/PCCM dùng assumption để giải thích vô nghiệm; capacity bound có thể chứng minh INFEASIBLE trước khi dựng mô hình. Không mở khóa ngoài khối.

Calendar vật lý đủ rộng để giữ cả tiết/ngày nền. Placement khối8 chỉ dùng active_days và session_periods={am:5,pm:4}; hoạt động/tiết đôi không vượt buổi. Nền có thể dùng chiều tiết5 hoặc ngày không học của khối8, vẫn tính đúng lịch GV. 6ngày không đồng nghĩa phải lấp hết ô.

Mục tiêu từ điển: đủ tiết và HARD luôn bắt buộc; sau đó gaps,visits,distribution,preferences,concentration,changes. Gaps/visits lấy hợp nhất nền+khối8; hằng số của GV chỉ dạy khối khác vẫn có trong tổng. Baseline_visits tính từ nền; added_visits=|buổi hợp nhất|-|buổi nền|. Không cộng độc lập buổi khối8 vào buổi nền. Phân bố/dồn môn/nguyện vọng/changes chỉ tối ưu phần có thể thay đổi. Tiết trống là ô trống nằm giữa các tiết trong cùng ngày/ca, không tính nghỉ trưa.

Mỗi mức giữ giá trị mức trước; incumbent dominance cut không cho xấu đi mức đang tối ưu. Warm được hậu kiểm cả HARD lẫn nền trước khi dùng. Nếu chưa chứng minh mà tiếp tục mức sau, ghi incumbent_locks và proof_scope có điều kiện; không nâng thành chứng minh toàn cục. Cận dưới đạt bởi incumbent được hậu kiểm có nhãn PROVEN_LOWER_BOUND, không giả là lượt CP-SAT. LNS tái dùng nghiệm tốt; tối ưu cục bộ khóa thêm các dòng khối8 ngoài scope. OPTIMAL local chỉ chứng minh phạm vi local; global_optimal_proven luôn False cho toàn trường.

verify_grade không đọc biến CP-SAT: kiểm tra lại PCCM,HARD,nội bộ rồi độc lập giao occupancy giáo viên/phòng với nền và cộng tải buổi. So hash mọi trường khóa, khác là CRITICAL. CSV/Excel/JSON nhập lại đi qua checker và recompute metrics; không kế thừa proof lịch sử. validate_problem chặn dấu hiệu JSON giả nội bộ, dữ liệu thiếu/thừa/trùng, phòng/mã không có.

Lịch nền thiếu giữ trạng thái unknown và mặc định BLOCKED trước solve. Chỉ chạy kỹ thuật với allow_incomplete_background=true và background_assumption không rỗng. known_cross_grade_conflicts có thể bằng0, nhưng cross_grade_conflicts/school_conflicts=null và CROSS-GRADE=BLOCKED. Lịch nền có lỗi bị từ chối, không âm thầm sửa. Nền có SCENARIO không được coi đầy đủ chính thức. Hoạt động liên cả khối đang xếp và khối khóa bị chặn thay vì tự tách.

STRICT/SCENARIO tái dùng module SpecialActivity V3.1. Chỉ kiểm kê khối đang xếp;27tiết PENDING trong dữ liệu thật. Không gán GV/slot hoặc tách CC/SHCN. Scenario có nhãn và lựa chọn riêng, không cộng vào placed chính thức.
