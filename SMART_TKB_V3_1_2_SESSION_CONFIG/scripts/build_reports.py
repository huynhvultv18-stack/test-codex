"""Generate current reports from measured A/B evidence; no optimization calls."""
import json,hashlib,statistics,shutil
from pathlib import Path
R=Path(__file__).resolve().parent.parent;P=R/'reports'
def read(p):return json.loads(p.read_text())
pairs=[]
for name,folder in [('AB_BENCHMARK.json','ab'),('AB_LNS_BENCHMARK.json','ab_lns')]:
 f=read(P/name)
 for run in f['runs']:
  path=R/run['file'];raw=read(path);perf=raw['observed_performance'];calls=perf['solver_calls']
  # Correct descriptive first-CP timing from recorded raw statuses. A warm
  # independently verified incumbent is different from a new CP solution.
  perf['first_cp_solution_seconds']=next((c['start_seconds']+c['seconds'] for c in calls if c['status'] in ('OPTIMAL','FEASIBLE')),None)
  raw['observed_performance']=perf;path.write_text(json.dumps(raw,ensure_ascii=False,indent=2));run['result']['observed_performance']=perf
 f['instrumentation_note']='first_cp_solution_seconds derived from first successful recorded CP call; UNKNOWN calls are not solutions. first verified incumbent timing in B performance.timings is separate.'
 (P/name).write_text(json.dumps(f,ensure_ascii=False,indent=2))
 for a,b in zip(f['runs'][::2],f['runs'][1::2]):
  ra,rb=a['result'],b['result'];ma,mb=ra['metrics'],rb['metrics']
  order=['gaps','visits','distribution','concentration','preferences','changes']
  outcome='CAPACITY_PROOF' if ma is None else 'BETTER' if tuple(mb[k] for k in order)<tuple(ma[k] for k in order) else 'WORSE' if tuple(mb[k] for k in order)>tuple(ma[k] for k in order) else 'EQUAL'
  pairs.append(dict(a=a,b=b,outcome=outcome))
f=read(P/'AB_BENCHMARK.json');counts={k:sum(p['outcome']==k for p in pairs) for k in ['BETTER','WORSE','EQUAL','CAPACITY_PROOF']};assert counts=={'BETTER':6,'WORSE':5,'EQUAL':1,'CAPACITY_PROOF':1},counts
lines=['# A/B · V3.1 baseline → Optimized Candidate','',f"{f['platform']}; Python {f['python']}; OR-Tools {f['ortools']}; logical CPU={f['logical_cpu']}. 26 lượt / 13 cặp, dữ liệu 37 lớp, 64 GV, 972 tiết PCCM. 18 lượt portfolio và 8 lượt LNS; seed 17/23/29, workers 4/1, time_limit 30 giây.",'','A là mã V3.1 từ ZIP SHA-256 a94c50bbe617c72210412ff5fa9b491d1bc2691fd6502fe7a35436ece04029e9; B là bản sửa. Mỗi cặp dùng cùng máy, JSON đầu vào được SHA, cấu hình, ngân sách, seed, worker và lịch warm nguồn. Chạy solver tuần tự trong process mới, không có solver khác chạy đồng thời. Các thao tác đọc báo cáo/browser ngắn trong thời gian đo có thể tạo nhiễu OS; nhiều worker không tất định, rerun có thể khác. Không dùng kết quả SCENARIO vào so sánh A/B 972 tiết. Tập benchmark nhỏ, không suy ra mọi dữ liệu.','', 'Portfolio đo checkpoint sau sửa solver; các kiểm tra tổng nguồn/importer/UI bổ sung sau đó không thay đổi mô hình trên đầu vào hợp lệ này. LNS chạy sau toàn bộ sửa code chức năng. Model-ready được instrument giống nhau ở validate(); wall gồm chuẩn bị projection, tạo mô hình, giải và hậu kiểm, không gồm mở Excel. RSS là process kernel high water mark MiB. Budget nominal 30s có overhead, không gọi wall 30.4s là đúng 30.0s.','', '| Chế độ/profile | Gap A→B | Buổi A→B | Distribution A→B | Concentration A→B | Changes A→B | So từ điển B/A |','|---|---:|---:|---:|---:|---:|---|']
for p in pairs:
 a,b=p['a'],p['b'];ma,mb=a['result']['metrics'],b['result']['metrics'];v=lambda k:f"{ma[k]} → {mb[k]}" if ma else '—'
 lines.append(f"| {a['mode']}/{a['profile']} | {v('gaps')} | {v('visits')} | {v('distribution')} | {v('concentration')} | {v('changes')} | {p['outcome']} |")
lines+=['','**6 cặp tốt hơn, 5 kém hơn, 1 bằng nhau; 1 cặp morning có cùng chứng minh vô nghiệm.** Không tính giảm changes là cải thiện khi distribution/visits ưu tiên cao hơn xấu đi. Tất cả 24 lịch khả thi đạt 972/972, 0 xung đột và 0 tiết trống, status FEASIBLE, không có chứng minh toàn cục. Chỉ sáng cả A/B: INFEASIBLE, 0/972, conflicts/metrics null, GV015 40 > 30 tiết công suất; không sửa giáo viên để ép nghiệm.','', '| Mode/profile | Model ready A/B s | Vars/constraints A/B | Wall A/B s | Peak RSS A/B MiB | CP calls A/B |','|---|---:|---|---:|---:|---:|']
for p in pairs:
 a,b=p['a'],p['b'];pa,pb=[x['result']['observed_performance'] for x in [a,b]]
 def ready(x):return f"{x['model_ready'][0]['seconds']:.3f}" if x['model_ready'] else '—'
 def size(x):return str(x['model_ready'][0]['variables'])+'/'+str(x['model_ready'][0]['constraints']) if x['model_ready'] else '—'
 lines.append(f"| {a['mode']}/{a['profile']} | {ready(pa)} / {ready(pb)} | {size(pa)} / {size(pb)} | {pa['wall_seconds']:.3f} / {pb['wall_seconds']:.3f} | {pa['peak_rss_mb']:.1f} / {pb['peak_rss_mb']:.1f} | {len(pa['solver_calls'])} / {len(pb['solver_calls'])} |")
lines+=['','Raw CP calls và phases ghi objective, best_bound, relative_gap, proof_scope và giây. Không có scalar objective/bound chung cho toàn bộ chuỗi từ điển; gap phase không phải global optimality gap. UNKNOWN phase có objective/gap null, giữ incumbent cũ đã hậu kiểm. PROVEN_LOWER_BOUND và VERIFIED_INCUMBENT là trạng thái ứng dụng, solver_status=null; không đổi thành CP OPTIMAL. First CP success và first verified incumbent tách nhau.','', 'Warm input cho both/mixed có gap=0 và buổi=217/239. Cận buổi được đạt bởi lịch hợp lệ nên hai mức đầu có chứng minh prefix, còn phân bố/dồn môn chưa chứng minh. Cold mixed B 243 < A245 nhưng chưa chạm cận239; không gọi 243 là tối ưu. Local37 khóa ngoài C06A01 đạt 0 thay đổi; proof_scope=local_frozen, global_optimal_proven=false.','', '| Result B chọn để minh họa, không phải cấu hình tối ưu cho mọi trường | Xếp/xung đột | Gap/buổi | Distribution/concentration | Giây/Peak MiB |','|---|---|---|---|---|']
for mode,filename in [('both','ab_lns/both_warm_lns_s17_w4_t30_B_OPTIMIZED.json'),('mixed','ab_lns/mixed_warm_lns_s23_w4_t30_B_OPTIMIZED.json')]:
 x=read(P/filename);shutil.copyfile(P/filename,P/(mode+'.json'));m=x['metrics'];perf=x['observed_performance'];q=x['quality_scores']
 lines.append(f"| {mode}, warm LNS seed {'17' if mode=='both' else '23'}, w4,30s | {x['placed']}/{x['required']}, {x['conflicts']} | {m['gaps']}/{m['visits']} | {m['distribution']}/{m['concentration']} (phạt /100 {q['distribution_penalty_100']}/{q['concentration_penalty_100']}) | {perf['wall_seconds']:.3f}/{perf['peak_rss_mb']:.1f} |")
lines+=['','Best A trên các profile thử: both distribution462 (LNS seed23), mixed587 (LNS seed17); best B466/596. Không tuyên bố B vượt best-of-seeds baseline. Portfolio warm both seed17/23 cải thiện ở cả hai seed; LNS không cải thiện đều. Khuyến nghị dùng incumbent đã kiểm tra, giữ priorities phù hợp và thử LNS khi có thời gian; không đổi mặc định theo một seed thắng.','', 'Mở rộng 37 lớp: SCENARIO both/mixed xếp972 tiết PCCM +111 mô phỏng, 0 xung đột; không công nhận1083 tiết chính thức. STRICT nguồn0 verified/approved,111 MISSING/PENDING. AB_INDEPENDENT_VERIFICATION.json kiểm26 kết quả và tính lại metrics bằng verifier hiện tại. EXTENDED_BENCHMARK.json tách fixture giả định.','', '**OPTIMIZATION = PASS theo tiêu chí có cải thiện đo được tại 6 profile và không làm xấu mục tiêu cao hơn trong những cặp đó. Phạm vi PASS có giới hạn; dominance mọi profile = FAIL (5 cặp kém hơn). Không chứng minh tối ưu toàn cục hoặc cấu hình thắng mọi seed.**']
(P/'AB_BENCHMARK.md').write_text('\n'.join(lines)+'\n');(P/'BENCHMARK.md').write_text('\n'.join(lines)+'\n')
valid=[p for p in pairs if p['outcome']!='CAPACITY_PROOF'];changes=[]
for p in valid:
 a,b=[x['result']['observed_performance'] for x in [p['a'],p['b']]];changes.append(100*(a['model_ready'][0]['seconds']-b['model_ready'][0]['seconds'])/a['model_ready'][0]['seconds'])
(P/'OPTIMIZATION.md').write_text(f'''# OPTIMIZATION · đo thực tế

PASS có phạm vi: 6/12 cặp khả thi cải thiện theo đúng thứ tự từ điển, 5 kém hơn, 1 bằng; không bảo đảm bản sửa luôn thắng hoặc thắng best-of-seeds baseline. B/A từng lượt ở AB_BENCHMARK.md. Hai mức ưu tiên đầu (0 gap, 217/239 visits warm) được giữ. Cold mixed 245→243 visits là cải thiện thật, cùng0 gap và972/972 tiết qua independent verifier.

Model-ready giảm trong cả12 cặp khả thi, median giảm {statistics.median(changes):.1f}%; không giảm số biến hay ràng buộc, không giảm peak memory đồng đều. Cache rule môn/khối và index unavailable loại bỏ lặp lookup, bỏ chỉ mục Python không dùng. BASELINE_MODEL_PROFILE.txt ghi bottleneck trước thay đổi.

Warm full schedule qua independent verifier được dùng làm incumbent ngay; tránh clone và CP feasibility, phase này chỉ mất thời gian verifier. Khi đạt cận phổ quát, gap/visits không cần chạy lại CP; objective=bound và proof riêng, solver_status=null. Warm portfolio w4 giảm6 CP calls còn3; worker1 giảm6 còn2. Thời gian tiết kiệm cấp cho các mục tiêu sau, nhưng thay quỹ đạo search có thể làm distribution cuối kém hơn A. Kiểm thử ngân sách0.001s giữ lịch warm hợp lệ; cold cùng ngân sách UNKNOWN không bị giả thành lịch.

LNS được thử A/B seed17/23,workers4,time30 với cùng warm input. Both seed17: distribution475→466,concentration76→61; seed23:462→472,58→67 (kém). Mixed seed17:587→600 (kém); seed23:604→596 (tốt). Không chọn default chỉ vì một seed. B minh họa both466/mixed596 vẫn kém best A462/587 trên toàn tập cấu hình.

Công thức và scope chứng minh ở ALGORITHM.md. 26 lượt A/B đều lưu raw phase status, objective, best bound, gap, timing, model size, peak RSS. Các kết quả toàn lịch là FEASIBLE; đạt cận visits không chứng minh chất lượng các mức sau. Lower bound không có incumbent không được dùng thay nghiệm.

OPTIMIZATION = PASS theo tiêu chí cải thiện có đo tại các profile nêu rõ; BASELINE DOMINANCE ALL PROFILES = FAIL. DATA ACCEPTED = NO; WINDOWS ACCEPTED = NO; PRODUCTION READY = NO.
''')
(P/'REGRESSION.md').write_text('''# REGRESSION · Optimized Candidate

REGRESSION = PASS trên Linux; không còn CRITICAL/HIGH đã biết chưa xử lý trong phạm vi rà soát. WINDOWS RUNTIME = UNTESTED.

- Baseline V3.1 đã chạy lại45 unit/20 browser PASS: BASELINE_UNIT_RERUN.txt, BASELINE_BROWSER_RERUN.txt.
- Bản sửa71 unit PASS (45 gốc +26 audit),28 browser checks PASS (20 gốc +8 audit). UNIT_REGRESSION.txt, UI_TESTS.json, UI_AUDIT_TESTS.json; không xóa test hoặc tắt assertion.
- 26 lượt A/B37 lớp được hậu kiểm bằng verifier hiện tại, SHA đầu vào và metrics tính lại: AB_INDEPENDENT_VERIFICATION.json PASS. 24 lịch972/972,0 conflicts/0 gaps; morning2 trường hợp INFEASIBLE với proof40>30.
- Unit cover HARD GV/lớp/phòng/PCCM/ca/nghỉ/khóa/tiết đôi/giới hạn; status OPTIMAL nhỏ, FEASIBLE37, INFEASIBLE proof/core, UNKNOWN không fake lịch; warm hợp lệ/không hợp lệ, local freeze/khóa mâu thuẫn, objective/bound/weight/grade/soft/hard/prefs.
- Audit: forged marker, source inventory bỏ/sửa, pending totals, fractional/bool time, malformed list/row, CSV literal formula/reversible ID, Excel fraction/columns, finite config, approved rule note/missing/conflict, không mutate SOURCE, dòng tổng thiếu/trùng.
- Integration/browser: Excel nguồn5 sheet, JSON V2/V3/V3.1, backup atomic khi mạng lỗi, CSV/XLSX roundtrip, ca từng lớp, live solve và live SCENARIO; giữ collective/fixed rules; bảng buổi/biểu đồ/lịch/so sánh, tiến độ,6 mục tiêu; mobile/tablet/desktop.
- Host/Origin/CSRF và CSP self, không có request ngoại mạng, không có native browser errors, JSON NaN bị từ chối. Không có nghiệm thì không hiển thị0 xung đột.
- Extended37: STRICT111 pending nguồn; SCENARIO chỉ fixture với lựa chọn74activity_ids/111 tiết và nhãn giả định, both/mixed xếp972+111 kỹ thuật; local37 ngoàiC06A01 giữ0 changes và global proof=false. EXTENDED_BENCHMARK.json.
- Offline Windows dependency resolution win_amd64/cp312 với no-index/hash đạt; runtime/wheel byte kiểm với baseline. WINDOWS_INTEGRITY.json và WINDOWS_OFFLINE_RESOLUTION.json. Không chạy PE/Windows batch trên Linux.

PACKAGING sau khi tạo ZIP: xem PACKAGE_VERIFICATION.json ở workspace/repository và log extracted unit/browser riêng. Không dùng log PACKAGE_UNIT_TESTS cũ ở historical_v31 như nghiệm thu hiện tại.

DATA ACCEPTED = NO · WINDOWS ACCEPTED = NO · PRODUCTION READY = NO.
''')
accept={k:{'status':'PASS','evidence':v} for k,v in [('AUDIT','FULL_AUDIT.md + BUGFIX.md'),('SOLVER','AB_INDEPENDENT_VERIFICATION.json + UNIT_REGRESSION.txt'),('REGRESSION','71 unit +28 browser; CRITICAL/HIGH known unresolved=0'),('SPECIAL_ACTIVITY','source111 MISSING/PENDING, APPROVED/VERIFIED/SCENARIO tests')]}
accept['OPTIMIZATION']=dict(status='PASS',scope='6/12 feasible pairs improve lexicographically without worsening higher-priority goals in those winning pairs; not general superiority',worse_pairs=5,equal_pairs=1,evidence='AB_BENCHMARK.md + OPTIMIZATION.md')
accept['BASELINE_DOMINANCE_ALL_PROFILES']=dict(status='FAIL',reason='5 worse pairs; best-of-seeds A distribution462/587 vs B466/596')
accept['PACKAGE']=dict(status='PENDING',reason='Finalize archive, extract/check manifest, verify download')
accept['WINDOWS_RUNTIME']=dict(status='BLOCKED',runtime='UNTESTED',reason='Linux environment; no real Windows execution')
(P/'ACCEPTANCE.json').write_text(json.dumps(dict(criteria=accept,data_accepted=False,windows_accepted=False,production_ready=False),ensure_ascii=False,indent=2))
print('Built current A/B, optimization, regression and acceptance reports:',counts)
