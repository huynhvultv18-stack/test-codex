# BENCHMARK — 37 lớp, CP-SAT V3 Candidate

**Kiểm thử kỹ thuật có điều kiện; DATA ACCEPTED = NO; PRODUCTION READY = NO.**

Máy kiểm thử: Linux-6.18.44-x86_64-with-glibc2.41; Python 3.12.14; OR-Tools 9.15.6755; CPU logical host báo 5, solver dùng 4 worker. Seed 17; chạy trên Linux/cloud, không phải Windows.

Cấu hình nguồn: 6 ngày, 5 tiết/buổi, tối đa 5 tiết lớp/GV/buổi, 30 giây/lượt. Chỉ 972 tiết có PCCM được giải; 111 tiết đặc biệt chưa có giáo viên vẫn pending. Không tự đặt phòng/nghỉ/tiết khóa trong benchmark nguồn.

| Chế độ | Cần xếp | Đã xếp | Xung đột | Tiết trống GV | Buổi lên trường | Giây thực đo | Trạng thái |
|---|---:|---:|---:|---:|---:|---:|---|
| Chỉ sáng | 972 | 0 | — (không có lịch) | — | — | 0.006 | INFEASIBLE |
| Sáng–chiều | 972 | 972 | 0 | 0 | 218 | 30.274 | FEASIBLE |
| Phân ca kỹ thuật | 972 | 972 | 0 | 0 | 240 | 30.28 | FEASIBLE |

Chỉ sáng: GV015 — Thầy Độ có 40 tiết > 30 ô; INFEASIBLE có chứng minh capacity bound, không tự sửa định danh hay giảm tiết. Không có lịch thì không dùng số 0 xung đột để nói lịch hợp lệ.

Phân ca kỹ thuật: 37 lớp theo thứ tự workbook được chia xen kẽ am/pm (19 sáng, 18 chiều). Ánh xạ đầy đủ trong benchmark.json. Đây là giả định kiểm thử, không phải ca đã được nhà trường phê duyệt.

## Chất lượng và chứng minh

### Sáng–chiều

Nghiệm đủ ban đầu: 51 tiết trống, 272 buổi GV. Sau tối ưu: 0 tiết trống, 218 buổi GV; distribution=638, concentration=251, preferences=0, changes=0.

Mức đã chứng minh: gaps. global_optimal_proven=False. Nghiệm tổng thể vẫn FEASIBLE; các mục tiêu phía sau mức dừng chưa được tối ưu lexicographic.

| Phase | Trạng thái | Mục tiêu | Cận | Giây |
|---|---|---:|---:|---:|
| feasibility | OPTIMAL | 0.0 | 0.0 | 0.953 |
| gaps | OPTIMAL | 0.0 | 0.0 | 3.56 |
| visits | FEASIBLE | 218.0 | 38.0 | 24.71 |

### Phân ca kỹ thuật

Nghiệm đủ ban đầu: 95 tiết trống, 370 buổi GV. Sau tối ưu: 0 tiết trống, 240 buổi GV; distribution=694, concentration=311, preferences=0, changes=0.

Mức đã chứng minh: gaps. global_optimal_proven=False. Nghiệm tổng thể vẫn FEASIBLE; các mục tiêu phía sau mức dừng chưa được tối ưu lexicographic.

| Phase | Trạng thái | Mục tiêu | Cận | Giây |
|---|---|---:|---:|---:|
| feasibility | OPTIMAL | 0.0 | 0.0 | 0.339 |
| gaps | OPTIMAL | 0.0 | 0.0 | 1.533 |
| visits | FEASIBLE | 240.0 | 133.0 | 27.6 |

## Warm start / xếp lại cục bộ 37 lớp

Dùng nghiệm sáng–chiều, chọn C06A01 và khóa ngoài phạm vi; ưu tiên changes trước. Đã xếp 972/972 tiết, 0 xung đột, 0 bloc đổi, thời gian 4.531 giây. Trạng thái OPTIMAL chỉ trong mô hình có khóa ngoài phạm vi: optimality_scope=local_frozen; global_optimal_proven=False. Không coi proof cục bộ là proof tối ưu toàn trường.

## Kiểm thử và cách lặp lại

23 unit test PASS (UNIT_TESTS.txt): đếm số tiết, trùng GV/lớp/phòng, 3 chế độ, tiết đôi, lịch nghỉ/tiết khóa, giới hạn/buổi, định danh chưa xác minh, dữ liệu trùng/thiếu, bổ sung hoạt động đặc biệt có điều kiện, warm start/xếp lại, proof nguyện vọng và verifier độc lập.

12 browser check PASS (UI_TESTS.json): workbook thực tế, cảnh báo, ca lớp, chẩn đoán vô nghiệm, khôi phục nghiệm và hậu kiểm, CSV/JSON, chuyển V2, API CP-SAT, CSRF/Origin, responsive, không lỗi JS/không request ngoài.

WINDOWS_OFFLINE_RESOLUTION.txt: pip dry-run trên Linux với target win_amd64/cp312, --no-index và --require-hashes đã tìm đủ 12 dependency. Đây là kiểm tra closure/hash, chưa phải thực thi DLL/ứng dụng trên Windows.

```sh
python -m unittest discover -s tests -v
python tests/benchmark.py --seconds 30 --local
# Từ terminal khác, sau khi khởi động server; Node/Playwright chỉ dùng cho harness:
node tests/browser.cjs
```

INFEASIBLE/UNKNOWN/FEASIBLE/OPTIMAL được test riêng; không có zero-test pass, không tắt assertion. Các kết quả benchmark có thể thay đổi giữa máy/lượt do search nhiều worker và giới hạn wall time. Không nghiệm thu thực tế khi PCCM/phòng/quy định chưa đủ; Windows còn UNRUN.
