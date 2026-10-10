"""Build human reports from measured evidence, no solver calls."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent.parent
f=json.loads((R/'reports/FAIR_BENCHMARK.json').read_text())
L=['# Benchmark V3 / V3.1 thực thi','',f"Máy {f['platform']}, Python {f['python']}, OR-Tools {f['ortools']}, logical CPU={f['cpu_count']}. Chạy tuần tự14 lượt, {f['total_seconds']} giây.",'','## A. So sánh công bằng','', 'Cùng972 tiết,37 lớp,64 GV,6 ngày,5 tiết/buổi,giới hạn5. Mỗi cặp có cùng dữ liệu, seed, worker, ngân sách và cùng warm incumbent. V3.1 phase allocation/cuts/search là phần đánh giá. Không chạy solver khác đồng thời trong phần A.','', '| Chế độ | Profile (seed/worker/giây) | V3 buổi | V3.1 buổi | V3 phân bố | V3.1 phân bố | V3 dồn môn | V3.1 dồn môn |','|---|---|---:|---:|---:|---:|---:|---:|']
for mode in ['both','mixed']:
 for p in f['profiles']:
  old,new=[x for x in f['runs'] if x['mode']==mode and x['profile']==p['name']]
  a,b=old['result']['metrics'],new['result']['metrics']
  L.append(f"| {mode} | {p['name']} | {a['visits']} | {b['visits']} | {a['distribution']} | {b['distribution']} | {a['concentration']} | {b['concentration']} |")
L+=['','12 lượt có lịch:972/972,0 xung đột,0 tiết trống,FEASIBLE. Chỉ sáng ở cả hai:INFEASIBLE,0/972,không có lịch; GV01540>30 ô. Không lấy conflicts=0 trong log V3 cũ làm bằng chứng có lịch; V3.1 conflicts=null khi không có nghiệm.','', 'Sáng–chiều cold218→217, phân bố624→537. Warm45 giây cả hai217 nhưng phân bố639→498 và dồn môn251→100. Phân ca warm45 giây240→239, phân bố686→615. Phân ca cold30 giây V3.1 kém hơn240→248; warm worker1 giữ240, không cải thiện. Không bảo đảm một lượt ngắn bất kỳ tốt hơn V3. Nên dùng lịch hợp lệ làm warm start và đọc bound/phase. Multiworker có biến động; rerun có thể khác. Tập thử nhỏ, không khẳng định cải thiện mọi dữ liệu.','', '217 và239 chạm cận dưới buổi suy từ tải/ca. Các lượt warm45 giây có CP-SAT phase gaps/visits OPTIMAL; distribution/concentration FEASIBLE. Chỉ hai mức đầu đã chứng minh. Toàn lịch FEASIBLE, global_optimal_proven=false. Khóa incumbent không phải chứng minh.','', 'Objective,best_bound,seconds,status,proof_scope từng phase ghi đầy đủ trong FAIR_BENCHMARK.json và reports/fair/*.json. INDEPENDENT_EVIDENCE_CHECK.json hậu kiểm14 kết quả và tính lại chỉ số, không đọc biến CP-SAT.','', '| V3.1 bàn giao | Profile | Phân bố /100 | Dồn môn /100 | Giây | Chứng minh |','|---|---|---:|---:|---:|---|']
for mode in ['both','mixed']:
 x=json.loads((R/'reports'/(mode+'.json')).read_text());q=x['quality_scores']
 L.append(f"| {mode} | warm_s23_w4_t45 | {q['distribution_penalty_100']} | {q['concentration_penalty_100']} | {x['elapsed_seconds']} | gaps,visits; toàn lịch FEASIBLE |")
L+=['','## B. Mở rộng hoạt động','', 'Nguồn có0 tiết đặc biệt đủ quy tắc STRICT;111 pending. Phần A STRICT không công nhận1083 tiết chính thức. Fixture phần B chọn rõ74 activity_ids/111 tiết, giả định độc lập không cần GV; giả định do test harness chọn, lưu nguyên văn. Không tạo GV hoặc sửa workbook.','', '| SCENARIO | PCCM xếp | Giả định | Xung đột | Trống | Buổi GV | Trạng thái |','|---|---:|---:|---:|---:|---:|---|']
e=json.loads((R/'reports/EXTENDED_BENCHMARK.json').read_text())
for case in e['cases']:
 if case['mode']=='both_local_37':continue
 x=case['result'];m=x['metrics'] or {};conf=x['conflicts'] if x['conflicts'] is not None else 'Không có lịch'
 L.append(f"| {case['mode']} | {x['placed']}/{x['required']} | {x['scenario_placed']} | {conf} | {m.get('gaps','—')} | {m.get('visits','—')} | {x['status']} |")
L+=['','Hai chế độ có lịch:972 PCCM +111 mô phỏng=1083 ô lớp kỹ thuật; verified=0,pending chính thức=111,official_complete=false. Không công bố1083/1083 lịch xác minh. Kết quả phần B không dùng so chất lượng với phần A vì tập ô lớp khác. Xếp lại cục bộ37 lớp khóa ngoài C06A01 giữ0 thay đổi,0 trống,217 buổi; global_optimal_proven=false.','', '**OPTIMIZATION=PASS theo tiêu chí có cải thiện đo được trong benchmark công bằng; không bảo đảm mọi lượt cải thiện. DATA ACCEPTED=NO; WINDOWS ACCEPTED=NO; PRODUCTION READY=NO.**']
(R/'reports/BENCHMARK.md').write_text('\n'.join(L)+'\n')
(R/'reports/benchmark.json').write_text(json.dumps(dict(fair='FAIR_BENCHMARK.json',extended='EXTENDED_BENCHMARK.json',data_accepted=False,windows_accepted=False,production_ready=False),indent=2))
print('Benchmark report written from14 paired measured runs + extended evidence')
