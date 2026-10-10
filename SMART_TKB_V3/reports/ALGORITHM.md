# CP-SAT V3: mô hình, tối ưu và kiểm chứng

## Biến quyết định

Mỗi dòng PCCM có tổng `count`, giáo viên, lớp và mã môn/phân môn. `double_count` là số **cặp** tiết đôi: tạo `double_count` bloc dài 2 và `count - 2*double_count` bloc dài 1. Với mỗi loại bloc, ngày, ca, tiết bắt đầu và phòng được phép, tạo một biến Boolean `x`. Tổng các biến đặt bloc đúng bằng số bloc yêu cầu. Các bloc cùng loại không có định danh occurrence riêng, giảm đối xứng.

Một placement chỉ tồn tại khi thuộc ca lớp, nằm trọn trong buổi và không chạm lịch nghỉ của lớp/GV/phòng. Không suy ra nghỉ hoặc phòng từ tên môn. Nếu `room_ids` rỗng, chưa có yêu cầu phòng; khi khai báo nhiều phòng, solver chọn một phòng trong pool cho cả bloc. Phòng dùng chung được kiểm tra ở từng tiết. Phòng thường/khả năng chứa/địa điểm thực tế phải do đơn vị cung cấp, không được suy ra từ PCCM hiện tại.

## Ràng buộc cứng

1. Đúng tổng bloc/tiết từng PCCM, đúng mã GV/lớp/môn. Không có lớp/môn tự sinh.
2. Tổng các placement phủ một ô giáo viên/lớp/phòng ≤ 1. Tiết đôi phủ cả hai ô liên tiếp, không qua ca hoặc ngày.
3. Tổng tiết của mỗi GV/lớp/ngày/ca không vượt `max_teacher_session` / `max_class_session`.
4. Ca `morning` = am; `both` = am/pm; `mixed` = ca cụ thể của từng lớp.
5. Lịch nghỉ loại placement. `fixed` buộc placement tương ứng bằng 1. Hai tiết khóa trùng giờ dẫn tới INFEASIBLE, không tự bỏ khóa.
6. Xếp lại cục bộ khóa từng placement trước đó ngoài hợp của các lớp/GV được chọn. Phạm vi trống hoặc mã không tồn tại bị từ chối từ UI/API.

Dòng PCCM và tiết khóa có assumption literal phục vụ chẩn đoán. Kiểm tra trước các cận sức chứa cần thiết; nếu thiếu sức chứa, INFEASIBLE có chứng minh bằng cận cần thiết. Khi CP-SAT chứng minh vô nghiệm, xuất sufficient assumption core, **không khẳng định là core nhỏ nhất**. UNKNOWN không phải bằng chứng vô nghiệm. Không fallback tham lam, bỏ tiết, chia định danh GV hoặc nới ràng buộc cứng.

## Các mục tiêu mềm

Mặc định lexicographic: `gaps → visits → distribution → concentration → preferences → changes`. Có thể đổi thứ tự qua UI/JSON, phải đủ 6 mục tiêu, không trùng.

- **gaps**: tiết chưa dạy nằm giữa tiết đầu và cuối của GV trong cùng ngày/ca. Không tính khoảng nghỉ giữa sáng/chiều.
- **visits**: tổng số buổi ngày/ca có ít nhất một tiết của một GV; một ngày dạy hai ca tính hai buổi.
- **distribution**: tổng (max − min) số tiết trong ngày của từng lớp/môn gốc, gồm các phân môn cùng môn. Các ngày không có môn vẫn tính 0. Giảm độ lệch, không buộc các phân môn do nhiều GV thành cùng một phân công.
- **concentration**: tổng `max(0, số tiết một môn/lớp/ngày − 1)`. Đây là penalty tuyến tính cho dồn môn; không cấm tiết đôi hoặc áp số tiết môn tối đa không có trong dữ liệu.
- **preferences**: penalty trên các ô muốn tránh; `weight` không âm, mỗi tiết của bloc tính riêng. Muốn tuyệt đối nghỉ phải dùng unavailable.
- **changes**: số bloc cũ không còn giữ cùng PCCM/ngày/ca/tiết/độ dài/phòng. Không có baseline thì bằng 0. Đơn vị là bloc, không phải đếm riêng hai tiết trong cặp. Baseline lạ hoặc không phù hợp không được công nhận hợp lệ; hint không thay thế ràng buộc.

## Quy trình giải và proof

Đầu tiên CP-SAT chỉ giải mô hình cứng, dừng khi có lịch đủ. Sau đó thêm auxiliary variables cho soft objective và dùng **hint đầy đủ** của nghiệm đã có (placement, occupancy, gaps, session, daily extrema và assumptions). Warm start nhận lịch trước cho cả mô hình feasibility và optimization. Tất cả nghiệm bàn giao phải được CP-SAT tìm thấy và verifier độc lập chấp nhận; không bàn giao hint như nghiệm chưa được xác minh.

Tối ưu từng mục tiêu trong ngân sách còn lại; chỉ khóa giá trị và chuyển mục tiêu tiếp khi CP-SAT trả OPTIMAL. Nếu FEASIBLE/UNKNOWN, dừng mở rộng mục tiêu và giữ nghiệm tốt nhất đã xác minh. Do đó ưu tiên cao không bị đổi để cải thiện ưu tiên thấp. Ngân sách tính cả thời gian tạo mô hình; thời gian wall có thể vượt một chút do khởi tạo, dừng thread và hậu kiểm.

`FEASIBLE` nghĩa là lịch đủ và hợp lệ, chưa chứng minh đủ cả sáu mức. `OPTIMAL` chỉ khi mọi mức được chứng minh; có thể có mức hằng số không cần giải. Khi xếp lại cục bộ, proof chỉ cho mô hình có các tiết ngoài phạm vi bị khóa; `optimality_scope=local_frozen` và `global_optimal_proven=false`, không gọi là tối ưu toàn trường. Trong mô hình đầy đủ, global proof chỉ đúng cho cấu hình/giả định/dữ liệu đã giải, không đồng nghĩa nghiệm thu dữ liệu thực tế.

Mỗi phase ghi thời gian, objective và best_bound. 37 lớp trong lượt benchmark 30 giây chứng minh gaps=0 là OPTIMAL; mức visits là FEASIBLE, các mức sau chưa được tối ưu. Sau khi có nghiệm đủ, assumption literals được buộc cứng bằng 1 rồi bỏ giao diện assumptions để mở search song song/LNS; không đổi feasible set. Không dùng weighted sum lớn để giả lập proof lexicographic.

## Verifier và giới hạn

`validation.py` hậu kiểm không đọc biến CP-SAT: tái đếm tiết/PCCM, giáo viên/môn, lớp/GV/phòng trùng, ca, nghỉ, giới hạn/buổi, tiết đôi, tiết khóa, khóa ngoài phạm vi. Metrics được tính lại từ lịch; test nhỏ kiểm cả cận và giá trị penalty nguyện vọng có optimum tính tay.

37 lớp chỉ có 972 tiết đã phân công trong sheet 04. 111 tiết đặc biệt chưa có giáo viên vẫn hiển thị pending, không tạo giả. Phân môn L/H/S và toàn bộ GV vẫn REVIEW. Kết quả này không phải lịch hoàn chỉnh được nghiệm thu cho nhà trường. Model chưa hỗ trợ tiết đồng giảng nhiều GV, lớp ghép, tuần luân phiên, thời gian di chuyển hay phút thực tế; cần mô hình riêng trước khi dùng các nghiệp vụ đó.
