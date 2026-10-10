'use strict';
const $=id=>document.getElementById(id),KEY='smart_tkb_thcs_v3_1_1_grade_candidate';
let data,config,token,result=null,solvedSnapshot='',tableView='teachers',busy=false,baseline={},specialContext=null,background=null,backgroundContext=null;
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const msg=t=>$('message').textContent=t;
async function api(path,payload){if(payload&&!Object.hasOwn(payload,'background'))payload={background,...payload};const r=await fetch(path,payload?{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':token},body:JSON.stringify(payload)}:{});const b=await r.json();if(!r.ok)throw Error(b.error||'Yêu cầu không thành công');return b;}
function download(content,name,type='application/json'){const url=URL.createObjectURL(new Blob([content],{type})),a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
function save(){try{localStorage.setItem(KEY,JSON.stringify({version:'3.1.1-grade',data,config,background,result,solvedSnapshot}));}catch(e){msg('Dữ liệu đang ở phiên hiện tại; lưu trình duyệt thất bại. Hãy tải bản sao JSON.');}}
function stable(x){return Array.isArray(x)?x.map(stable):x&&typeof x==='object'?Object.fromEntries(Object.keys(x).sort().map(k=>[k,stable(x[k])])):x;}
function snapshot(){return JSON.stringify(stable({data,config,background}));}
function lockEditing(value){document.querySelectorAll('#grade-controls input,#grade-controls select,#grade-controls button,#optimize,#check-grade,#config input,#config select,#config textarea,#special input,#special select,#dataset input,#dataset select,input[type=file],#validate,#backup,#warm,#local,#scope').forEach(el=>{if(value){el.dataset.wasDisabled=String(el.disabled);el.disabled=true;}else if(el.dataset.wasDisabled!==undefined){el.disabled=el.dataset.wasDisabled==='true';delete el.dataset.wasDisabled;}});}
function stale(){return result&&solvedSnapshot!==snapshot();}
function readConfig(){
 const advanced=JSON.parse($('advanced').value);for(const k of Object.keys(advanced))if(!ADVANCED.includes(k))throw Error('Trường JSON bổ sung chưa được hỗ trợ: '+k);
 config={...config,...advanced,mode:$('mode').value,priorities:$('priorities').value.split(',')};
 for(const id of ['max_class_session','max_teacher_session','time_limit','seed','workers'])config[id]=Number($(id).value);
 config.target_grade=Number($('target_grade').value);config.days=6;config.active_days=[...document.querySelectorAll('[data-day]:checked')].map(x=>Number(x.dataset.day));config.session_periods={am:Number($('am_periods').value),pm:Number($('pm_periods').value)};config.periods=Math.max(config.session_periods.am,config.session_periods.pm);config.allow_incomplete_background=$('simulate-background').checked;config.background_assumption=$('background-assumption').value;
 config.search_mode=$('search_mode').value;config.special_mode=$('special_mode').value;
 config.objective_settings=Object.fromEntries(config.priorities.map(k=>[k,{enabled:document.querySelector('[data-objective="'+k+'"]').checked,weight:Number(document.querySelector('[data-weight="'+k+'"]').value)}]));
 if(config.special_mode==='SCENARIO')config.special_scenario={...config.special_scenario,enabled:true,activity_ids:[...document.querySelectorAll('[data-activity]:checked')].map(x=>x.dataset.activity),teacher_required:$('scenario-teacher').value==='true',teacher_id:$('scenario-teacher').value==='true'?($('scenario-gv').value||null):null,scheduling_policy:$('scenario-policy').value,shared_teacher_group:$('scenario-group').value||null,assumption_label:$('assumption').value};
 config.technical_only=true;
 return config;
}
const ADVANCED=['rooms','unavailable','fixed','preferences','phase_fractions','advance_on_incumbent','subject_rules','subject_hard_limits','heavy_subjects','heavy_run_limit','heavy_weight','special_overrides'];
const DEFAULT_ADVANCED={phase_fractions:{gaps:.25,visits:.5,distribution:.16,concentration:.06,preferences:.02,changes:.01},advance_on_incumbent:true,heavy_run_limit:2,heavy_weight:0};
const GOALS={gaps:'Tiết trống GV',visits:'Buổi GV',distribution:'Phân bố',concentration:'Dồn môn / liên tiếp',preferences:'Nguyện vọng',changes:'Thay đổi lịch cũ'};
function configUI(){$('target_grade').value=config.target_grade;$('am_periods').value=config.session_periods.am;$('pm_periods').value=config.session_periods.pm;$('simulate-background').checked=config.allow_incomplete_background;$('background-assumption').value=config.background_assumption;document.querySelectorAll('[data-day]').forEach(x=>x.checked=config.active_days.includes(Number(x.dataset.day))); for(const id of ['mode','days','periods','max_class_session','max_teacher_session','time_limit','seed','workers','search_mode','special_mode'])$(id).value=config[id];
 const priority=config.priorities.join(',');if(![...$('priorities').options].some(o=>o.value===priority))$('priorities').add(new Option(priority,priority));$('priorities').value=priority;
 $('objective-table').innerHTML='<table><tr><th>Mục tiêu</th><th>Bật</th><th>Trọng số</th></tr>'+Object.entries(GOALS).map(([k,v])=>`<tr><td>${v}</td><td><input data-objective="${k}" type="checkbox" ${config.objective_settings?.[k]?.enabled===false?'':'checked'} aria-label="Bật ${v}"></td><td><input data-weight="${k}" type="number" min="1" max="100" value="${config.objective_settings?.[k]?.weight||1}" aria-label="Trọng số ${v}"></td></tr>`).join('')+'</table>';
 $('assumption').value=config.special_scenario?.assumption_label||'';$('scenario-teacher').value=String(config.special_scenario?.teacher_required===true);$('scenario-gv').value=config.special_scenario?.teacher_id||'';
 $('scenario-policy').value=config.special_scenario?.scheduling_policy||'independent';$('scenario-group').value=config.special_scenario?.shared_teacher_group||'';
 $('advanced').value=JSON.stringify(Object.fromEntries(ADVANCED.map(k=>[k,config[k]??DEFAULT_ADVANCED[k]??[]])),null,2);
}
function activeClasses(){return data.classes.filter(c=>c.grade===config.target_grade);}
function activeAssignments(){const ids=new Set(activeClasses().map(c=>c.id));return data.assignments.filter(a=>ids.has(a.class_id));}
function activeTeachers(){const ids=new Set(activeAssignments().map(a=>a.teacher));return data.teachers.filter(t=>ids.has(t.id));}
function activePending(){const ids=new Set(activeClasses().map(c=>c.id));return data.pending_special.filter(a=>ids.has(a.class_id));}
function render(){
 $('nc').textContent=activeClasses().length;$('nt').textContent=activeTeachers().length;
 $('nr').textContent=activeAssignments().reduce((s,a)=>s+a.count,0);$('np').textContent=result?.placed||0;
 const pending=activePending().reduce((s,x)=>s+x.count,0),unverified=activeTeachers().filter(t=>t.status!=='VERIFIED'||!t.full_name).length;
 $('special-title').textContent=pending+' tiết đặc biệt · kiểm kê theo nguồn';
 $('trust').textContent=`KIỂM THỬ KỸ THUẬT CÓ ĐIỀU KIỆN · ${unverified} định danh GV chưa xác minh. ${pending} tiết hoạt động đặc biệt chưa có PCCM giáo viên, không được tự xếp. Tổng đối chiếu: ${Number($('nr').textContent)+pending} tiết. ${result?.simulation?'MÔ PHỎNG KỸ THUẬT · không dùng chính thức. ':''}${stale()?'Lịch đang hiển thị đã cũ so với dữ liệu/cấu hình; cần giải lại.':''}`;
 $('solve').textContent='✦ Xếp TKB khối '+config.target_grade;$('optimize').textContent='Tối ưu lại khối '+config.target_grade;document.querySelector('h1').textContent='XẾP TKB KHỐI '+config.target_grade;$('day-count').textContent=config.active_days.length+' ngày học / tuần; không bắt buộc lấp đầy các ô.';renderBackground();renderGrid();renderDataset();renderResult();renderAnalytics();refreshSpecial();
}
function renderGrid(){
 const type=$('viewtype').value,old=$('viewer').value;
 $('viewer').innerHTML=(type==='classes'?activeClasses():activeTeachers()).map(x=>`<option value="${esc(x.id)}">${esc(x.name)} (${esc(x.id)})</option>`).join('');
 if((type==='classes'?activeClasses():activeTeachers()).some(x=>x.id===old))$('viewer').value=old;
 const id=$('viewer').value,lessons=[...(result?.lessons||[]),...(type==='teachers'?(result?.locked_lessons||background?.lessons?.filter(l=>!activeClasses().some(c=>c.id===l.class_id))||[]):[])];const days=type==='teachers'?Array.from({length:config.days},(_,d)=>d):config.active_days;
 let h='<thead><tr><th>Buổi / Tiết</th>'+days.map(d=>`<th>Thứ ${d+2}</th>`).join('')+'</tr></thead><tbody>';
 for(const sh of type==='teachers'?['am','pm']:config.mode==='morning'?['am']:['am','pm']){
  h+=`<tr><th class="shift" colspan="${days.length+1}">${sh==='am'?'☀ BUỔI SÁNG':'◐ BUỔI CHIỀU'}</th></tr>`;
  for(let p=0;p<(type==='teachers'?Math.max(config.session_periods[sh],background?.config?.session_periods?.[sh]||background?.config?.periods||0):config.session_periods[sh]);p++){
   h+=`<tr><th>Tiết ${p+1}</th>`;
   for(const d of days){
    const l=lessons.find(l=>l.day===d&&l.shift===sh&&p>=l.period&&p<l.period+l.length&&(type==='classes'?(l.class_ids||[l.class_id]).includes(id):l.teacher===id));
    const a=l&&data.assignments.find(a=>a.id===l.assignment),s=a&&data.subjects.find(s=>s.id===a.subject_id);
    const secondary=l&&(type==='classes'?data.teachers.find(t=>t.id===l.teacher)?.name:data.classes.find(c=>c.id===l.class_id)?.name);
    h+='<td>'+(l?`<div class="lesson"><b>${esc(a?.subject||l.subject)}${s?.sub_name?' · '+esc(s.sub_name):''}</b><small>${esc(secondary)}</small>${l.room?'<small>'+esc(l.room)+'</small>':''}${!activeClasses().some(c=>c.id===l.class_id)?'<small>🔒 LỊCH KHỐI KHÁC</small>':''}${l.activity_status==='SCENARIO'?'<small>MÔ PHỎNG</small>':''}${l.length===2?'<small>↔ Tiết đôi</small>':''}</div>`:'—')+'</td>';
   }h+='</tr>';
  }
 }$('grid').innerHTML=h+'</tbody>';$('empty').hidden=lessons.length>0;
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
 const m=result.metrics||{},labels={gaps:'Tiết trống GV',visits:'Buổi lên trường GV',distribution:'Độ lệch phân bố',concentration:'Dồn môn trong ngày',preferences:'Phạt nguyện vọng',changes:'Bloc cũ thay đổi'};
 let h=`<p>GRADE SCHEDULING: ${esc(result.grade_scheduling)} · CROSS-GRADE: ${esc(result.cross_grade_conflict)} · LOCKED GRADES: ${esc(result.locked_grades)}</p><p>Xung đột đã biết với lịch khóa: ${result.known_cross_grade_conflicts??'Chưa kiểm tra'} · Xung đột toàn trường: ${result.school_conflicts??'CHƯA XÁC MINH'}</p><p>Buổi GV lịch nền: ${m.baseline_visits??'—'} · Buổi tăng thêm: ${m.added_visits??'—'} · Phạm vi chứng minh: ${esc(result.optimality_scope)}</p><div class="status ${esc(result.status)}">${esc(result.status)} ${stale()?'· LỊCH CŨ / CẦN GIẢI LẠI':''}</div><p>${result.placed} / ${result.required} tiết PCCM / hoạt động đủ quy tắc · ${result.lessons?.length?result.conflicts+' xung đột':'Không có lịch; chưa có số xung đột'} · ${result.elapsed_seconds==null?'Nhập lịch; không chạy bộ giải':result.elapsed_seconds+' giây'} · ${result.unscheduled_special} tiết đặc biệt chưa có PCCM.</p>`;
 h+=result.simulation?`<div class="warning">MÔ PHỎNG: ${result.scenario_placed} tiết giả định, chưa xác minh. ${esc((result.scenario_assumptions||[]).join('; '))}</div>`:'';
 h+='<div class="quality-grid">'+Object.entries(labels).map(([k,v])=>`<div>${v}<b>${m[k]??'—'}</b></div>`).join('')+'</div>';
 h+=`<p>Chứng minh tối ưu toàn cục theo cấu hình: ${result.global_optimal_proven?'CÓ':'CHƯA'}. ${result.optimality_scope==='local_frozen'?'Kết quả chỉ xét phạm vi cục bộ với các tiết ngoài phạm vi đã khóa. ':''}Mức ưu tiên đã chứng minh: ${esc((result.proven_priorities||[]).join(', ')||'Chưa có')}.</p>`;
 h+=(result.diagnostics||[]).map(x=>`<div class="warning">${esc(x)}</div>`).join('');
 h+='<table><tr><th>Giai đoạn</th><th>Trạng thái</th><th>Mục tiêu</th><th>Cận</th><th>Giây</th></tr>'+(result.phases||[]).map(p=>`<tr><td>${esc(p.name)}</td><td>${esc(p.status==='VERIFIED_INCUMBENT'?'Nghiệm trước đã hậu kiểm':p.status==='PROVEN_LOWER_BOUND'?'Nghiệm đạt cận dưới':p.status)}</td><td>${p.objective??'—'}</td><td>${p.best_bound??'—'}</td><td>${p.seconds}</td></tr>`).join('')+'</table>';
 h+=`<p>Khóa nghiệm chưa chứng minh: ${esc(JSON.stringify(result.incumbent_locks||{}))}. Các mức tối ưu chỉ có điều kiện: ${esc((result.conditional_optimal_priorities||[]).join(', ')||'—')}.</p>`;
 if(result.quality_scores)h+=`<p>Phạt phân bố /100 (thấp tốt hơn): ${result.initial_quality_scores?.distribution_penalty_100??'—'} → ${result.quality_scores.distribution_penalty_100}. Phạt dồn môn /100: ${result.initial_quality_scores?.concentration_penalty_100??'—'} → ${result.quality_scores.concentration_penalty_100}.</p>`;
 if(result.performance)h+=`<p>Tạo mô hình: ${result.performance.timings?.model_build_seconds??'—'} giây · ${result.performance.model?.variables??'—'} biến / ${result.performance.model?.constraints??'—'} ràng buộc · nghiệm đầu: ${result.performance.timings?.first_solution_seconds??'—'} giây.</p>`;
 if(result.verification)h+=`<p>Kiểm tra độc lập: ${result.verification.valid?'ĐẠT':'KHÔNG ĐẠT'}; đúng số tiết, giáo viên/môn, ca học, phòng, lịch nghỉ, tiết cố định, tiết đôi và phạm vi xếp lại.</p>`;
 $('result').innerHTML=h;
}
function showTab(id){document.querySelectorAll('main section').forEach(x=>x.classList.toggle('hidden',x.id!==id&&!(x.id==='grade-controls'&&['schedule','config'].includes(id))));document.querySelectorAll('nav button').forEach(x=>x.classList.toggle('active',x.dataset.tab===id));}
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
  for(const n of names)if(!data.classes.some(x=>x.id===n)&&!data.teachers.some(x=>x.id===n))throw Error('Mã phạm vi chưa tồn tại: '+n);
  scope={classes:names.filter(n=>data.classes.some(x=>x.id===n)),teachers:names.filter(n=>data.teachers.some(x=>x.id===n))};}
 busy=true;lockEditing(true);const snap=snapshot();$('solve').disabled=true;msg('Đang lập mô hình CP-SAT…');
 try{const job=await api('/api/solve',{data,config,previous,scope});
  for(;;){await new Promise(r=>setTimeout(r,500));const state=await api('/api/jobs/'+job.id);msg(state.progress);
   if(state.state==='error')throw Error(state.error);
   if(state.state==='done'){result=state.result;solvedSnapshot=snap;save();render();msg(`Hoàn tất: ${result.status} · ${result.placed}/${result.required} tiết. ${result.unscheduled_special} tiết đặc biệt vẫn chưa phân công.`);break;}}
 }finally{busy=false;lockEditing(false);$('solve').disabled=false;}
});
$('validate').onclick=guard(async()=>{readConfig();const r=await api('/api/validate',{data,config});backgroundContext=r.background;msg(r.errors.length?r.errors.join(' · '):`Dữ liệu kỹ thuật hợp lệ; còn ${data.issues.length} cảnh báo/ghi nhận nguồn cần xem. Chưa phải nghiệm thu lịch thực tế.`);save();render();});
$('xlsx').onchange=guard(async e=>{if(busy)throw Error('Đang giải, chưa thể thay dữ liệu.');const f=e.target.files[0];if(!f)return;const bytes=new Uint8Array(await f.arrayBuffer());let s='';for(let i=0;i<bytes.length;i+=8192)s+=String.fromCharCode(...bytes.subarray(i,i+8192));const r=await api('/api/import',{base64:btoa(s)});data=r.data;config.special_overrides=[];config.special_scenario={};result=null;solvedSnapshot='';configUI();save();render();msg('Đã đọc trực tiếp cả 5 sheet PCCM. Xem cảnh báo trước khi xếp.');e.target.value='';});
async function validatedBackup(x){
 const nextBackground=x.background??{lessons:x.result?.lessons||[],config:x.config,source_label:'Lịch lưu V3.1 nhập lại'};
 const check=await api('/api/validate',{data:x.data,config:x.config,background:nextBackground,...(x.result?.locked_hash_before?{locked_hash:x.result.locked_hash_before}:{}),...(x.result?.lessons?.length?{lessons:x.result.lessons}:{})});
 if(check.errors.length)throw Error(check.errors.join(' · '));
 return {data:x.data,config:check.config,background:nextBackground,backgroundContext:check.background,result:check.schedule?.valid?check.result:null};
}
function applyBackup(next){data=next.data;config=next.config;background=next.background;backgroundContext=next.backgroundContext;result=next.result;solvedSnapshot=result?snapshot():'';}
$('json').onchange=guard(async e=>{if(busy)throw Error('Đang giải, chưa thể thay dữ liệu.');const f=e.target.files[0];if(!f)return;const x=JSON.parse(await f.text());
 if(x.version===3||x.version==='3.1'||x.version==='3.1.1-grade'){const next=await validatedBackup(x);applyBackup(next);msg(next.result?'Đã khôi phục lịch và kiểm tra lại ràng buộc cứng. Chứng minh tối ưu trong backup là ghi nhận lịch sử.':'Đã khôi phục dữ liệu; lịch backup không hợp lệ hoặc chưa có lịch nên cần giải lại.');}
 else{const migrated=(await api('/api/migrate-v2',{data:x})).data;if(migrated.classes.some(c=>![6,7,8,9].includes(c.grade)))throw Error('V2 chưa có khối xác minh. Bổ sung grade 6..9 vào danh mục lớp JSON trước khi nhập; không tự đoán khối từ tên.');data=migrated;config.special_overrides=[];config.special_scenario={};result=null;solvedSnapshot='';msg('Đã chuyển JSON V2 sang V3 riêng. Chưa xác minh PCCM.');}
 configUI();save();render();e.target.value='';});
$('backup').onclick=guard(()=>{readConfig();download(JSON.stringify({version:'3.1.1-grade',data,config,background,result:stale()?null:result,solvedSnapshot},null,2),'SMART_TKB_V3_1_1_KHOI'+config.target_grade+'_backup.json');});
async function exportSchedule(format){readConfig();if(!result?.lessons.length||stale())throw Error('Cần lịch hiện hành đã giải trước khi xuất.');const r=await api('/api/export-schedule',{data,config,lessons:result.lessons,format});const bytes=Uint8Array.from(atob(r.base64),c=>c.charCodeAt(0));download(bytes,'SMART_TKB_V3_1_1_KHOI'+config.target_grade+'.'+format,format==='csv'?'text/csv;charset=utf-8':'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');}
$('csv').onclick=guard(()=>exportSchedule('csv'));$('export-xlsx').onclick=guard(()=>exportSchedule('xlsx'));
$('schedule-file').onchange=guard(async e=>{if(busy)throw Error('Chờ giải xong trước khi nhập lịch.');readConfig();const f=e.target.files[0];if(!f)return;const bytes=new Uint8Array(await f.arrayBuffer());let raw='';for(let i=0;i<bytes.length;i+=8192)raw+=String.fromCharCode(...bytes.subarray(i,i+8192));result=(await api('/api/import-schedule',{data,config,base64:btoa(raw),format:f.name.toLowerCase().endsWith('.csv')?'csv':'xlsx'})).result;solvedSnapshot=snapshot();save();render();msg('Đã nhập lịch và kiểm tra độc lập.');e.target.value='';});
$('print').onclick=()=>window.print();
guard(async()=>{const boot=await api('/api/bootstrap');token=boot.token;data=boot.data;config=boot.config;background=boot.background;backgroundContext=boot.background_context;baseline={};
 try{const saved=JSON.parse(localStorage.getItem(KEY)||'null');if(saved?.version==='3.1.1-grade'){applyBackup(await validatedBackup(saved));if(!result)msg('Bản lưu dữ liệu đã mở; lịch cũ không qua kiểm tra độc lập hoặc chưa có lịch nên cần giải lại.');}}
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
function renderChart(){const rows=result?.quality_scores?.daily_matrix||[],sub=$('chart-subject').value,totals=config.active_days.map(d=>rows.filter(r=>r.subject===sub).reduce((s,r)=>s+r.days[d],0)),max=Math.max(1,...totals);
 $('distribution-chart').innerHTML=rows.length?'<table><tr><th>Ngày</th><th>Tổng tiết khối đang xếp của môn</th><th>Phân bố</th></tr>'+totals.map((v,d)=>`<tr><td>Thứ ${config.active_days[d]+2}</td><td>${v}</td><td><meter min="0" max="${max}" value="${v}">${v}</meter></td></tr>`).join('')+'</table>':'Chưa có lịch để tính phân bố.';
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
   const bc=background?.config||config,days=Math.max(bc.days||6,config.days),periods=Math.max(bc.periods||5,config.periods);
   const combine=(a,b)=>[...new Map([...a,...b].map(x=>[x.activity_id,x])).values()];
   background={source_label:'Lịch nền phiên trước + khối '+config.target_grade+' đã hậu kiểm',lessons:[...result.locked_lessons,...result.lessons],config:{...bc,mode:'both',days,periods,active_days:Array.from({length:days},(_,d)=>d),session_periods:{am:Math.max(bc.session_periods?.am||bc.periods||5,config.session_periods.am),pm:Math.max(bc.session_periods?.pm||bc.periods||5,config.session_periods.pm)},rooms:config.rooms,special_overrides:combine(bc.special_overrides||[],config.special_overrides||[]),special_mode:config.special_mode==='SCENARIO'?'SCENARIO':bc.special_mode||'STRICT',special_scenario:config.special_mode==='SCENARIO'?config.special_scenario:bc.special_scenario||{},fixed:[...(bc.fixed||[]),...config.fixed]}};
  }
  readConfig();config.target_grade=next;const r=await api('/api/validate',{data,config});backgroundContext=r.background;result=null;solvedSnapshot='';save();render();
 }catch(e){config=oldConfig;background=oldBackground;configUI();throw e;}
});
