"""Native fixed-workspace gate. Only synthetic PDFs, fresh owned paths, no REINS login."""
import hashlib
import json
import platform
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import time

from importlib.util import spec_from_file_location, module_from_spec

spec = spec_from_file_location('pdf_fixture', Path(__file__).with_name('verify-install.py'))
fixture = module_from_spec(spec)
spec.loader.exec_module(fixture)


def main():
    archive, expected, bundle = sys.argv[1:]
    assert sys.platform == 'darwin' and platform.machine() == 'arm64'
    assert hashlib.sha256(Path(archive).read_bytes()).hexdigest() == expected
    print(json.dumps({'platform': platform.platform(), 'arch': platform.machine(), 'sha256': expected}), flush=True)
    with tempfile.TemporaryDirectory(prefix='sumai-native-mac-') as tmp:
        base = Path(tmp)
        with tarfile.open(archive) as source:
            source.extractall(base / 'download', filter='data')
        node = base / 'download/package/runtime/node'
        assert fixture.run(node, '-p', 'process.platform+"/"+process.arch').strip() == b'darwin/arm64'
        import os
        env = dict(os.environ, SUMAI_WORKSPACE_PACKAGE=str(Path(archive).resolve()))
        subprocess.run([node, '--test', str(Path(bundle).resolve())], env=env, check=True, timeout=300)
        renderer = base / 'download/package/browser/render-pdf-mac'
        assert b'PDFKit' in fixture.run(renderer, '-v')
        for index in [1, 2]:
            # Match the actual MCP protocol; --page-only testing missed this regression.
            args = ['-f', str(index), '-l', str(index), '-scale-to', '2450', '-jpeg', '-jpegopt', 'quality=90', '-singlefile', '-']
            jpeg = fixture.run(renderer, *args, input=fixture.synthetic_pdf())
            assert jpeg.startswith(b'\xff\xd8') and jpeg.endswith(b'\xff\xd9')
            image = base / f'page-{index}.jpg'
            image.write_bytes(jpeg)
            size = fixture.run('/usr/bin/sips', '-g', 'pixelWidth', '-g', 'pixelHeight', image)
            assert b'pixelWidth: 2450' in size and b'pixelHeight: 1470' in size
            pixel = base / f'pixel-{index}.bmp'
            fixture.run('/usr/bin/sips', '-z', '1', '1', '-s', 'format', 'bmp', image, '--out', pixel)
            bmp = pixel.read_bytes()
            offset = int.from_bytes(bmp[10:14], 'little')
            blue, green, red = bmp[offset:offset+3]
            assert (red > 200 and blue < 50) if index == 1 else (blue > 200 and red < 50)
        invalid = subprocess.run([renderer, '-f', '3', '-l', '3'], input=fixture.synthetic_pdf(), capture_output=True, timeout=30)
        assert invalid.returncode != 0
        print('PASS native MCP, two cases, restored drawing references, page identity/end, backup/restore/reinstall, private storage', flush=True)
        print('PASS PDFKit pages 1/2 colors and dimensions, out-of-range rejection', flush=True)
        chrome = Path('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
        profile = base / 'Chrome dedicated smoke'
        proc = subprocess.Popen([chrome, '--user-data-dir='+str(profile), '--no-first-run', 'about:blank'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            for _ in range(30):
                if (profile/'Local State').is_file(): break
                time.sleep(1)
            assert (profile/'Local State').is_file(), 'Chrome profile did not initialize'
            print('PASS real Chrome starts in fresh profile; extension consent, Gatekeeper, Codex desktop and REINS remain unverified', flush=True)
        finally:
            proc.terminate()
            proc.wait(timeout=30)


if __name__ == '__main__':
    main()
