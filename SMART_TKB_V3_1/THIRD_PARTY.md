# Dependency và giấy phép

Python 3.12.10 Windows x64: Python Software Foundation; package NuGet `python`, nguồn tải và SHA-512 xác minh trong `windows/PYTHON_PROVENANCE.json`. Giữ `windows/runtime/LICENSE.txt`, metadata và notice của runtime.

OR-Tools 9.15.6755: Google, Apache-2.0. openpyxl 3.1.5: MIT. Các dependency absl-py, numpy, pandas, protobuf, typing-extensions, immutabledict, et-xmlfile, python-dateutil, six, tzdata được ghim phiên bản/hash trong `windows/requirements-lock.txt`.

Toàn bộ wheel giữ nguyên byte, có `.dist-info/METADATA`, `RECORD`, giấy phép/notice đi kèm. Khi pip cài, giữ các thư mục giấy phép trong site-packages. Không xóa license hoặc thay đổi expected checksum để làm cài đặt thành công.

Gói là Candidate cho kiểm thử. Trước phân phối Production, đơn vị triển khai cần rà soát giấy phép, security update và nghiệm thu Windows. Không có kết luận rằng kiểm thử trên Linux chứng minh các DLL Windows đã chạy được.
