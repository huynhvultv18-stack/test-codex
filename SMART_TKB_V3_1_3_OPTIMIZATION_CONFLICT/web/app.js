'use strict';
const $=id=>document.getElementById(id),KEY='smart_tkb_thcs_v3_1_3_time_conflict_candidate';
let sessionProfiles={},calendarRequest=0;
let data,config,token,result=null,solvedSnapshot='',tableView='teachers',busy=false,baseline={},specialContext=null,background=null,backgroundContext=null;
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const msg=t=>$('message').textContent=t;
async function api(path,payload){if(payload&&!Object.hasOwn(payload,'background'))payload={background,...payload};const r=await fetch(path,payload?{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':token},body:JSON.stringify(payload)}:{});const b=await r.json();if(!r.ok)throw Error(b.error||'Yêu cầu không thành công');return b;}
function download(content,name,type='application/json'){const url=URL.createObjectURL(new Blob([content],{type})),a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
function save(){try{localStorage.setItem(KEY,JSON.stringify({version:'3.1.3-time-conflict',data,config,background,result,solvedSnapshot,sessionProfiles}));}catch(e){msg('Dữ liệu đang ở phiên hiện tại; lưu trình duyệt thất bại. Hãy tải bản sao JSON.');}}
function stable(x){return Array.isArray(x)?x.map(stable):x&&typeof x==='object'?Object.fromEntries(Object.keys(x).sort().map(k=>[k,stable(x[k])])):x;}
function snapshot(){return JSON.stringify(stable({data,config,background}));}
function lockEditing(value){document.querySelectorAll('#grade-controls input,#grade-controls select,#grade-controls button,#optimize,#check-grade,#config input,#config select,#config textarea,#special input,#special select,#dataset input,#dataset select,input[type=file],#validate,#backup,#warm,#local,#scope,#post-check,#confirm-schedule,#conflicts-xlsx,#conflicts-print,#manual-apply').forEach(el=>{if(value){el.dataset.wasDisabled=String(el.disabled);el.disabled=true;}else if(el.dataset.wasDisabled!==undefined){el.disabled=el.dataset.wasDisabled==='true';delete el.dataset.wasDisabled;}});}
function stale(){return result&&solvedSnapshot!==snapshot();}
function readConfig(){
 const advanced=JSON.parse($('advanced').value);for(const k of Object.keys(advanced))if(!ADVANCED.includes(k))throw Error('Trường JSON bổ sung chưa được hỗ trợ: '+k);
 config={...config,...advanced,mode:$('mode').value,priorities:$('priorities').value.split(',')};
 for(const id of ['max_class_session','max_teacher_session','time_limit','seed','workers'])config[id]=Number($(id).value);
 config.target_grade=Number($('target_grade').value);ensureCalendar();config.days=7;config.periods=Math.max(config.periods||1,config.session_config.max_periods);config.allow_incomplete_background=$('simulate-background').checked;config.background_assumption=$('background-assumption').value;
 config.search_mode=$('search_mode').value;config.special_mode=$('special_mode').value;
 config.objective_settings=Object.fromEntries(config.priorities.map(k=>[k,{enabled:document.querySelector('[data-objective="'+k+'"]').checked,weight:Number(document.querySelector('[data-weight="'+k+'"]').value)}]));
 if(config.special_mode==='SCENARIO')config.special_scenario={...config.special_scenario,enabled:true,activity_ids:[...document.querySelectorAll('[data-activity]:checked')].map(x=>x.dataset.activity),teacher_required:$('scenario-teacher').value==='true',teacher_id:$('scenario-teacher').value==='true'?($('scenario-gv').value||null):null,scheduling_policy:$('scenario-policy').value,shared_teacher_group:$('scenario-group').value||null,assumption_label:$('assumption').value};
 config.teacher_time={...config.teacher_time,enabled:$('teacher-enabled').checked,mode:$('teacher-mode').value,priorities:$('teacher-priorities').value.split(',').map(x=>x.trim()),waiting_enabled:$('waiting-enabled').checked,fairness_enabled:$('fairness-enabled').checked,seeds:$('teacher-seeds').value.split(',').map(x=>x.trim()).filter(Boolean).map(Number),period_times:JSON.parse($('period-times').value),lunch_break:JSON.parse($('lunch-break').value)};
 config.technical_only=true;
 return config;
}
const ADVANCED=['rooms','unavailable','fixed','preferences','phase_fractions','advance_on_incumbent','subject_rules','subject_hard_limits','heavy_subjects','heavy_run_limit','heavy_weight','special_overrides'];
const DEFAULT_ADVANCED={phase_fractions:{gaps:.25,visits:.5,distribution:.16,concentration:.06,preferences:.02,changes:.01},advance_on_incumbent:true,heavy_run_limit:2,heavy_weight:0};
const GOALS={gaps:'Tiết trống GV',visits:'Buổi GV',distribution:'Phân bố',concentration:'Dồn môn / liên tiếp',preferences:'Nguyện vọng',changes:'Thay đổi lịch cũ'};
function configUI(){ensureCalendar();renderCalendar();$('target_grade').value=config.target_grade;$('simulate-background').checked=config.allow_incomplete_background;$('background-assumption').value=config.background_assumption; for(const id of ['mode','days','periods','max_class_session','max_teacher_session','time_limit','seed','workers','search_mode','special_mode'])$(id).value=config[id];
 const priority=config.priorities.join(',');if(![...$('priorities').options].some(o=>o.value===priority))$('priorities').add(new Option(priority,priority));$('priorities').value=priority;
 $('objective-table').innerHTML='<table><tr><th>Mục tiêu</th><th>Bật</th><th>Trọng số</th></tr>'+Object.entries(GOALS).map(([k,v])=>`<tr><td>${v}</td><td><input data-objective="${k}" type="checkbox" ${config.objective_settings?.[k]?.enabled===false?'':'checked'} aria-label="Bật ${v}"></td><td><input data-weight="${k}" type="number" min="1" max="100" value="${config.objective_settings?.[k]?.weight||1}" aria-label="Trọng số ${v}"></td></tr>`).join('')+'</table>';
 $('assumption').value=config.special_scenario?.assumption_label||'';$('scenario-teacher').value=String(config.special_scenario?.teacher_required===true);$('scenario-gv').value=config.special_scenario?.teacher_id||'';
 $('scenario-policy').value=config.special_scenario?.scheduling_policy||'independent';$('scenario-group').value=config.special_scenario?.shared_teacher_group||'';
 const tt=config.teacher_time||{};$('teacher-enabled').checked=tt.enabled===true;$('teacher-mode').value=tt.mode||'BALANCED';$('teacher-priorities').value=(tt.priorities||['gaps','visits','days','waiting','fragmentation','distribution','preferences','fairness','concentration','changes']).join(',');$('teacher-seeds').value=(tt.seeds||[]).join(',');$('waiting-enabled').checked=tt.waiting_enabled===true;$('fairness-enabled').checked=tt.fairness_enabled!==false;$('period-times').value=JSON.stringify(tt.period_times||[],null,2);$('lunch-break').value=JSON.stringify(tt.lunch_break??null);
 $('advanced').value=JSON.stringify(Object.fromEntries(ADVANCED.map(k=>[k,config[k]??DEFAULT_ADVANCED[k]??[]])),null,2);
}
function activeClasses(){return data.classes.filter(c=>c.grade===config.target_grade);}
function activeAssignments(){const ids=new Set(activeClasses().map(c=>c.id));return data.assignments.filter(a=>ids.has(a.class_id));}
function activeTeachers(){const ids=new Set(activeAssignments().flatMap(a=>[a.teacher,...(a.co_teacher_ids||[])]));return data.teachers.filter(t=>ids.has(t.id));}
function activePending(){const ids=new Set(activeClasses().map(c=>c.id));return data.pending_special.filter(a=>ids.has(a.class_id));}
function render(){
 $('nc').textContent=activeClasses().length;$('nt').textContent=activeTeachers().length;
 $('nr').textContent=activeAssignments().reduce((s,a)=>s+a.count,0);$('np').textContent=result?.placed||0;
 const pending=activePending().reduce((s,x)=>s+x.count,0),unverified=activeTeachers().filter(t=>t.status!=='VERIFIED'||!t.full_name).length;
 $('special-title').textContent=pending+' tiết đặc biệt · kiểm kê theo nguồn';
 $('trust').textContent=`KIỂM THỬ KỸ THUẬT CÓ ĐIỀU KIỆN · ${unverified} định danh GV chưa xác minh. ${pending} tiết hoạt động đặc biệt chưa có PCCM giáo viên, không được tự xếp. Tổng đối chiếu: ${Number($('nr').textContent)+pending} tiết. ${result?.simulation?'MÔ PHỎNG KỸ THUẬT · không dùng chính thức. ':''}${stale()?'Lịch đang hiển thị đã cũ so với dữ liệu/cấu hình; cần giải lại.':''}`;
 $('solve').textContent='✦ Xếp TKB khối '+config.target_grade;$('optimize').textContent='Tối ưu lại khối '+config.target_grade;document.querySelector('h1').textContent='XẾP TKB KHỐI '+config.target_grade;renderCalendar();refreshCalendarAnalysis();renderBackground();renderGrid();renderDataset();renderResult();renderAnalytics();renderPostCheck();renderTeacherTime();refreshSpecial();
}
function renderGrid(){
 const type=$('viewtype').value,old=$('viewer').value,items=type==='classes'?activeClasses():activeTeachers();
 $('viewer').innerHTML=items.map(x=>`<option value="${esc(x.id)}">${esc(x.name)} (${esc(x.id)})</option>`).join('');if(items.some(x=>x.id===old))$('viewer').value=old;
 const id=$('viewer').value,cl=data.classes.find(x=>x.id===id),locked=type==='teachers'?(result?.locked_lessons||background?.lessons?.filter(l=>!activeClasses().some(c=>c.id===l.class_id))||[]):[],lessons=[...(result?.lessons||[]),...locked];
 const days=Array.from({length:config.session_config.include_sunday||locked.some(l=>l.day===6)?7:6},(_,d)=>d);
 let h='<thead><tr><th>Buổi / Tiết</th>'+days.map(d=>`<th>${DAYS[d]}</th>`).join('')+'</tr></thead><tbody>';
 for(const sh of ['am','pm']){
  h+=`<tr><th class="shift" colspan="${days.length+1}">${sh==='am'?'☀ BUỔI SÁNG':'◐ BUỔI CHIỀU'}</th></tr>`;
  const counts=days.map(d=>type==='classes'?effectiveCount(cl,d,sh):Math.max(0,...activeClasses().map(c=>effectiveCount(c,d,sh)),...locked.filter(l=>l.day===d&&l.shift===sh&&[l.teacher,...(l.co_teacher_ids||[])].includes(id)).map(l=>l.period+l.length)));
  const height=Math.max(1,...counts);
  for(let p=0;p<height;p++){
   h+=`<tr><th>${Math.max(...counts)>0?'Tiết '+(p+1):'Nghỉ'}</th>`;
   for(let di=0;di<days.length;di++){
    const d=days[di],n=counts[di];
    if(p>=n){if(p===n)h+=`<td class="rest" rowspan="${height-n}" data-rest-day="${d}" data-rest-shift="${sh}">${n===0?'NGHỈ':'Hết buổi · '+n+' tiết'}</td>`;continue;}
    const l=lessons.find(l=>l.day===d&&l.shift===sh&&p>=l.period&&p<l.period+l.length&&(type==='classes'?(l.class_ids||[l.class_id]).includes(id):[l.teacher,...(l.co_teacher_ids||[])].includes(id)));
    const a=l&&data.assignments.find(a=>a.id===l.assignment),sub=a&&data.subjects.find(s=>s.id===a.subject_id),secondary=l&&(type==='classes'?data.teachers.find(t=>t.id===l.teacher)?.name:data.classes.find(c=>c.id===l.class_id)?.name);
    h+=`<td ${l&&result?.lessons?.includes(l)?'data-edit-index="'+result.lessons.indexOf(l)+'" tabindex="0" title="Nhấp để chuyển tiết"':''} data-slot-day="${d}" data-slot-shift="${sh}" data-slot-period="${p}">`+(l?`<div class="lesson"><b>${esc(a?.subject||l.subject)}${sub?.sub_name?' · '+esc(sub.sub_name):''}</b><small>${esc(secondary)}</small>${l.room?'<small>'+esc(l.room)+'</small>':''}${!activeClasses().some(c=>c.id===l.class_id)?'<small>🔒 LỊCH KHỐI KHÁC</small>':''}${l.activity_status==='SCENARIO'?'<small>MÔ PHỎNG</small>':''}${l.length===2?'<small>↔ Tiết đôi</small>':''}</div>`:'—')+'</td>';
   }h+='</tr>';
  }
 }$('grid').innerHTML=h+'</tbody>';$('empty').hidden=Boolean(result?.lessons?.length);
}
function renderDataset(){
 let h='';
 if(tableView==='issues'){h=data.issues.map(i=>`<div class="warning ${i.level==='ERROR'?'error':''}"><b>${esc(i.code)}</b> · ${esc(i.message)}</div>`).join('');
  h+='<h3>Hoạt động chưa có phân công</h3><table><tr><th>Lớp</th><th>Hoạt động</th><th>Tiết</th></tr>'+activePending().map(x=>`<tr><td>${esc(x.class_id)}</td><td>${esc(x.subject)}</td><td>${x.count}</td></tr>`).join('')+'</table>';
 }else if(tableView==='teachers'){h='<table><tr><th>Mã</th><th>Nhãn nguồn</th><th>Họ tên đầy đủ</th><th>Định danh</th><th>Tiết PCCM</th></tr>'+activeTeachers().map(t=>`<tr><td>${esc(t.id)}</td><td>${esc(t.name)}</td><td>${esc(t.full_name||'Chưa xác minh')}</td><td>${esc(t.status)}</td><td>${data.assignments.filter(a=>a.teacher===t.id).reduce((s,a)=>s+a.count,0)}</td></tr>`).join('')+'</table>';
 }else if(tableView==='classes'){h='<table><tr><th>Mã lớp</th><th>Lớp</th><th>Ca học (chế độ phân ca)</th><th>Tiết môn học</th></tr>'+activeClasses().map(c=>`<tr><td>${esc(c.id)}</td><td>${esc(c.name)}</td><td><select data-class="${esc(c.id)}" aria-label="Ca ${esc(c.name)}"><option value="am" ${c.shift==='am'?'selected':''}>Sáng</option><option value="pm" ${c.shift==='pm'?'selected':''}>Chiều</option></select></td><td>${data.assignments.filter(a=>a.class_id===c.id).reduce((s,a)=>s+a.count,0)}</td></tr>`).join('')+'</table>';
 }else{h='<table><tr><th>PCCM</th><th>GV</th><th>Lớp</th><th>Môn / phân môn</th><th>Tiết</th><th>Cặp tiết đôi</th><th>Mã phòng được phép</th></tr>'+activeAssignments().map(a=>`<tr><td title="${esc(a.source_cells)}">${esc(a.id)} · dòng ${a.source_row||'V2'}</td><td>${esc(a.teacher)}</td><td>${esc(a.class_id)}</td><td>${esc(a.subject)} · ${esc(a.sub)}</td><td>${a.count}</td><td><input data-double="${esc(a.id)}" type="number" min="0" max="${Math.floor(a.count/2)}" value="${a.double_count}" aria-label="Cặp tiết đôi ${esc(a.id)}"></td><td><input data-rooms="${esc(a.id)}" value="${esc(a.room_ids.join(','))}" placeholder="TIN01" aria-label="Phòng ${esc(a.id)}"></td></tr>`).join('')+'</table>';
 }$('dataset').innerHTML=h;
}
function renderResult(){
 if(!result){$('result').textContent='Chưa có kết quả giải.';return;}
 const m=result.metrics||{},labels={gaps:'Tiết trống GV',visits:'Buổi lên trường GV',distribution:'Độ lệch phân bố',concentration:'Dồn môn trong ngày',days:'Ngày lên trường GV',waiting:'Chờ sáng–chiều (xem đơn vị)',fragmentation:'Cụm tiết',fairness:'Tiết trống lớn nhất/GV',preferences:'Phạt nguyện vọng',changes:'Bloc cũ thay đổi'};
 let h=`<p>GRADE SCHEDULING: ${esc(result.grade_scheduling)} · CROSS-GRADE: ${esc(result.cross_grade_conflict)} · LOCKED GRADES: ${esc(result.locked_grades)}</p><p>Xung đột đã biết với lịch khóa: ${result.known_cross_grade_conflicts??'Chưa kiểm tra'} · Xung đột toàn trường: ${result.school_conflicts??'CHƯA XÁC MINH'}</p><p>Buổi GV lịch nền: ${m.baseline_visits??'—'} · Buổi tăng thêm: ${m.added_visits??'—'} · Phạm vi chứng minh: ${esc(result.optimality_scope)}</p><div class="status ${esc(result.status)}">${esc(result.status)} ${stale()?'· LỊCH CŨ / CẦN GIẢI LẠI':''}</div><p>${result.placed} / ${result.required} tiết PCCM / hoạt động đủ quy tắc · ${result.lessons?.length?result.conflicts+' xung đột':'Không có lịch; chưa có số xung đột'} · ${result.elapsed_seconds==null?'Nhập lịch; không chạy bộ giải':result.elapsed_seconds+' giây'} · ${result.unscheduled_special} tiết đặc biệt chưa có PCCM.</p>`;
 h+=result.simulation?`<div class="warning">MÔ PHỎNG: ${result.scenario_placed} tiết giả định, chưa xác minh. ${esc((result.scenario_assumptions||[]).join('; '))}</div>`:'';
 h+='<div class="quality-grid">'+Object.entries(labels).map(([k,v])=>`<div>${v}<b>${m[k]??'—'}</b></div>`).join('')+'</div>';
 h+=`<p>Chứng minh tối ưu toàn cục theo cấu hình: ${result.global_optimal_proven?'CÓ':'CHƯA'}. ${result.optimality_scope==='local_frozen'?'Kết quả chỉ xét phạm vi cục bộ với các tiết ngoài phạm vi đã khóa. ':''}Mức ưu tiên đã chứng minh: ${esc((result.proven_priorities||[]).join(', ')||'Chưa có')}.</p>`;
 h+=(result.diagnostics||[]).map(x=>`<div class="warning">${esc(x)}</div>`).join('');
 h+='<table><tr><th>Giai đoạn</th><th>Trạng thái</th><th>Mục tiêu</th><th>Cận</th><th>Gap</th><th>Phạm vi chứng minh</th><th>Seed</th><th>Giây</th></tr>'+(result.phases||[]).map(p=>`<tr><td>${esc(p.name)}</td><td>${esc(p.status==='VERIFIED_INCUMBENT'?'Nghiệm trước đã hậu kiểm':p.status==='PROVEN_LOWER_BOUND'?'Nghiệm đạt cận dưới':p.status)}</td><td>${p.objective??'—'}</td><td>${p.best_bound??'—'}</td><td>${p.relative_gap??'—'}</td><td>${esc(p.proof_scope||'—')}</td><td>${esc((p.trials||[]).map(x=>x.seed+':'+x.status).join(', '))}</td><td>${p.seconds}</td></tr>`).join('')+'</table>';
 h+=`<p>Khóa nghiệm chưa chứng minh: ${esc(JSON.stringify(result.incumbent_locks||{}))}. Các mức tối ưu chỉ có điều kiện: ${esc((result.conditional_optimal_priorities||[]).join(', ')||'—')}.</p>`;
 if(result.quality_scores)h+=`<p>Phạt phân bố /100 (thấp tốt hơn): ${result.initial_quality_scores?.distribution_penalty_100??'—'} → ${result.quality_scores.distribution_penalty_100}. Phạt dồn môn /100: ${result.initial_quality_scores?.concentration_penalty_100??'—'} → ${result.quality_scores.concentration_penalty_100}.</p>`;
 if(result.performance)h+=`<p>Tạo mô hình: ${result.performance.timings?.model_build_seconds??'—'} giây · ${result.performance.model?.variables??'—'} biến / ${result.performance.model?.constraints??'—'} ràng buộc · nghiệm đầu: ${result.performance.timings?.first_solution_seconds??'—'} giây.</p>`;
 if(result.verification)h+=`<p>Kiểm tra độc lập: ${result.verification.valid?'ĐẠT':'KHÔNG ĐẠT'}; đúng số tiết, giáo viên/môn, ca học, phòng, lịch nghỉ, tiết cố định, tiết đôi và phạm vi xếp lại.</p>`;
 $('result').innerHTML=h;
}
function showTab(id){document.querySelectorAll('main > section').forEach(x=>x.classList.toggle('hidden',x.id!==id&&!(x.id==='grade-controls'&&['schedule','config'].includes(id))));document.querySelectorAll('nav button').forEach(x=>x.classList.toggle('active',x.dataset.tab===id));}
function guard(fn){return async(...args)=>{try{await fn(...args);}catch(e){msg(e.message);}};}
document.querySelectorAll('[data-tab]').forEach(b=>b.onclick=()=>showTab(b.dataset.tab));
$('viewtype').onchange=renderGrid;$('viewer').onchange=renderGrid;
for(const kind of ['teachers','classes','assignments','issues'])$('show-'+kind).onclick=()=>{tableView=kind;renderDataset();};
$('dataset').onchange=guard(e=>{const t=e.target;if(busy)throw Error('Chờ bộ giải kết thúc trước khi sửa dữ liệu.');
 if(t.dataset.class)data.classes.find(c=>c.id===t.dataset.class).shift=t.value;
 if(t.dataset.double)data.assignments.find(a=>a.id===t.dataset.double).double_count=Number(t.value);
 if(t.dataset.rooms)data.assignments.find(a=>a.id===t.dataset.rooms).room_ids=t.value.split(',').map(x=>x.trim()).filter(Boolean);
 save();render();
});
$('solve').onclick=guard(async()=>{
 if(busy)return;readConfig();
 const previous=$('warm').checked?(result?.lessons||[]):[];let scope;
 if($('local').checked){if(!previous.length)throw Error('Xếp lại cục bộ cần bật lịch hiện tại và có nghiệm trước.');const names=$('scope').value.split(',').map(x=>x.trim()).filter(Boolean);if(!names.length)throw Error('Nhập mã lớp/GV cần xếp lại.');
  for(const n of names)if(!/^day:[0-6]$|^session:[0-6]:(am|pm)$/.test(n)&&!data.classes.some(x=>x.id===n)&&!data.teachers.some(x=>x.id===n))throw Error('Mã phạm vi chưa tồn tại: '+n);
  scope={classes:names.filter(n=>data.classes.some(x=>x.id===n)),teachers:names.filter(n=>data.teachers.some(x=>x.id===n)),days:names.filter(n=>/^day:[0-6]$/.test(n)).map(n=>Number(n.split(':')[1])),sessions:names.filter(n=>/^session:[0-6]:(am|pm)$/.test(n)).map(n=>({day:Number(n.split(':')[1]),shift:n.split(':')[2]}))};}
 busy=true;lockEditing(true);const snap=snapshot();$('solve').disabled=true;msg('Đang lập mô hình CP-SAT…');
 try{const current_schedule=result?.lessons||[],analysis=await api('/api/session-analysis',{data,config,current_schedule});let session_confirmation;
  if(analysis.change.confirmation_required){if(!await confirmCalendarChange(analysis.change)){msg('Đã hủy xếp lại. Lịch hiện tại được giữ; cấu hình mới chưa được áp dụng vào nghiệm.');return;}session_confirmation=analysis.change.confirmation;}
  const job=await api('/api/solve',{data,config,previous,scope,current_schedule,session_confirmation});
  for(;;){await new Promise(r=>setTimeout(r,500));const state=await api('/api/jobs/'+job.id);msg(state.progress);
   if(state.state==='error')throw Error(state.error);
   if(state.state==='done'){if(state.result.status==='BLOCKED'&&state.result.session_change)throw Error(state.result.diagnostics.join(' · '));result=state.result;markChecked();solvedSnapshot=snap;save();render();msg(`Hoàn tất: ${result.status} · ${result.placed}/${result.required} tiết. ${result.unscheduled_special} tiết đặc biệt vẫn chưa phân công.`);break;}}
 }finally{busy=false;lockEditing(false);$('solve').disabled=false;renderCalendar();renderPostCheck();}
});
$('validate').onclick=guard(async()=>{readConfig();const r=await api('/api/validate',{data,config});backgroundContext=r.background;msg(r.errors.length?r.errors.join(' · '):`Dữ liệu kỹ thuật hợp lệ; còn ${data.issues.length} cảnh báo/ghi nhận nguồn cần xem. Chưa phải nghiệm thu lịch thực tế.`);save();render();});
$('xlsx').onchange=guard(async e=>{if(busy)throw Error('Đang giải, chưa thể thay dữ liệu.');const f=e.target.files[0];if(!f)return;const bytes=new Uint8Array(await f.arrayBuffer());let s='';for(let i=0;i<bytes.length;i+=8192)s+=String.fromCharCode(...bytes.subarray(i,i+8192));const r=await api('/api/import',{base64:btoa(s)});data=r.data;config.special_overrides=[];config.special_scenario={};result=null;solvedSnapshot='';configUI();save();render();msg('Đã đọc trực tiếp cả 5 sheet PCCM. Xem cảnh báo trước khi xếp.');e.target.value='';});
async function validatedBackup(x){
 const nextBackground=x.background??{lessons:x.result?.lessons||[],config:x.config,source_label:'Lịch lưu V3.1 nhập lại'};
 const isDraft=x.version==='3.1.3-time-conflict';
 const check=await api('/api/validate',{data:x.data,config:x.config,background:nextBackground,...(x.result?.locked_hash_before?{locked_hash:x.result.locked_hash_before}:{}),...(!isDraft&&x.result?.lessons?.length?{lessons:x.result.lessons}:{})});
 if(check.errors.length)throw Error(check.errors.join(' · '));
 return {data:x.data,config:check.config,background:nextBackground,backgroundContext:check.background,result:isDraft&&x.result?.lessons?.length?(await api('/api/draft',{data:x.data,config:check.config,background:nextBackground,lessons:x.result.lessons})).result:check.schedule?.valid?check.result:null};
}
function applyBackup(next){data=next.data;config=next.config;background=next.background;backgroundContext=next.backgroundContext;result=next.result;markChecked();solvedSnapshot=result?snapshot():'';}
$('json').onchange=guard(async e=>{if(busy)throw Error('Đang giải, chưa thể thay dữ liệu.');const f=e.target.files[0];if(!f)return;const x=JSON.parse(await f.text());
 if(x.version===3||x.version==='3.1'||x.version==='3.1.1-grade'||x.version==='3.1.2-session'||x.version==='3.1.3-time-conflict'){const next=await validatedBackup(x);applyBackup(next);msg(next.result?'Đã khôi phục lịch và kiểm tra lại ràng buộc cứng. Chứng minh tối ưu trong backup là ghi nhận lịch sử.':'Đã khôi phục dữ liệu; lịch backup không hợp lệ hoặc chưa có lịch nên cần giải lại.');}
 else{const migrated=(await api('/api/migrate-v2',{data:x})).data;if(migrated.classes.some(c=>![6,7,8,9].includes(c.grade)))throw Error('V2 chưa có khối xác minh. Bổ sung grade 6..9 vào danh mục lớp JSON trước khi nhập; không tự đoán khối từ tên.');data=migrated;config.special_overrides=[];config.special_scenario={};result=null;solvedSnapshot='';msg('Đã chuyển JSON V2 sang V3 riêng. Chưa xác minh PCCM.');}
 configUI();solvedSnapshot=result?snapshot():'';save();render();e.target.value='';});
$('backup').onclick=guard(async()=>{readConfig();if(result?.lessons?.length)await doPostCheck();download(JSON.stringify({version:'3.1.3-time-conflict',data,config,background,result,solvedSnapshot,draft:true,production_ready:false},null,2),'SMART_TKB_V3_1_3_KHOI'+config.target_grade+'_DRAFT.json');msg('Đã lưu bản nháp; trạng thái hậu kiểm: '+checkStatus()+'.');});
async function exportSchedule(format){readConfig();if(!result?.lessons.length||stale())throw Error('Cần lịch hiện hành đã giải trước khi xuất.');const post=await doPostCheck();if(post.status==='FAIL')throw Error('TKB có lỗi HARD; sửa trước khi xuất lịch. Có thể xuất báo cáo lỗi hoặc lưu bản nháp JSON.');const r=await api('/api/export-schedule',{data,config,lessons:result.lessons,format});const bytes=Uint8Array.from(atob(r.base64),c=>c.charCodeAt(0));download(bytes,'SMART_TKB_V3_1_3_KHOI'+config.target_grade+'.'+format,format==='csv'?'text/csv;charset=utf-8':'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');}
$('csv').onclick=guard(()=>exportSchedule('csv'));$('export-xlsx').onclick=guard(()=>exportSchedule('xlsx'));
$('schedule-file').onchange=guard(async e=>{if(busy)throw Error('Chờ giải xong trước khi nhập lịch.');readConfig();const f=e.target.files[0];if(!f)return;const bytes=new Uint8Array(await f.arrayBuffer());let raw='';for(let i=0;i<bytes.length;i+=8192)raw+=String.fromCharCode(...bytes.subarray(i,i+8192));result=(await api('/api/import-draft',{data,config,base64:btoa(raw),format:f.name.toLowerCase().endsWith('.csv')?'csv':'xlsx'})).result;markChecked();solvedSnapshot=snapshot();save();render();msg('Đã nhập lịch và kiểm tra độc lập.');e.target.value='';});
$('print').onclick=()=>window.print();
guard(async()=>{const boot=await api('/api/bootstrap');token=boot.token;data=boot.data;config=boot.config;background=boot.background;backgroundContext=boot.background_context;baseline={};
 try{const saved=JSON.parse(localStorage.getItem(KEY)||'null');if(['3.1.2-session','3.1.3-time-conflict'].includes(saved?.version)){const wasStale=saved.result&&saved.solvedSnapshot!==JSON.stringify(stable({data:saved.data,config:saved.config,background:saved.background}));applyBackup(await validatedBackup(wasStale?{...saved,result:null}:saved));sessionProfiles=saved.sessionProfiles||{};if(wasStale){result=saved.result;solvedSnapshot=saved.solvedSnapshot;msg('Đã mở cấu hình đang sửa và lịch cũ; cần xác nhận nếu lịch nằm ngoài số tiết mới.');}if(!result)msg('Bản lưu dữ liệu đã mở; lịch cũ không qua kiểm tra độc lập hoặc chưa có lịch nên cần giải lại.');}}
 catch(e){msg('Không dùng được bản lưu cũ; đang dùng PCCM SOURCE. '+e.message);}
 configUI();render();
})();
let specialRequest=0;
async function refreshSpecial(){
 const request=++specialRequest;
 try{const next=await api('/api/special',{data,config});if(request!==specialRequest)return;specialContext=next;const selected=new Set(config.special_scenario?.activity_ids||[]);
 $('special-summary').textContent=`Tổng ${specialContext.total} · quy tắc xác minh ${specialContext.rule_verified??specialContext.verified} · phê duyệt ${specialContext.approved??0} · pending chính thức ${specialContext.pending} · đủ điều kiện mô phỏng ${specialContext.eligible_scenario}. Hoạt động được đưa vào lịch sẽ chiếm công suất lớp; nhóm tập thể chỉ dùng một buổi GV cho cùng sự kiện.`;
 $('special-table').innerHTML='<table><tr><th>Chọn mô phỏng</th><th>Mã / lớp</th><th>Nhãn nguồn / loại</th><th>Tiết</th><th>Trạng thái nguồn / kiểm kê</th><th>Lý do pending</th></tr>'+specialContext.inventory.map(a=>`<tr><td><input data-activity="${esc(a.activity_id)}" type="checkbox" ${selected.has(a.activity_id)?'checked':''} aria-label="Mô phỏng ${esc(a.activity_id)}"></td><td>${esc(a.activity_id)}<br>${esc((a.class_ids||[a.class_id]).join(', '))}</td><td>${esc(a.source_label)}<br><small>${esc(a.activity_type)}</small></td><td>${a.weekly_count}</td><td>${esc(a.validation_status)} / ${esc(a.audit_status||'MISSING')}</td><td>${esc(specialContext.pending_details.find(p=>p.activity_id===a.activity_id)?.reasons.join('; ')||a.verification_note||'')}</td></tr>`).join('')+'</table>';
 }catch(e){if(request===specialRequest)$('special-summary').textContent=e.message;}
}
$('special-check').onclick=guard(async()=>{readConfig();await refreshSpecial();save();msg('Đã kiểm tra quy tắc; hoạt động pending không được coi là lịch chính thức.');});
function renderAnalytics(){
 const ref=baseline[config.mode],m=result?.metrics,q=result?.quality_scores;
 $('before-after').innerHTML=m&&result?.initial_metrics?'<table><tr><th>Chỉ số</th><th>Nghiệm khởi đầu của lượt này</th><th>Sau tối ưu</th></tr>'+Object.keys(GOALS).map(k=>`<tr><td>${GOALS[k]}</td><td>${result.initial_metrics[k]??'—'}</td><td>${m[k]??'—'}</td></tr>`).join('')+'</table>':'Chạy tối ưu để so sánh với nghiệm khởi đầu trên cùng dữ liệu/cấu hình.';
 $('comparison').innerHTML=ref&&m?'<table><tr><th>Chỉ số</th><th>V3 tham chiếu</th><th>V3.1 hiện tại</th></tr>'+['gaps','visits','distribution','concentration'].map(k=>`<tr><td>${GOALS[k]}</td><td>${ref.metrics?.[k]??'—'}</td><td>${m[k]??'—'}</td></tr>`).join('')+'</table>':'Benchmark hiện tại chỉ xét khối được chọn; báo cáo 37 lớp là tài liệu lịch sử.';
 $('teacher-visits').innerHTML='<table><tr><th>Mã GV</th><th>Nhãn nguồn</th><th>Tiết</th><th>Buổi</th><th>Ngày / ca</th></tr>'+(result?.teacher_visits||[]).map(t=>`<tr><td>${esc(t.teacher_id)}</td><td>${esc(t.name)}</td><td>${t.periods}</td><td>${t.visits}</td><td>${esc(t.sessions.map(([d,s])=>'T'+(d+2)+' '+s).join(', '))}</td></tr>`).join('')+'</table>';
 const old=$('chart-subject').value,subjects=[...new Set((q?.daily_matrix||[]).map(r=>r.subject))];$('chart-subject').innerHTML=subjects.map(s=>`<option value="${esc(s)}">${esc(data.subjects.find(x=>x.base===s)?.name||s)} (${esc(s)})</option>`).join('');if(subjects.includes(old))$('chart-subject').value=old;renderChart();
}
function renderChart(){const rows=result?.quality_scores?.daily_matrix||[],sub=$('chart-subject').value,chartDays=Array.from({length:config.session_config.include_sunday?7:6},(_,d)=>d),totals=chartDays.map(d=>rows.filter(r=>r.subject===sub).reduce((s,r)=>s+r.days[d],0)),max=Math.max(1,...totals);
 $('distribution-chart').innerHTML=rows.length?'<table><tr><th>Ngày</th><th>Tổng tiết khối đang xếp của môn</th><th>Phân bố</th></tr>'+totals.map((v,d)=>`<tr><td>${DAYS[chartDays[d]]}</td><td>${v}</td><td><meter min="0" max="${max}" value="${v}">${v}</meter></td></tr>`).join('')+'</table>':'Chưa có lịch để tính phân bố.';
}
$('chart-subject').onchange=renderChart;

function renderBackground(){
 const b=backgroundContext;if(!b)return;
 $('locked-summary').innerHTML='<table><tr><th>Khối khóa</th><th>Lớp</th><th>Tiết đã khóa</th><th>Trạng thái</th><th>SHA-256 snapshot</th></tr>'+b.grades.map(g=>`<tr><td>${g.grade}</td><td>${g.classes}</td><td>${g.locked_periods}</td><td>${esc(g.status)}</td><td><code>${esc(g.hash)}</code></td></tr>`).join('')+'</table>';
 $('cross-teachers').innerHTML='<table><tr><th>Mã GV</th><th>Nhãn nguồn</th><th>Khối</th><th>Tiết nền / buổi</th><th>Định danh</th></tr>'+b.cross_grade_teachers.map(t=>`<tr><td>${esc(t.teacher_id)}</td><td>${esc(t.name)}</td><td>${t.grades.join(', ')}</td><td>${t.locked_periods} / ${t.locked_visits}</td><td>${t.identity_verified?'VERIFIED':'CHƯA XÁC MINH'}</td></tr>`).join('')+'</table>';
 $('background-warnings').textContent=(b.complete?'Lịch nền đầy đủ trong dữ liệu được kiểm tra. ':'LỊCH NỀN CHƯA ĐẦY ĐỦ · CROSS-GRADE BLOCKED. ')+b.warnings.join(' ');
}
$('optimize').onclick=guard(async()=>{if(!result?.lessons?.length)throw Error('Cần lịch khối hiện tại trước khi tối ưu lại.');$('warm').checked=true;await $('solve').onclick();});
$('check-grade').onclick=()=>$('validate').onclick();
$('background-file').onchange=guard(async e=>{const f=e.target.files[0];if(!f)return;readConfig();const x=JSON.parse(await f.text()),next=x.background??{lessons:x.lessons??x.result?.lessons??[],config:x.config,source_label:x.source_label||f.name};const check=await api('/api/validate',{data,config,background:next});background=next;backgroundContext=check.background;result=null;solvedSnapshot='';save();render();msg('Đã nạp lịch nền sau kiểm tra, không sửa các dòng khóa.');e.target.value='';});
$('clear-background').onclick=guard(async()=>{readConfig();const check=await api('/api/validate',{data,config,background:null});background=null;backgroundContext=check.background;result=null;solvedSnapshot='';save();render();msg('Không còn lịch nền trong phiên. Không thể xác minh đầy đủ xung đột liên khối.');});
$('target_grade').onchange=guard(async()=>{
 const oldConfig=structuredClone(config),oldBackground=background;
 try{
  const next=Number($('target_grade').value);
  if(result?.lessons?.length){
   if(stale())throw Error('Lịch đang cũ; xếp lại hoặc khôi phục backup hiện hành trước khi đổi khối.');
   background=(await api('/api/freeze-background',{data,config,lessons:result.lessons})).background;
  }
  sessionProfiles[oldConfig.target_grade]=structuredClone(oldConfig.session_config);config.session_config=structuredClone(sessionProfiles[next]||referenceWeekConfig());readConfig();config.target_grade=next;const r=await api('/api/validate',{data,config});backgroundContext=r.background;result=null;solvedSnapshot='';configUI();save();render();
 }catch(e){config=oldConfig;background=oldBackground;configUI();throw e;}
});

const DAYS=['Thứ Hai','Thứ Ba','Thứ Tư','Thứ Năm','Thứ Sáu','Thứ Bảy','Chủ nhật'];
function referenceWeekConfig(){return {schema_version:1,max_periods:5,include_sunday:false,week:[{am:5,pm:4},{am:5,pm:0},{am:5,pm:4},{am:5,pm:0},{am:5,pm:4},{am:4,pm:0},{am:0,pm:0}],class_weeks:{}};}
function ensureCalendar(){if(config.session_config)return;config.session_config={schema_version:1,max_periods:Math.max(5,config.periods),include_sunday:config.days===7,week:Array.from({length:7},(_,d)=>({am:(config.active_days||[]).includes(d)?config.session_periods.am:0,pm:(config.active_days||[]).includes(d)?config.session_periods.pm:0})),class_weeks:{}};}
function classWeek(cid){return config.session_config.class_weeks[cid]||config.session_config.week;}
function effectiveCount(cl,d,sh){if(!cl)return 0;if(config.mode==='morning'&&sh==='pm'||config.mode==='mixed'&&sh!==(cl.shift||'am'))return 0;return classWeek(cl.id)[d][sh];}
function renderCalendar(){
 ensureCalendar();const old=$('session-scope').value,classes=activeClasses();$('session-scope').innerHTML='<option value="grade">Cả khối · lịch chung</option>'+classes.map(c=>`<option value="${esc(c.id)}">${esc(c.name)}${config.session_config.class_weeks[c.id]?' · chỉnh riêng':''}</option>`).join('');if(old==='grade'||classes.some(c=>c.id===old))$('session-scope').value=old;
 const scope=$('session-scope').value,v=config.session_config,w=scope==='grade'?v.week:classWeek(scope);$('session-max').value=v.max_periods;$('include-sunday').checked=v.include_sunday;
 $('session-table').innerHTML='<thead><tr><th>Ngày</th><th>Buổi sáng · số tiết</th><th>Buổi chiều · số tiết</th></tr></thead><tbody>'+w.slice(0,v.include_sunday?7:6).map((day,d)=>'<tr><th>'+DAYS[d]+'</th>'+['am','pm'].map(sh=>`<td class="${day[sh]===0?'rest':''}"><label><input type="number" min="0" max="${v.max_periods}" value="${day[sh]}" data-session-day="${d}" data-session-shift="${sh}" aria-label="${DAYS[d]} ${sh==='am'?'sáng':'chiều'}"><span>${day[sh]===0?'NGHỈ':day[sh]+' tiết'}</span></label></td>`).join('')+'</tr>').join('')+'</tbody>';
 for(const id of ['copy-from','copy-to']){const prev=$(id).value;$(id).innerHTML=classes.map(c=>`<option value="${esc(c.id)}">${esc(c.name)}</option>`).join('');if(classes.some(c=>c.id===prev))$(id).value=prev;}
 if(busy)document.querySelectorAll('#session-table input').forEach(x=>x.disabled=true);
}
function calendarChanged(){save();render();msg('Đã giữ cấu hình mới. Lịch đã xếp cần giải lại nếu cấu hình thay đổi.');}
$('session-scope').onchange=renderCalendar;
$('session-table').onchange=guard(e=>{if(busy)throw Error('Chờ giải xong.');const t=e.target,d=Number(t.dataset.sessionDay),sh=t.dataset.sessionShift,n=Number(t.value);if(!sh)return;if(!Number.isInteger(n)||n<0||n>config.session_config.max_periods){renderCalendar();throw Error('Số tiết phải nguyên0..'+config.session_config.max_periods);}
 const cid=$('session-scope').value;if(cid==='grade')config.session_config.week[d][sh]=n;else{config.session_config.class_weeks[cid]=structuredClone(classWeek(cid));config.session_config.class_weeks[cid][d][sh]=n;}calendarChanged();});
$('include-sunday').onchange=guard(()=>{if(!$('include-sunday').checked&&[config.session_config.week,...Object.values(config.session_config.class_weeks)].some(w=>w[6].am||w[6].pm)){$('include-sunday').checked=true;throw Error('Đặt hai buổi Chủ nhật về0 ở lịch chung và từng lớp trước khi ẩn.');}config.session_config.include_sunday=$('include-sunday').checked;calendarChanged();});
$('session-max').onchange=guard(()=>{const n=Number($('session-max').value);if(!Number.isInteger(n)||n<1||n>8||[config.session_config.week,...Object.values(config.session_config.class_weeks)].some(w=>w.some(d=>d.am>n||d.pm>n))){renderCalendar();throw Error('Giới hạn1..8 phải đủ cho mọi số tiết đang nhập; không tự giảm số tiết.');}config.session_config.max_periods=n;config.periods=Math.max(config.periods,n);calendarChanged();});
$('apply-grade').onclick=guard(()=>{const cid=$('session-scope').value;config.session_config.week=structuredClone(cid==='grade'?config.session_config.week:classWeek(cid));config.session_config.class_weeks={};$('session-scope').value='grade';calendarChanged();msg('Đã áp dụng lịch đang chọn cho cả khối '+config.target_grade+'. Các khối khóa giữ nguyên.');});
$('inherit-grade').onclick=guard(()=>{const cid=$('session-scope').value;if(cid==='grade')throw Error('Chọn một lớp để trở về lịch chung.');delete config.session_config.class_weeks[cid];calendarChanged();});
$('copy-calendar').onclick=guard(()=>{const from=$('copy-from').value,to=$('copy-to').value;config.session_config.class_weeks[to]=structuredClone(classWeek(from));calendarChanged();msg('Đã sao chép lịch '+from+' sang '+to+'.');});
$('reference-calendar').onclick=guard(()=>{config.session_config=referenceWeekConfig();calendarChanged();});
function profileKey(){return 'calendar:'+config.target_grade+':'+activeClasses().map(c=>c.id).sort().join(',');}
$('save-calendar').onclick=guard(async()=>{readConfig();await api('/api/session-analysis',{data,config});localStorage.setItem(KEY+':'+profileKey(),JSON.stringify(config.session_config));save();msg('Đã lưu cấu hình buổi cho khối và danh mục lớp hiện tại.');});
async function acceptCalendar(next){if(busy)throw Error('Chờ tác vụ hiện tại kết thúc.');busy=true;lockEditing(true);try{const candidate={...config,session_config:next},r=await api('/api/session-analysis',{data,config:candidate});config=r.config;configUI();calendarChanged();}finally{busy=false;lockEditing(false);renderCalendar();}}
$('restore-calendar').onclick=guard(async()=>{const raw=localStorage.getItem(KEY+':'+profileKey());if(!raw)throw Error('Chưa có cấu hình buổi đã lưu cho khối này.');await acceptCalendar(JSON.parse(raw));});
$('download-calendar').onclick=guard(()=>{download(JSON.stringify({version:'3.1.2-session-config',target_grade:config.target_grade,class_ids:activeClasses().map(c=>c.id),session_config:config.session_config},null,2),'CAU_HINH_BUOI_KHOI'+config.target_grade+'.json');});
$('calendar-file').onchange=guard(async e=>{const f=e.target.files[0];if(!f)return;const x=JSON.parse(await f.text());if(x.target_grade!==config.target_grade||JSON.stringify([...x.class_ids].sort())!==JSON.stringify(activeClasses().map(c=>c.id).sort()))throw Error('Cấu hình khác khối hoặc danh mục lớp; không tự ánh xạ.');await acceptCalendar(x.session_config);e.target.value='';});
async function refreshCalendarAnalysis(){const id=++calendarRequest;try{const r=await api('/api/session-analysis',{data,config,current_schedule:result?.lessons||[]});if(id!==calendarRequest)return;const a=r.analysis;
 $('day-count').textContent=`Khối ${config.target_grade}: ${a.weekly_sessions} buổi học · ${a.weekly_slots} ô tiết · ${a.rest_sessions} buổi nghỉ (cộng từng lớp).`;
 $('session-summary').textContent=`PCCM/quy tắc đủ điều kiện: ${a.required} tiết; công suất ${a.capacity}; còn ${a.capacity_after_fixed} ô sau ${a.fixed_periods} tiết cố định. ${r.change.confirmation_required?r.change.affected_periods+' tiết lịch cũ ngoài cấu hình mới; cần xác nhận trước khi giải lại. ':''}${a.warnings.join(' ')}`;
 $('session-capacity').innerHTML='<table><tr><th>Lớp</th><th>Buổi học</th><th>Ô tiết</th><th>Công suất</th><th>PCCM</th><th>Buổi nghỉ</th><th>Còn sau cố định</th></tr>'+a.classes.map(c=>`<tr><td>${esc(c.class_name)}</td><td>${c.weekly_sessions}</td><td>${c.weekly_slots}</td><td>${c.capacity}</td><td class="${c.over_capacity?'warning':''}">${c.required}</td><td>${c.rest_sessions}</td><td>${c.capacity_after_fixed}</td></tr>`).join('')+'</table>';
 $('resource-capacity').innerHTML='<p>Đây là cận công suất cần thiết; chưa chứng minh có nghiệm.</p><table><tr><th>GV</th><th>Ô dùng được</th><th>Công suất sau giới hạn/lịch khóa</th></tr>'+a.teacher_availability.map(t=>`<tr><td>${esc(t.teacher_id)}</td><td>${t.available_slots}</td><td>${t.residual_session_capacity}</td></tr>`).join('')+'</table><p>'+a.room_availability.map(r=>esc(r.room_id)+': '+r.available_slots+' ô').join(' · ')+'</p>';
 }catch(e){if(id===calendarRequest)$('session-summary').textContent=e.message;}}
function confirmCalendarChange(change){return new Promise(resolve=>{const dialog=$('session-confirm');$('session-confirm-message').textContent=change.affected_periods+' tiết đã xếp rơi vào buổi nghỉ hoặc vượt số tiết mới. Xác nhận xếp lại khối '+config.target_grade+'?';const finish=value=>{dialog.close();resolve(value);};$('session-cancel').onclick=()=>finish(false);$('session-continue').onclick=()=>finish(true);dialog.oncancel=e=>{e.preventDefault();finish(false);};dialog.showModal();});}
$('config').addEventListener('change',guard(()=>{if(busy)return;readConfig();save();render();}));

const TIME_GOALS={gaps:'Tiết trống',visits:'Buổi',days:'Ngày',waiting:'Chờ sáng–chiều',fragmentation:'Cụm tiết',fairness:'Tiết trống lớn nhất/GV'};
function checkSnapshot(){return JSON.stringify(stable({data,config,background,lessons:result?.lessons}));}
function markChecked(){if(result?.post_check)result._client_check_snapshot=checkSnapshot();}
function checkStatus(){return result?.post_check?(result._client_check_snapshot===checkSnapshot()?result.post_check.status:'STALE'):'NOT_CHECKED';}
async function doPostCheck(){if(busy)throw Error('Chờ bộ giải kết thúc.');if(!result?.lessons?.length)throw Error('Chưa có lịch để kiểm tra.');const report=await api('/api/post-check',{data,config,lessons:result.lessons});result.post_check=report;result.confirmation=null;markChecked();save();renderPostCheck();return report;}
function renderPostCheck(){const r=result?.post_check,status=checkStatus();$('confirm-schedule').disabled=busy||status!=='PASS';$('post-summary').textContent=r?status+' · '+Object.entries(r.counts).map(([k,v])=>k+': '+v).join(' · ')+' · Toàn trường: '+(status==='STALE'?'cần kiểm tra lại':r.school_conflicts??'CHƯA XÁC MINH')+' · Hash: '+r.context_hash:'Chưa có lịch để kiểm tra.';
 $('post-errors').innerHTML=r?.errors?.length?'<table><tr><th>Loại / mức độ</th><th>Vị trí</th><th>Lỗi / đề xuất</th></tr>'+r.errors.map((e,i)=>`<tr><td>${esc(e.type)}<br>${esc(e.severity)}</td><td><button data-error="${i}">Định vị</button><br>${(e.events||[]).map(v=>esc(v.teacher_ids?.join(', ')+' / '+v.class_ids?.join(', ')+' / '+v.subject+' / '+v.day_name+' '+v.shift+' tiết '+(v.period+1)+' / '+(v.room||'—')+' / khối '+v.grades?.join(','))).join('<br>')}</td><td>${esc(e.message)}<br>${esc(e.suggestion)}</td></tr>`).join('')+'</table>':status==='STALE'?'Lịch đã đổi, kết quả kiểm tra cũ hết hiệu lực.':'Chưa phát hiện lỗi trong phạm vi đã kiểm tra.';
 $('post-warnings').innerHTML=(r?.warnings||[]).map(w=>'<div class="warning">'+esc(w.type)+': '+esc(w.message)+'</div>').join('');}
function renderTeacherTime(){const t=result?.teacher_time;if(!t){$('time-summary').textContent='Chưa có chỉ số.';$('time-teachers').innerHTML='';return;}
 $('time-summary').textContent=Object.entries(TIME_GOALS).map(([k,v])=>v+': '+t.totals[k]+' (nền khóa '+t.locked_baseline[k]+')').join(' · ')+' · Chờ '+(config.teacher_time?.waiting_enabled?'được bật tối ưu':'chỉ thống kê')+': '+t.waiting_kind+' / '+t.waiting_unit+' '+t.waiting_note;
 const before=new Map((result.initial_teacher_time?.teachers||[]).map(x=>[x.teacher_id,x]));$('time-teachers').innerHTML='<table><tr><th>Mã GV / nhãn</th><th>Tiết</th><th>Trống trước→sau</th><th>Buổi trước→sau</th><th>Ngày trước→sau</th><th>Chờ trước→sau</th><th>Cụm</th></tr>'+t.teachers.filter(x=>x.periods).map(x=>`<tr><td>${esc(x.teacher_id)} / ${esc(x.name)}</td><td>${x.periods}</td>${['gaps','visits','days','waiting'].map(k=>'<td>'+(before.get(x.teacher_id)?.[k]??'—')+' → '+x[k]+'</td>').join('')}<td>${x.fragmentation}</td></tr>`).join('')+'</table>';}
$('post-check').onclick=guard(async()=>{readConfig();const r=await doPostCheck();msg('Hậu kiểm: '+r.status+'; '+r.counts.hard_violations+' lỗi HARD.');});
$('confirm-schedule').onclick=guard(async()=>{readConfig();if(!result?.post_check)throw Error('Kiểm tra lịch trước.');const r=await api('/api/confirm-schedule',{data,config,lessons:result.lessons,certificate:result.post_check});result.post_check=r.report;markChecked();if(r.accepted)result.confirmation=r;save();renderPostCheck();msg(r.status+' · '+r.message);});
$('conflicts-xlsx').onclick=guard(async()=>{readConfig();if(!result?.lessons?.length)throw Error('Chưa có lịch.');const r=await api('/api/export-conflicts',{data,config,lessons:result.lessons});result.post_check=r.report;markChecked();save();renderPostCheck();download(Uint8Array.from(atob(r.base64),c=>c.charCodeAt(0)),'KIEM_TRA_TKB_KHOI'+config.target_grade+'.xlsx','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');});
$('conflicts-print').onclick=guard(async()=>{readConfig();await doPostCheck();showTab('schedule');document.body.classList.add('print-conflicts');window.print();document.body.classList.remove('print-conflicts');});
$('post-errors').onclick=e=>{const b=e.target.closest('[data-error]');if(!b)return;const err=result.post_check.errors[Number(b.dataset.error)],v=err.events?.find(x=>!x.locked)||err.events?.[0];if(!v)return;showTab('schedule');$('viewtype').value=v.locked?'teachers':'classes';renderGrid();$('viewer').value=v.locked?v.teacher_ids[0]:v.class_ids[0];renderGrid();const cell=document.querySelector(`[data-slot-day="${v.day}"][data-slot-shift="${v.shift}"][data-slot-period="${v.period}"]`);if(cell){cell.classList.add('conflict-focus');cell.scrollIntoView({block:'center',behavior:'smooth'});}};
let editIndex=null;
function openEdit(index){if(busy)return;const l=result?.lessons?.[index];if(!l)return;editIndex=index;$('manual-info').textContent=l.assignment+' · '+l.teacher+' · '+l.class_id+' · '+l.subject+' · '+l.length+' tiết';$('manual-day').value=l.day;$('manual-shift').value=l.shift;$('manual-period').value=l.period+1;$('manual-room').value=l.room||'';$('manual-dialog').showModal();}
$('grid').onclick=e=>{const td=e.target.closest('[data-edit-index]');if(td)openEdit(Number(td.dataset.editIndex));};$('grid').onkeydown=e=>{if(e.key==='Enter'){const td=e.target.closest('[data-edit-index]');if(td)openEdit(Number(td.dataset.editIndex));}};
$('manual-cancel').onclick=()=>$('manual-dialog').close();
$('manual-apply').onclick=guard(async()=>{if(busy)throw Error('Chờ giải xong.');readConfig();const r=await api('/api/manual-edit',{data,config,lessons:result.lessons,index:editIndex,patch:{day:Number($('manual-day').value),shift:$('manual-shift').value,period:Number($('manual-period').value)-1,room:$('manual-room').value||null}});result=r.result;markChecked();solvedSnapshot=snapshot();$('manual-dialog').close();save();render();msg('Đã chuyển tiết; hậu kiểm '+checkStatus()+'. Chứng minh tối ưu trước đây không được kế thừa.');});

for(const panel of ['config','dataset','special','grade-controls'])$(panel).addEventListener('input',e=>{if(!busy&&result?.post_check&&e.target.type!=='file'){result._client_check_snapshot='';result.confirmation=null;renderPostCheck();}});
