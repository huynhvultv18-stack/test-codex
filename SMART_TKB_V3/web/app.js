'use strict';
const $=id=>document.getElementById(id),KEY='smart_tkb_thcs_v3_candidate';
let data,config,token,result=null,solvedSnapshot='',tableView='teachers',busy=false;
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const msg=t=>$('message').textContent=t;
async function api(path,payload){const r=await fetch(path,payload?{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':token},body:JSON.stringify(payload)}:{});const b=await r.json();if(!r.ok)throw Error(b.error||'Yêu cầu không thành công');return b;}
function download(content,name,type='application/json'){const url=URL.createObjectURL(new Blob([content],{type})),a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
function save(){try{localStorage.setItem(KEY,JSON.stringify({version:3,data,config,result,solvedSnapshot}));}catch(e){msg('Dữ liệu đang ở phiên hiện tại; lưu trình duyệt thất bại. Hãy tải bản sao JSON.');}}
function snapshot(){return JSON.stringify({data,config});}
function stale(){return result&&solvedSnapshot!==snapshot();}
function readConfig(){
 const advanced=JSON.parse($('advanced').value);for(const k of Object.keys(advanced))if(!['rooms','unavailable','fixed','preferences'].includes(k))throw Error('JSON bổ sung chỉ cho phép rooms/unavailable/fixed/preferences');
 config={...config,...advanced,mode:$('mode').value,priorities:$('priorities').value.split(',')};
 for(const id of ['days','periods','max_class_session','max_teacher_session','time_limit'])config[id]=Number($(id).value);
 config.technical_only=true;
 return config;
}
function configUI(){for(const id of ['mode','days','periods','max_class_session','max_teacher_session','time_limit'])$(id).value=config[id];
 const priority=config.priorities.join(',');if(![...$('priorities').options].some(o=>o.value===priority))$('priorities').add(new Option(priority,priority));$('priorities').value=priority;
 $('advanced').value=JSON.stringify(Object.fromEntries(['rooms','unavailable','fixed','preferences'].map(k=>[k,config[k]||[]])),null,2);
}
function render(){
 $('nc').textContent=data.classes.length;$('nt').textContent=data.teachers.length;
 $('nr').textContent=data.assignments.reduce((s,a)=>s+a.count,0);$('np').textContent=result?.placed||0;
 const pending=data.pending_special.reduce((s,x)=>s+x.count,0),unverified=data.teachers.filter(t=>t.status!=='VERIFIED'||!t.full_name).length;
 $('trust').textContent=`KIỂM THỬ KỸ THUẬT CÓ ĐIỀU KIỆN · ${unverified} định danh GV chưa xác minh. ${pending} tiết hoạt động đặc biệt chưa có PCCM giáo viên, không được tự xếp. Tổng đối chiếu: ${data.all_expected_periods??$('nr').textContent} tiết. ${stale()?'Lịch đang hiển thị đã cũ so với dữ liệu/cấu hình; cần giải lại.':''}`;
 renderGrid();renderDataset();renderResult();
}
function renderGrid(){
 const type=$('viewtype').value,old=$('viewer').value;
 $('viewer').innerHTML=data[type].map(x=>`<option value="${esc(x.id)}">${esc(x.name)} (${esc(x.id)})</option>`).join('');
 if(data[type].some(x=>x.id===old))$('viewer').value=old;
 const id=$('viewer').value,lessons=result?.lessons||[];
 let h='<thead><tr><th>Buổi / Tiết</th>'+Array.from({length:config.days},(_,d)=>`<th>Thứ ${d+2}</th>`).join('')+'</tr></thead><tbody>';
 for(const sh of config.mode==='morning'?['am']:['am','pm']){
  h+=`<tr><th class="shift" colspan="${config.days+1}">${sh==='am'?'☀ BUỔI SÁNG':'◐ BUỔI CHIỀU'}</th></tr>`;
  for(let p=0;p<config.periods;p++){
   h+=`<tr><th>Tiết ${p+1}</th>`;
   for(let d=0;d<config.days;d++){
    const l=lessons.find(l=>l.day===d&&l.shift===sh&&p>=l.period&&p<l.period+l.length&&(type==='classes'?l.class_id:l.teacher)===id);
    const a=l&&data.assignments.find(a=>a.id===l.assignment),s=a&&data.subjects.find(s=>s.id===a.subject_id);
    const secondary=l&&(type==='classes'?data.teachers.find(t=>t.id===l.teacher)?.name:data.classes.find(c=>c.id===l.class_id)?.name);
    h+='<td>'+(l?`<div class="lesson"><b>${esc(a?.subject||l.subject)}${s?.sub_name?' · '+esc(s.sub_name):''}</b><small>${esc(secondary)}</small>${l.room?'<small>'+esc(l.room)+'</small>':''}${l.length===2?'<small>↔ Tiết đôi</small>':''}</div>`:'—')+'</td>';
   }h+='</tr>';
  }
 }$('grid').innerHTML=h+'</tbody>';$('empty').hidden=lessons.length>0;
}
function renderDataset(){
 let h='';
 if(tableView==='issues'){h=data.issues.map(i=>`<div class="warning ${i.level==='ERROR'?'error':''}"><b>${esc(i.code)}</b> · ${esc(i.message)}</div>`).join('');
  h+='<h3>Hoạt động chưa có phân công</h3><table><tr><th>Lớp</th><th>Hoạt động</th><th>Tiết</th></tr>'+data.pending_special.map(x=>`<tr><td>${esc(x.class_id)}</td><td>${esc(x.subject)}</td><td>${x.count}</td></tr>`).join('')+'</table>';
 }else if(tableView==='teachers'){h='<table><tr><th>Mã</th><th>Nhãn nguồn</th><th>Họ tên đầy đủ</th><th>Định danh</th><th>Tiết PCCM</th></tr>'+data.teachers.map(t=>`<tr><td>${esc(t.id)}</td><td>${esc(t.name)}</td><td>${esc(t.full_name||'Chưa xác minh')}</td><td>${esc(t.status)}</td><td>${data.assignments.filter(a=>a.teacher===t.id).reduce((s,a)=>s+a.count,0)}</td></tr>`).join('')+'</table>';
 }else if(tableView==='classes'){h='<table><tr><th>Mã lớp</th><th>Lớp</th><th>Ca học (chế độ phân ca)</th><th>Tiết môn học</th></tr>'+data.classes.map(c=>`<tr><td>${esc(c.id)}</td><td>${esc(c.name)}</td><td><select data-class="${esc(c.id)}" aria-label="Ca ${esc(c.name)}"><option value="am" ${c.shift==='am'?'selected':''}>Sáng</option><option value="pm" ${c.shift==='pm'?'selected':''}>Chiều</option></select></td><td>${data.assignments.filter(a=>a.class_id===c.id).reduce((s,a)=>s+a.count,0)}</td></tr>`).join('')+'</table>';
 }else{h='<table><tr><th>PCCM</th><th>GV</th><th>Lớp</th><th>Môn / phân môn</th><th>Tiết</th><th>Cặp tiết đôi</th><th>Mã phòng được phép</th></tr>'+data.assignments.map(a=>`<tr><td title="${esc(a.source_cells)}">${esc(a.id)} · dòng ${a.source_row||'V2'}</td><td>${esc(a.teacher)}</td><td>${esc(a.class_id)}</td><td>${esc(a.subject)} · ${esc(a.sub)}</td><td>${a.count}</td><td><input data-double="${esc(a.id)}" type="number" min="0" max="${Math.floor(a.count/2)}" value="${a.double_count}" aria-label="Cặp tiết đôi ${esc(a.id)}"></td><td><input data-rooms="${esc(a.id)}" value="${esc(a.room_ids.join(','))}" placeholder="TIN01" aria-label="Phòng ${esc(a.id)}"></td></tr>`).join('')+'</table>';
 }$('dataset').innerHTML=h;
}
function renderResult(){
 if(!result){$('result').textContent='Chưa có kết quả giải.';return;}
 const m=result.metrics||{},labels={gaps:'Tiết trống GV',visits:'Buổi lên trường GV',distribution:'Độ lệch phân bố',concentration:'Dồn môn trong ngày',preferences:'Phạt nguyện vọng',changes:'Bloc cũ thay đổi'};
 let h=`<div class="status ${esc(result.status)}">${esc(result.status)} ${stale()?'· LỊCH CŨ / CẦN GIẢI LẠI':''}</div><p>${result.placed} / ${result.required} tiết môn học · ${result.conflicts} xung đột · ${result.elapsed_seconds} giây · ${result.unscheduled_special} tiết đặc biệt chưa có PCCM.</p>`;
 h+='<div class="quality-grid">'+Object.entries(labels).map(([k,v])=>`<div>${v}<b>${m[k]??'—'}</b></div>`).join('')+'</div>';
 h+=`<p>Chứng minh tối ưu toàn cục theo cấu hình: ${result.global_optimal_proven?'CÓ':'CHƯA'}. ${result.optimality_scope==='local_frozen'?'Kết quả chỉ xét phạm vi cục bộ với các tiết ngoài phạm vi đã khóa. ':''}Mức ưu tiên đã chứng minh: ${esc((result.proven_priorities||[]).join(', ')||'Chưa có')}.</p>`;
 h+=(result.diagnostics||[]).map(x=>`<div class="warning">${esc(x)}</div>`).join('');
 h+='<table><tr><th>Giai đoạn</th><th>Trạng thái</th><th>Mục tiêu</th><th>Cận</th><th>Giây</th></tr>'+(result.phases||[]).map(p=>`<tr><td>${esc(p.name)}</td><td>${esc(p.status)}</td><td>${p.objective??'—'}</td><td>${p.best_bound??'—'}</td><td>${p.seconds}</td></tr>`).join('')+'</table>';
 if(result.verification)h+=`<p>Kiểm tra độc lập: ${result.verification.valid?'ĐẠT':'KHÔNG ĐẠT'}; đúng số tiết, giáo viên/môn, ca học, phòng, lịch nghỉ, tiết cố định, tiết đôi và phạm vi xếp lại.</p>`;
 $('result').innerHTML=h;
}
function showTab(id){document.querySelectorAll('main section').forEach(x=>x.classList.toggle('hidden',x.id!==id));document.querySelectorAll('nav button').forEach(x=>x.classList.toggle('active',x.dataset.tab===id));}
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
 busy=true;const snap=snapshot();$('solve').disabled=true;msg('Đang lập mô hình CP-SAT…');
 try{const job=await api('/api/solve',{data,config,previous,scope});
  for(;;){await new Promise(r=>setTimeout(r,500));const state=await api('/api/jobs/'+job.id);msg(state.progress);
   if(state.state==='error')throw Error(state.error);
   if(state.state==='done'){result=state.result;solvedSnapshot=snap;save();render();msg(`Hoàn tất: ${result.status} · ${result.placed}/${result.required} tiết. ${result.unscheduled_special} tiết đặc biệt vẫn chưa phân công.`);break;}}
 }finally{busy=false;$('solve').disabled=false;}
});
$('validate').onclick=guard(async()=>{readConfig();const r=await api('/api/validate',{data,config});msg(r.errors.length?r.errors.join(' · '):`Dữ liệu kỹ thuật hợp lệ; còn ${data.issues.length} cảnh báo/ghi nhận nguồn cần xem. Chưa phải nghiệm thu lịch thực tế.`);save();render();});
$('xlsx').onchange=guard(async e=>{if(busy)throw Error('Đang giải, chưa thể thay dữ liệu.');const f=e.target.files[0];if(!f)return;const bytes=new Uint8Array(await f.arrayBuffer());let s='';for(let i=0;i<bytes.length;i+=8192)s+=String.fromCharCode(...bytes.subarray(i,i+8192));const r=await api('/api/import',{base64:btoa(s)});data=r.data;result=null;solvedSnapshot='';save();render();msg('Đã đọc trực tiếp cả 5 sheet PCCM. Xem cảnh báo trước khi xếp.');e.target.value='';});
$('json').onchange=guard(async e=>{if(busy)throw Error('Đang giải, chưa thể thay dữ liệu.');const f=e.target.files[0];if(!f)return;const x=JSON.parse(await f.text());
 if(x.version===3){const check=await api('/api/validate',{data:x.data,config:x.config});if(check.errors.length)throw Error(check.errors.join('\n'));data=x.data;config=x.config;result=null;solvedSnapshot='';
  if(x.result?.lessons?.length){const v=await api('/api/validate',{data,config,lessons:x.result.lessons});if(v.schedule?.valid){result={...x.result,status:'FEASIBLE',global_optimal_proven:false,proven_priorities:[],verification:v.schedule};solvedSnapshot=snapshot();msg('Đã khôi phục lịch và kiểm tra lại ràng buộc cứng. Chứng minh tối ưu trong backup là ghi nhận lịch sử.');}else msg('Đã khôi phục dữ liệu; lịch backup không hợp lệ nên không dùng.');}
 }else{data=(await api('/api/migrate-v2',{data:x})).data;result=null;solvedSnapshot='';msg('Đã chuyển JSON V2 sang V3 riêng. Chưa xác minh PCCM.');}
 configUI();save();render();e.target.value='';});
$('backup').onclick=guard(()=>{readConfig();download(JSON.stringify({version:3,data,config,result,solvedSnapshot},null,2),'SMART_TKB_V3_backup.json');});
$('csv').onclick=guard(()=>{readConfig();if(!result?.lessons.length||stale())throw Error('Cần có lịch hiện hành đã giải thành công trước khi xuất CSV.');const rows=[['Lớp','Mã GV','Giáo viên','Môn','Phân môn','Thứ','Buổi','Tiết','Phòng'],...result.lessons.flatMap(l=>Array.from({length:l.length},(_,p)=>[data.classes.find(c=>c.id===l.class_id)?.name,l.teacher,data.teachers.find(t=>t.id===l.teacher)?.name,l.subject,data.assignments.find(a=>a.id===l.assignment)?.sub,l.day+2,l.shift==='am'?'Sáng':'Chiều',l.period+p+1,l.room||'']))];
 const cell=v=>{let s=String(v??'');if(/^[=+\-@]/.test(s))s="'"+s;return '"'+s.replace(/"/g,'""')+'"';};download('\ufeff'+rows.map(r=>r.map(cell).join(',')).join('\r\n'),'SMART_TKB_V3.csv','text/csv;charset=utf-8');});
$('print').onclick=()=>window.print();
guard(async()=>{const boot=await api('/api/bootstrap');token=boot.token;data=boot.data;config=boot.config;
 try{const saved=JSON.parse(localStorage.getItem(KEY)||'null');if(saved?.version===3){const v=await api('/api/validate',{data:saved.data,config:saved.config});if(!v.errors.length){data=saved.data;config=saved.config;solvedSnapshot=saved.solvedSnapshot||'';
  if(saved.result?.lessons?.length){const check=await api('/api/validate',{data,config,lessons:saved.result.lessons});if(check.schedule?.valid)result={...saved.result,status:'FEASIBLE',global_optimal_proven:false,proven_priorities:[],verification:check.schedule};else msg('Bản lưu dữ liệu đã mở; lịch cũ không qua kiểm tra độc lập nên cần giải lại.');}
 }}}catch(e){msg('Không dùng được bản lưu cũ; đang dùng PCCM SOURCE.');}
 configUI();render();
})();
