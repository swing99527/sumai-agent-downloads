"""Exercise the distribution on an Apple Silicon runner using synthetic data."""
import hashlib
import json
import os
from pathlib import Path
import platform
import stat
import subprocess
import sys
import tarfile
import tempfile
import time


def run(*args, **kwargs):
    return subprocess.check_output(args, timeout=45, **kwargs)


def synthetic_pdf():
    objects = [b'<< /Type /Catalog /Pages 2 0 R >>',
               b'<< /Type /Pages /Kids [3 0 R 5 0 R] /Count 2 >>']
    for index, color in [(4, b'1 0 0'), (6, b'0 0 1')]:
        objects.append(b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 300 180] /Resources << >> /Contents %d 0 R >>' % index)
        paint = color + b' rg 0 0 300 180 re f\n'
        objects.append(b'<< /Length %d >>\nstream\n' % len(paint) + paint + b'endstream')
    pdf = bytearray(b'%PDF-1.4\n')
    offsets = [0]
    for i, obj in enumerate(objects, 1):
        offsets.append(len(pdf))
        pdf.extend(b'%d 0 obj\n' % i + obj + b'\nendobj\n')
    start = len(pdf)
    pdf.extend(b'xref\n0 7\n0000000000 65535 f \n')
    for offset in offsets[1:]:
        pdf.extend(b'%010d 00000 n \n' % offset)
    pdf.extend(b'trailer\n<< /Size 7 /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n' % start)
    return bytes(pdf)


def main():
    archive, expected = sys.argv[1:]
    assert sys.platform == 'darwin' and platform.machine() == 'arm64'
    assert hashlib.sha256(Path(archive).read_bytes()).hexdigest() == expected
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        project = base / '空の案件 Folder'
        project.mkdir()
        with tarfile.open(archive) as source:
            source.extractall(base / 'download', filter='data')
        install = base / 'download' / 'install.mjs'
        node = install.parent / 'package/runtime/node'
        assert run(node,'-p','process.platform+"/"+process.arch').strip() == b'darwin/arm64'
        def setup():
            return json.loads(run(node, install, project, 'Codex'))
        first = setup()
        assert first['status'] == 'installed' and first['candidate'] == '27'
        assert setup()['status'] == 'already-installed'
        client = Path(first['client'])
        case = Path(first['browser']['exchange']).parent
        assert case.stat().st_uid == os.getuid() and stat.S_IMODE(case.stat().st_mode) == 0o700
        assert not (case / 'host.json').exists()
        state = json.loads(run(first['node'],client,project,'status'))
        assert state['connected'] is False and state['extensionId'] == 'hoadgoaopafcjbgabnlbannhnfoghbld'
        print('PASS native empty installation, reinstall, private case, honest disconnected status',flush=True)
        renderer = client.parent / 'render-pdf-mac'
        assert b'PDFKit' in run(renderer,'-v')
        for index in [1,2]:
            args = ['-f','1','-l','1','-scale-to','2450','-jpeg','-jpegopt','quality=90','-singlefile','-'] if index == 1 else ['--page','2']
            jpeg = run(renderer,*args,input=synthetic_pdf())
            assert jpeg.startswith(b'\xff\xd8') and jpeg.endswith(b'\xff\xd9')
            image = base / f'page-{index}.jpg'
            image.write_bytes(jpeg)
            size = run('/usr/bin/sips','-g','pixelWidth','-g','pixelHeight',image)
            assert b'pixelWidth: 2450' in size and b'pixelHeight: 1470' in size, size
            sample = base / 'pixel.bmp'
            run('/usr/bin/sips','-z','1','1','-s','format','bmp',image,'--out',sample)
            bmp = sample.read_bytes()
            offset = int.from_bytes(bmp[10:14],'little')
            blue,green,red = bmp[offset:offset+3]
            assert (red > 200 and blue < 50) if index == 1 else (blue > 200 and red < 50), (index,blue,green,red)
        invalid = subprocess.run([renderer,'--page','3'],input=synthetic_pdf(),capture_output=True,timeout=30)
        assert invalid.returncode != 0
        print('PASS macOS PDFKit, two source pages, correct page colors and size, missing page rejected',flush=True)
        assert json.loads(run(first['node'],client,project,'open-store'))['status'] == 'store-opened'
        profile = Path(state['profile'])
        for _ in range(45):
            if (profile/'Local State').is_file():
                break
            time.sleep(1)
        assert (profile/'Local State').is_file(), 'Dedicated Chrome did not initialize its profile'
        assert json.loads(run(first['node'],client,project,'status'))['connected'] is False
        print('PASS Google Chrome starts in a dedicated project profile; store consent and REINS require live validation',flush=True)


if __name__ == '__main__':
    main()
