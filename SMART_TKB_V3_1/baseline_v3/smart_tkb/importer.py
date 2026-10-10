"""Read the five actual PCCM sheets. Never invent teacher identities."""
from collections import Counter, defaultdict
from hashlib import sha256
from pathlib import Path
import re
import unicodedata
import openpyxl

SHEETS = ['01_DANH_SACH_LOP', '02_DANH_SACH_GV', '03_DANH_MUC_MON',
          '04_PCCM_TOAN_TRUONG', '05_SO_TIET_THEO_LOP']

def text(v):
    return unicodedata.normalize('NFC', str(v or '').strip())

def integer(v):
    if isinstance(v, bool) or not isinstance(v, (int, float)) or v != int(v) or v < 0:
        raise ValueError(f'Số tiết phải là số nguyên không âm: {v!r}')
    return int(v)

def read_pccm(path):
    wb = openpyxl.load_workbook(path, data_only=True, read_only=True)
    if wb.sheetnames != SHEETS:
        raise ValueError('Workbook phải có đúng 5 sheet PCCM theo mẫu: ' + ', '.join(SHEETS))
    rows = {s: list(wb[s].values) for s in SHEETS}
    wb.close()
    issues = []
    def issue(level, code, message, **detail):
        issues.append(dict(level=level, code=code, message=message, **detail))
    classes, teachers, subjects, assignments, pending = [], [], [], [], []
    for n, r in enumerate(rows[SHEETS[0]][1:], 2):
        if not any(v is not None for v in r): continue
        if not r[1]: raise ValueError(f'Sheet lớp dòng {n}: thiếu mã lớp')
        classes.append(dict(id=text(r[1]), name=text(r[3]), grade=integer(r[2]),
                            shift='am', expected=integer(r[6]), curricular=integer(r[7]),
                            special=integer(r[8]), status=text(r[10]), source_row=n))
    for n, r in enumerate(rows[SHEETS[1]][1:], 2):
        if not any(v is not None for v in r): continue
        if not r[0]: raise ValueError(f'Sheet GV dòng {n}: thiếu mã')
        t = dict(id=text(r[0]), name=text(r[1]), full_name=text(r[2]),
                 aliases=text(r[3]), status=text(r[9]), source_row=n,
                 curricular=integer(r[7]), special=integer(r[8]))
        teachers.append(t)
        if t['status'] != 'VERIFIED' or not t['full_name']:
            issue('WARNING', 'TEACHER_ID_REVIEW', f"{t['id']} — {t['name']}: định danh chưa xác minh; không tự gộp/đổi tên.", teacher=t['id'])
    for n, r in enumerate(rows[SHEETS[2]][1:], 2):
        if not any(v is not None for v in r): continue
        subjects.append(dict(id=text(r[0]) + ':' + text(r[2]), base=text(r[0]),
                             name=text(r[1]), sub=text(r[2]), sub_name=text(r[3]),
                             kind=text(r[5]), status=text(r[6]), source_row=n))
        if text(r[6]) != 'VERIFIED':
            issue('WARNING', 'SUBJECT_REVIEW', f'{r[0]}:{r[2]} — giữ ký hiệu phân môn, chờ chú giải chính thức.')
    ids = {}
    for label, items in [('class', classes), ('teacher', teachers), ('subject', subjects)]:
        ids[label] = {x['id']: x for x in items}
        if len(ids[label]) != len(items):
            issue('ERROR', 'DUPLICATE_ID', f'Trùng mã {label}')
    seen = set()
    observations = []
    for n, r in enumerate(rows[SHEETS[3]][1:], 2):
        if not any(v is not None for v in r): continue
        if text(r[0]) == 'TỔNG CỘNG':
            declared_total = integer(r[7]); continue
        if not r[1] or not r[10] or not r[11] or not r[12]:
            issue('ERROR', 'MISSING_REFERENCE', f'PCCM dòng {n}: thiếu mã GV/lớp/môn/phân môn'); continue
        sid = text(r[11]) + ':' + text(r[12])
        a = dict(id=f'A{n:04}', teacher=text(r[1]), class_id=text(r[10]), subject_id=sid,
                 subject=text(r[3]), sub=text(r[12]), count=integer(r[7]),
                 status=text(r[8]), source_row=n, source_cells=text(r[14]),
                 source_conflict_cells=integer(r[13] or 0), double_count=0, room_ids=[])
        key=(a['teacher'], a['class_id'], sid)
        if key in seen: issue('ERROR', 'DUPLICATE_ASSIGNMENT', f'PCCM dòng {n}: trùng phân công', key=list(key))
        seen.add(key)
        if not a['count']: issue('ERROR', 'ZERO_ASSIGNMENT', f'PCCM dòng {n}: số tiết bằng 0')
        if a['teacher'] not in ids['teacher'] or a['class_id'] not in ids['class'] or sid not in ids['subject']:
            issue('ERROR', 'UNKNOWN_REFERENCE', f'PCCM dòng {n}: mã không có trong danh mục')
        else:
            if text(r[2]) != ids['teacher'][a['teacher']]['name'] or text(r[6]) != ids['class'][a['class_id']]['name'] or text(r[3]) != ids['subject'][sid]['name']:
                issue('ERROR', 'LABEL_MISMATCH', f'PCCM dòng {n}: nhãn không khớp mã danh mục')
            if integer(r[5]) != ids['class'][a['class_id']]['grade']:
                issue('ERROR', 'GRADE_MISMATCH', f'PCCM dòng {n}: khối không khớp lớp')
        assignments.append(a)
        matches = re.findall(r'(C\d+A\d+)_T([2-7])_([SC])(\d+)', a['source_cells'])
        if len(matches) != a['count']:
            issue('WARNING', 'TRACE_COUNT', f'PCCM dòng {n}: số ID truy vết không khớp số tiết')
        for c, d, sh, p in matches:
            if c != a['class_id']: issue('ERROR', 'TRACE_CLASS', f'PCCM dòng {n}: ID truy vết khác lớp')
            observations.append(dict(assignment=a['id'], teacher=a['teacher'], class_id=c,
                                     day=int(d)-2, shift='am' if sh=='S' else 'pm', period=int(p)-1, length=1, room=None))
    total = sum(a['count'] for a in assignments)
    if 'declared_total' in locals() and declared_total != total:
        issue('ERROR', 'TOTAL_MISMATCH', f'Tổng PCCM khai báo {declared_total}, tính lại {total}')
    actual = Counter()
    for a in assignments: actual[(a['class_id'], a['subject_id'].split(':')[0])] += a['count']
    expected = Counter(); expected_seen=set()
    for n, r in enumerate(rows[SHEETS[4]][1:], 2):
        if not any(v is not None for v in r): continue
        if text(r[0]) == 'TỔNG Ô CÓ LỊCH':
            expected_total=integer(r[3]); continue
        key=(text(r[4]), text(r[5])); count=integer(r[3])
        if key in expected_seen: issue('ERROR', 'DUPLICATE_EXPECTED', f'Sheet 05 dòng {n}: trùng lớp/môn')
        expected_seen.add(key); expected[key] += count
        if key[0] not in ids['class'] or key[1] not in {s['base'] for s in subjects}:
            issue('ERROR', 'EXPECTED_REFERENCE', f'Sheet 05 dòng {n}: mã chưa có trong danh mục')
        if key[1].startswith('HD') and actual[key] < count:
            pending.append(dict(class_id=key[0], subject_id=key[1], subject=text(r[2]), count=count-actual[key], reason='Chưa có phân công giáo viên trong sheet 04'))
        elif actual[key] != count:
            issue('ERROR', 'PCCM_COUNT_MISMATCH', f'{key}: PCCM {actual[key]}, sheet 05 {count}')
    for key in actual:
        if key not in expected: issue('ERROR', 'EXPECTED_MISSING', f'Không có định mức sheet 05: {key}')
    if 'expected_total' in locals() and expected_total != sum(expected.values()):
        issue('ERROR', 'EXPECTED_TOTAL', 'Tổng sheet 05 không khớp các dòng chi tiết')
    for c in classes:
        if sum(v for (cid, _),v in expected.items() if cid == c['id']) != c['expected']:
            issue('ERROR', 'CLASS_TOTAL', f"{c['id']}: tổng lớp không khớp sheet 01")
        if sum(a['count'] for a in assignments if a['class_id']==c['id'] and not a['subject_id'].startswith('HD')) != c['curricular']:
            issue('ERROR', 'CLASS_CURRICULAR', f"{c['id']}: số tiết môn học không khớp")
    for t in teachers:
        if sum(a['count'] for a in assignments if a['teacher']==t['id'] and not a['subject_id'].startswith('HD')) != t['curricular']:
            issue('ERROR', 'TEACHER_LOAD', f"{t['id']}: tổng tiết môn học GV không khớp")
        if sum(a['count'] for a in assignments if a['teacher']==t['id'] and a['subject_id'].startswith('HD')) > t['special']:
            issue('ERROR', 'TEACHER_SPECIAL_LOAD', f"{t['id']}: phân công đặc biệt vượt tổng sheet 02")
    if pending: issue('WARNING', 'SPECIAL_UNASSIGNED', f'{sum(x["count"] for x in pending)} tiết hoạt động đặc biệt thiếu PCCM giáo viên; không tự tạo phân công.')
    source_conflicts=sum(a['source_conflict_cells'] for a in assignments)
    if source_conflicts: issue('WARNING', 'SOURCE_CONFLICTS', f'{source_conflicts} ô được đánh dấu trùng giờ trong nguồn; lịch quan sát không phải lịch hợp lệ để khóa mặc định.')
    return dict(schema_version='3.0', source_sha256=sha256(Path(path).read_bytes()).hexdigest(),
                classes=classes, teachers=teachers, subjects=subjects, assignments=assignments,
                pending_special=pending, observations=observations, issues=issues,
                sheet_rows={s:len(rows[s])-1 for s in SHEETS}, required_periods=total,
                all_expected_periods=sum(expected.values()),
                data_accepted=False, production_ready=False)

def import_v2(data):
    """Explicit JSON migration, separate IDs/state; no reading V2 localStorage."""
    if not all(isinstance(data.get(k),list) for k in ['classes','teachers','assignments']):
        raise ValueError('JSON V2 thiếu classes/teachers/assignments')
    out=dict(schema_version='3.0', classes=[], teachers=[], subjects=[], assignments=[],
             issues=[dict(level='WARNING',code='V2_UNVERIFIED',message='JSON V2 chưa xác minh theo PCCM.')],
             pending_special=[], observations=[], data_accepted=False, production_ready=False)
    for c in data['classes']: out['classes'].append(dict(id=c['id'],name=c['name'],shift=c.get('shift','am'),grade=0))
    for t in data['teachers']: out['teachers'].append(dict(id=t['id'],name=t['name'],status='REVIEW',full_name=''))
    subjects={}
    for a in data['assignments']:
        sid=text(a['subject'])+':NONE'; subjects[sid]=dict(id=sid,base=text(a['subject']),name=text(a['subject']),sub='NONE')
        out['assignments'].append(dict(id=a['id'],teacher=a['teacher'],class_id=a['classId'],subject_id=sid,
                                      subject=text(a['subject']),sub='NONE',count=integer(a['count']),double_count=0,room_ids=[]))
    out['subjects']=list(subjects.values());out['required_periods']=sum(a['count'] for a in out['assignments'])
    out['all_expected_periods']=out['required_periods']
    return out
