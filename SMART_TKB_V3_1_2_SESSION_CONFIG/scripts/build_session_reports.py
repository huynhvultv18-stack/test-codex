"""Current reports from measured evidence; no new solver calls."""
from pathlib import Path
import json,shutil
R=Path(__file__).resolve().parent.parent;P=R/'reports'
def read(n):return json.loads((P/n).read_text())
b=read('SESSION_BENCHMARK.json');unit=read('SESSION_REGRESSION.json');browser=read('SESSION_BROWSER.json');old=read('SESSION_BROWSER_REGRESSION.json');verify=read('SESSION_INDEPENDENT_VERIFICATION.json');source=read('SESSION_SOURCE_IMMUTABILITY.json')
assert unit['success'] and not unit['failures'] and not unit['errors'];assert browser['status']=='PASS' and old['result']=='PASS';assert verify['status']==source['status']=='PASS';assert len(verify['runs'])==8
lines=['# Benchmark khối8 · V3.1.2','',b['scope'],'','Source37lớp được nhập và kiểm tra; chỉ9lớp khối8 được giải.234tiết môn học,27tiết đặc biệt PENDING;26mãGV chưa xác minh. Lịch nền738tiết giữ nguyên,84tiết đặc biệt lịch nền chưa biết. Mô phỏng kỹ thuật có nhãn; school_conflicts=null. Không nghiệm thu lịch thực tế. Ngân sách30s cho4profile chính,10s cho2chế độ bổ sung; workers4,seed17. Lượt giải chạy tuần tự; đọc báo cáo và kiểm tra browser smoke ngắn có thể tạo nhiễu OS. Wall bao gồm overhead Python/hậu kiểm; không phải thời gianCP thuần.','', '| Cấu hình | Cần/đã xếp | Công suất | Buổi nghỉ* | Xung đột trong khối/đã biết liên khối | Trống GV** | Buổi GV** | Giây | Trạng thái |','|---|---:|---:|---:|---|---:|---:|---:|---|']
for run in b['runs']:
 value=lambda k:'—' if run.get(k) is None else run[k]
 lines.append(f"| {run['name']} | {run['required']}/{run['placed']} | {run['capacity']} | {run['rest_sessions']} | {value('conflicts')}/{value('known_cross_grade_conflicts')} | {value('gaps')} | {value('visits')} | {run['elapsed_seconds']:.3f} | {run['status']} |")
lines+=['','*Buổi nghỉ cộng theo9lớp trên thứHai..thứBảy; chế độ morning/mixed tính cả buổi không được phép sử dụng. Sunday0/0 không cộng khi ẩn. **Trống/buổi GV tính trên hợp lịch nền đã biết và lịch khối8, không đếm buổi trống không có tiết. Buổi nền186; số tăng thêm có trong raw metrics.','', 'Reference: sáng5/5/5/5/5/4;chiều4/0/4/0/4/0. Mỗi lớp41ô,9buổi; toàn khối369ô,81buổi học,27buổi nghỉ. different_classes giảm riêng1tiết sáng từng lớp và thay chiều của4lớp, giữ đúng lựa chọn. Variable_days có378ô; uniform5/4 có486ô.','', '6lượt có nghiệm đều234/234,0xungđột trong khối/đã biết với lịch khóa; independent verifier và raw-calendar/occupancy audit PASS. Mọi lịch giữ SHA khối khóa. Không có chứng minh tối ưu các mục tiêu sau; trạng thái FEASIBLE,global_optimal_proven=false. Không so chất lượng giữa bài toán có miền khác nhau như một phép A/B.','', 'Mặc định thiếu nền:BLOCKED,solver_status=NOT_RUN,không có lịch và xung đột=null. Không gọi BLOCKED làINFEASIBLE. over_capacity:6ô/lớp<26tiết PCCM/lớp,INFEASIBLE bởi cận công suất; không tăng số tiết,không mở khóa. Chi tiết chẩn đoán:']
for run in b['runs']:
 if run['status']=='INFEASIBLE':lines+=['','```']+run['diagnostics']+['```']
lines+=['','Raw các phases,objective/bounds/locks/model_scope và calendar nằm trong reports/sessions/*.json. SESSION_INDEPENDENT_VERIFICATION.json tính lại metrics và kiểm5fileUIexport. WINDOWS ACCEPTED=NO; DATA ACCEPTED=NO; PRODUCTION READY=NO.']
(P/'SESSION_BENCHMARK.md').write_text('\n'.join(lines)+'\n')
(P/'SESSION_REGRESSION.md').write_text(f'''# Regression V3.1.2

PASS: **{unit['tests']} kiểm thử Python** (93 hồi quy +28lịch buổi), **{len(old['checks'])} kiểm tra browser hồi quy** và **{len(browser['checks'])} kiểm tra browser lịch buổi** trên Linux Chromium. Không xóa test gốc/tắt assertion. Lỗi trong quá trình phát triển đã được sửa và chạy lại; log hiện tại là lượt hoàn tất.

- Miền0..5 và mở rộng6/Sunday,buổi0/cả ngày0,khác ngày/lớp,công suất thiếu,tiết đôi tràn/nối buổi,khóa nghỉ,phòng/GV liên khối và giới hạn tải cộng nền.
- Rawcounts giữ nguyên; cấu hình sai/mã ngoài khối/bool/phân số bị từ chối. Metadata lịch buổi trong Excel không được làm tròn.
- Special STRICT/PENDING/SCENARIO/collective vẫn giữ; không sinh hoạt động vào buổi nghỉ hoặc tự xóa pending.
- Warm/incumbent/local,UNKNOWN ngân sách nhỏ,INFEASIBLE core/capacity; soft không đánh đổi HARD; scope chỉ khối.
- Confirmation trướcCP khi đổi số tiết ảnh hưởng lịch; fingerprint cũ bị từ chối,tắt warm vẫn cần xác nhận,hủy giữ lịch,đổi cấu hình+reload vẫn giữ trạng thái cũ có nhãn.
- UI grade/class/copy/apply/reset/save/restore/JSON/Sunday/capacity; không có ôN+1,NGHỈ shading; asyncimport khóa thao tác để tránh phản hồi cũ ghi đè; mở lại chỉnh buổi sau khi solver hoàn tất.
- 20luồng hồi quy gồm bootstrap9/234/26,bg738/84,CSRF/Host/CSP,backup lỗi atomic,lịch3chếđộ/234warm,CSV/XLSX/JSON/hash,đổi khối tương lai giữ lịch8 không giải9,mobile390/768/1366px,noJSerrors.
- 8benchmark được audit độc lập,6nghiệm234/234;5UIexports qua hậu kiểm,bao gồm Excel khối8thật.
- Baseline ZIP/tree1593file giữ nguyên; SOURCE và1336fileWindows runtime/wheel/provenance byte-identical. Chưa chạy Windows thật.

3testlegacy whole-school vẫn giữ nguyên trong source và chỉ loại khỏi runner riêng khối để tuân thủ phạm vi: {', '.join(x['test'] for x in unit['scope_exclusions'])}. Không chạy mô hình37lớp; UNKNOWN/công suất được cover theo khối8. Benchmark lịch sử không thay thế kiểm thử hiện tại.

Evidence: SESSION_REGRESSION.json/SESSION_REGRESSION_RUN.txt,SESSION_BROWSER_REGRESSION.json,SESSION_BROWSER.json,SESSION_INDEPENDENT_VERIFICATION.json,SESSION_SOURCE_IMMUTABILITY.json. Chi tiết số test/chạy/chưa chạy có trong JSON.

WINDOWS ACCEPTED=NO · DATA ACCEPTED=NO · PRODUCTION READY=NO.
''')
accept=dict(version='3.1.2-session-config-candidate',session_config='PASS',zero_period='PASS',cross_grade_lock='PASS',solver='PASS',cross_grade_conflict='BLOCKED: incomplete background; known occupancy checked',data_accepted=False,windows_accepted=False,production_ready=False,global_optimal_proven=False,python_tests=unit['tests'],browser_regression_checks=len(old['checks']),browser_session_checks=len(browser['checks']),benchmark_runs=8,feasible_verified=6,source_immutable=True,package='See adjacent PACKAGE_VERIFICATION.json after ZIP extraction/download verification',known_missing=dict(grade8_pending_special_periods=27,grade8_unverified_teacher_ids=26,background_pending_special_periods=84),windows_runtime='UNTESTED')
(P/'SESSION_ACCEPTANCE.json').write_text(json.dumps(accept,ensure_ascii=False,indent=2))
(P/'README.md').write_text('''# Báo cáo V3.1.2

SESSION_* là bằng chứng hiện tại. sessions/ chứa8lượt benchmark riêng khối8. historical_v311/ giữ toàn bộ báo cáo baseline V3.1.1 và lịch sửV3.1 bên trong; các báo cáo đó không nghiệm thu V3.1.2. SOURCE/baseline giữ nguyên; không chạy lại benchmark37lớp. Kiểm tra ZIP/SHA/manifest/giải nén/download nằm cạnh ZIP trong PACKAGE_VERIFICATION.json để tránh vòng checksum của gói tự chứa chính nó.
''')
print('Built current reports:',unit['tests'],'Python,',len(old['checks'])+len(browser['checks']),'browser checks')
