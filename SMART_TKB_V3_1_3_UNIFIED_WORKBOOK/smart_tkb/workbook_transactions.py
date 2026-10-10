"""Short-lived, single-use previews. Client controls reviewed replacement/undo."""
import secrets
import threading
import time
from copy import deepcopy
from .workbook import parse_workbook, changes, fingerprint, export_errors

class PreviewStore:
 def __init__(self,ttl=900,capacity=8):self.ttl=ttl;self.capacity=capacity;self.entries={};self.lock=threading.Lock()
 def preview(self,raw,current):
  report=parse_workbook(raw);token=secrets.token_urlsafe(24)
  public={k:v for k,v in report.items() if k!='state'};public['preview_token']=token;public['expires_in_seconds']=self.ttl
  if report['valid']:public['changes']=changes(current,report['state'])
  public['current_fingerprint']=fingerprint(current)
  with self.lock:
   self.entries={k:v for k,v in self.entries.items() if v['expires']>time.monotonic()}
   while len(self.entries)>=self.capacity:self.entries.pop(next(iter(self.entries)))
   self.entries[token]=dict(report=deepcopy(report),current_hash=public['current_fingerprint'],expires=time.monotonic()+self.ttl)
  return public
 def get(self,token):
  item=self.entries.get(token)
  if not item or item['expires']<=time.monotonic():raise ValueError('Xem trước đã hết hạn; chọn lại workbook')
  return item
 def errors(self,token):
  with self.lock:return export_errors(self.get(token)['report'])
 def commit(self,token,current,acknowledge_warnings=False):
  with self.lock:
   item=self.get(token);r=item['report']
   if not r['valid']:raise ValueError('Workbook có lỗi; không thể xác nhận nhập')
   if item['current_hash']!=fingerprint(current):raise ValueError('Dữ liệu phiên đã đổi sau khi xem trước; chọn lại workbook')
   if r['warnings'] and acknowledge_warnings is not True:raise ValueError('Cần xác nhận đã xem cảnh báo dữ liệu chưa xác minh')
   result=deepcopy(r['state']);del self.entries[token]
   return result
