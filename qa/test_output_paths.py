"""Verify that real pytest runs retain complete, separate output folders offline."""
import base64
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest


ROOT = next(parent for parent in Path(__file__).resolve().parents if (parent / "pytest.ini").is_file())
PNG = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/l9sAAAAASUVORK5CYII='
SOURCE = '''import base64
from pathlib import Path
import pytest

class Browser:
    current_url = "https://example.com/index.php?route=account/login"
    def save_screenshot(self, path):
        Path(path).write_bytes(base64.b64decode("PNG_DATA"))
    def get_screenshot_as_base64(self):
        return "PNG_DATA"
    def find_elements(self, *args):
        return []

@pytest.fixture
def driver(request):
    browser = Browser()
    request.node._browser = browser
    return browser

def test_offline_checkpoint(checkpoint):
    checkpoint("login")
'''.replace('PNG_DATA', PNG)


class OutputPathsTests(unittest.TestCase):
    def run_pytest(self, directory, *options):
        test_file = directory / 'test_sample.py'
        test_file.write_text(SOURCE)
        result = subprocess.run(
            [sys.executable, '-m', 'pytest', '-c', str(ROOT / 'pytest.ini'),
             str(test_file), '--screenshots=all', '-q', *options],
            cwd=directory, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_default_reruns_preserve_reports_screenshots_and_checkpoints(self):
        with TemporaryDirectory(dir=Path(__file__).parent) as temporary:
            directory = Path(temporary).resolve()
            self.run_pytest(directory)
            first = next((directory / 'reports/runs').iterdir())
            saved = {p.relative_to(first): p.read_bytes() for p in first.rglob('*') if p.is_file()}
            self.run_pytest(directory)
            runs = sorted((directory / 'reports/runs').iterdir())
            self.assertEqual(len(runs), 2)
            for run in runs:
                self.assertTrue((run / 'overview.html').is_file())
                self.assertEqual(len(list((run / 'screenshots').glob('*.png'))), 1)
                self.assertEqual(len(list((run / 'screenshots').glob('*.json'))), 1)
                self.assertEqual(len(list((run / 'steps').glob('*.png'))), 1)
            for name, data in saved.items():
                self.assertEqual((first / name).read_bytes(), data)
            latest = (directory / 'reports/latest.html').read_text()
            self.assertIn(f'runs/{runs[-1].name}/overview.html', latest)

    def test_explicit_evidence_directory_keeps_report_and_images_together(self):
        with TemporaryDirectory(dir=Path(__file__).parent) as temporary:
            directory = Path(temporary).resolve()
            output = directory / 'chosen-run'
            self.run_pytest(directory, f'--evidence-dir={output}')
            self.assertTrue((output / 'overview.html').is_file())
            self.assertEqual(len(list((output / 'screenshots').glob('*.png'))), 1)
            self.assertTrue((output / 'steps/test_offline_checkpoint-login.png').is_file())
            self.assertFalse((directory / 'reports').exists())

    def test_default_collection_only_does_not_create_output(self):
        with TemporaryDirectory(dir=Path(__file__).parent) as temporary:
            directory = Path(temporary).resolve()
            self.run_pytest(directory, '--collect-only')
            self.assertFalse((directory / 'reports').exists())
