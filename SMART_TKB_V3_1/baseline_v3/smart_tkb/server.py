"""Offline loopback HTTP API; no cloud service, telemetry or external assets."""
import argparse
import base64
import json
import secrets
import tempfile
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
from .importer import read_pccm, import_v2
from .solver import solve
from .validation import config_with_defaults, validate_problem, verify_schedule

ROOT=Path(__file__).resolve().parent.parent
TOKEN=secrets.token_urlsafe(32)
JOBS={};LOCK=threading.Lock();RUNNING=False

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args): pass
    def reply(self,status,obj):
        body=json.dumps(obj,ensure_ascii=False).encode()
        self.send_response(status);self.send_header('Content-Type','application/json; charset=utf-8')
        self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
    def local(self):
        host=self.headers.get('Host','')
        allowed={f'127.0.0.1:{self.server.server_port}',f'localhost:{self.server.server_port}'}
        if host not in allowed:self.reply(403,{'error':'Host không hợp lệ'});return False
        origin=self.headers.get('Origin')
        if origin and origin not in {'http://'+h for h in allowed}:
            self.reply(403,{'error':'Origin không hợp lệ'});return False
        return True
    def do_GET(self):
        if not self.local():return
        path=urlsplit(self.path).path
        if path=='/api/bootstrap':
            self.reply(200,dict(token=TOKEN,data=read_pccm(ROOT/'SOURCE/PCCM_INPUT_CODEX_5_NHOM.xlsx'),config=config_with_defaults()));return
        if path.startswith('/api/jobs/'):
            with LOCK:job=JOBS.get(path.rsplit('/',1)[-1]);payload=dict(job) if job else None
            self.reply(200 if payload else 404,payload or {'error':'Không có tác vụ'});return
        files={'/':'index.html','/app.js':'app.js','/style.css':'style.css'}
        if path not in files:self.reply(404,{'error':'Không tìm thấy'});return
        target=ROOT/'web'/files[path];body=target.read_bytes()
        self.send_response(200)
        self.send_header('Content-Type',{'html':'text/html; charset=utf-8','js':'text/javascript; charset=utf-8','css':'text/css; charset=utf-8'}[target.suffix[1:]])
        self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; object-src 'none'; frame-ancestors 'none'; base-uri 'none'")
        self.send_header('X-Content-Type-Options','nosniff');self.send_header('Cache-Control','no-store')
        self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
    def do_POST(self):
        global RUNNING
        if not self.local():return
        if not secrets.compare_digest(self.headers.get('X-CSRF-Token',''),TOKEN):self.reply(403,{'error':'Thiếu phiên ứng dụng hợp lệ'});return
        try:
            size=int(self.headers.get('Content-Length','0'))
            if not 0<size<=15_000_000:raise ValueError('Yêu cầu phải có kích thước 1..15 MB')
            body=json.loads(self.rfile.read(size));path=urlsplit(self.path).path
            if path=='/api/import':
                raw=base64.b64decode(body['base64'],validate=True)
                if len(raw)>10_000_000:raise ValueError('Workbook quá lớn')
                with tempfile.TemporaryDirectory(prefix='smart-tkb-') as tmp:
                    f=Path(tmp)/'upload.xlsx';f.write_bytes(raw)
                    with __import__('zipfile').ZipFile(f) as z:
                        if sum(i.file_size for i in z.infolist())>100_000_000:raise ValueError('Workbook giải nén vượt 100 MB')
                    data=read_pccm(f)
                self.reply(200,dict(data=data));return
            if path=='/api/migrate-v2':
                self.reply(200,dict(data=import_v2(body['data'])));return
            if path in ('/api/validate','/api/solve'):
                data=body['data'];c=config_with_defaults(body.get('config'));errors=validate_problem(data,c)
                if path=='/api/validate':
                    self.reply(200,dict(errors=errors,issues=data.get('issues',[]),schedule=verify_schedule(data,c,body['lessons']) if 'lessons' in body else None));return
                if errors:raise ValueError('\n'.join(errors))
                with LOCK:
                    if RUNNING:self.reply(409,{'error':'Đang có tác vụ giải. Chờ kết quả trước khi chạy tiếp.'});return
                    RUNNING=True;jobid=secrets.token_hex(8)
                    if len(JOBS)>=5:
                        JOBS.pop(next(iter(JOBS)))
                    JOBS[jobid]=dict(state='running',progress='Đang lập mô hình',result=None)
                def work():
                    global RUNNING
                    def report(msg):
                        with LOCK:JOBS[jobid]['progress']=msg
                    try:
                        result=solve(data,c,body.get('previous'),body.get('scope'),report)
                        with LOCK:JOBS[jobid].update(state='done',result=result)
                    except Exception as e:
                        with LOCK:JOBS[jobid].update(state='error',error=str(e))
                    finally:
                        with LOCK:RUNNING=False
                threading.Thread(target=work,daemon=True).start();self.reply(202,{'id':jobid});return
            self.reply(404,{'error':'API không tồn tại'})
        except (ValueError,KeyError,TypeError,OverflowError) as e:self.reply(400,{'error':str(e)})
        except Exception as e:self.reply(400,{'error':f'Không đọc được dữ liệu: {type(e).__name__}: {e}'})

def main():
    p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=8768);p.add_argument('--open',action='store_true');args=p.parse_args()
    server=ThreadingHTTPServer(('127.0.0.1',args.port),Handler)
    print(f'SMART TKB V3 Candidate — http://127.0.0.1:{args.port} — Ctrl+C để dừng',flush=True)
    if args.open: webbrowser.open(f'http://127.0.0.1:{args.port}')
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()

if __name__=='__main__':main()
