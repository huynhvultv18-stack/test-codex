"""Lossless schedule exchange and independent recomputation after restore."""
import csv,io,json,base64
from openpyxl import Workbook,load_workbook
from .special import prepare_special,special_report
from .validation import config_with_defaults,verify_schedule,metrics,teacher_visits
from .quality import features,class_ids
COLUMNS=['assignment','teacher','class_id','subject_id','day','shift','period','length','room','class_ids','activity_ids','activity_status','activity_type','shared_teacher_group','is_special']
def summarize_schedule(data,config,lessons):
 c=config_with_defaults(config);working,c,context=prepare_special(data,c)
 v=verify_schedule(working,c,lessons)
 if not v['valid']:raise ValueError('Lịch nhập không hợp lệ: '+'; '.join(v['errors']))
 report=special_report(context,lessons)
 return dict(status='FEASIBLE',lessons=lessons,required=context['curricular_required']+context['verified'],placed=sum(r.get('length',1)*len(class_ids(r)) for r in lessons if r.get('activity_status')!='SCENARIO'),scenario_placed=report['scheduled_scenario'],model_required=v['required'],scheduled_class_periods=v['placed'],conflicts=v['conflicts'],metrics=metrics(working,c,lessons),quality_scores={k:x for k,x in features(working,c,lessons).items() if k!='values'},teacher_visits=teacher_visits(working,lessons),verification=v,special_report=report,simulation=report['simulation'],scenario_assumptions=report['assumptions'],unscheduled_special=report['pending'],all_source_periods=context['curricular_required']+context['total'],official_complete=report['official_complete'],elapsed_seconds=None,phases=[],proven_priorities=[],global_optimal_proven=False,lexicographic_optimal_proven=False,optimality_scope='restored_verified_schedule',diagnostics=['Lịch nhập được kiểm tra lại; chứng minh tối ưu lịch sử không được kế thừa.'],data_accepted=False,windows_accepted=False,production_ready=False)
def export_schedule(data,config,lessons,fmt):
 result=summarize_schedule(data,config,lessons)
 rows=[]
 for r in lessons:
  row=[]
  for key in COLUMNS:
   value=r.get(key)
   if key in ('class_ids','activity_ids'):value=json.dumps(value or ([r['class_id']] if key=='class_ids' else []))
   if key=='is_special':value=int(bool(value))
   if isinstance(value,str) and value.startswith(('=','+','-','@')):value="'"+value
   row.append(value)
  rows.append(row)
 if fmt=='csv':
  stream=io.StringIO(newline='');writer=csv.writer(stream);writer.writerow(COLUMNS);writer.writerows(rows);return ('\ufeff'+stream.getvalue()).encode('utf-8')
 if fmt!='xlsx':raise ValueError('Định dạng phải là csv/xlsx')
 wb=Workbook();ws=wb.active;ws.title='TKB';ws.append(COLUMNS)
 for row in rows:ws.append(row)
 ws.freeze_panes='A2';ws.auto_filter.ref=ws.dimensions
 meta=wb.create_sheet('KIEM_CHUNG');meta.append(['Thuộc tính','Giá trị'])
 for key in ('status','required','placed','scenario_placed','conflicts','simulation','official_complete','data_accepted','windows_accepted','production_ready'):meta.append([key,result[key]])
 special=wb.create_sheet('HOAT_DONG_PENDING');special.append(['activity_id','classes','count','reasons'])
 for r in result['special_report']['pending_details']:special.append([r['activity_id'],','.join(r['class_ids']),r['count'],'; '.join(r['reasons'])])
 out=io.BytesIO();wb.save(out);return out.getvalue()
def import_schedule(data,config,raw,fmt):
 if fmt=='csv':table=list(csv.reader(io.StringIO(raw.decode('utf-8-sig'))))
 elif fmt=='xlsx':
  import zipfile
  with zipfile.ZipFile(io.BytesIO(raw)) as z:
   if sum(i.file_size for i in z.infolist())>100_000_000:raise ValueError('Workbook quá lớn khi giải nén')
  wb=load_workbook(io.BytesIO(raw),read_only=True,data_only=False)
  if 'TKB' not in wb.sheetnames:raise ValueError('Cần sheet TKB; PCCM dùng nút nhập riêng')
  table=list(wb['TKB'].values);wb.close()
 else:raise ValueError('Định dạng phải là csv/xlsx')
 if not table or list(table[0])!=COLUMNS:raise ValueError('Cột lịch không đúng định dạng V3.1')
 working,_,_=prepare_special(data,config_with_defaults(config));assign={a['id']:a for a in working['assignments']};lessons=[]
 for values in table[1:]:
  if not any(v is not None and v!='' for v in values):continue
  r=dict(zip(COLUMNS,values))
  for key in ('day','period','length'):r[key]=int(r[key])
  for key in ('teacher','room','activity_status','activity_type','shared_teacher_group'):r[key]=r[key] or None
  for key in ('class_ids','activity_ids'):r[key]=json.loads(r[key])
  r['is_special']=bool(int(r['is_special'] or 0))
  a=assign.get(r['assignment']);r['subject']=a['subject'] if a else ''
  lessons.append(r)
 return summarize_schedule(data,config,lessons)
