from pathlib import Path

WORKFLOWS = [
    Path('.github/workflows/centos7-verify.yml'),
    Path('.github/workflows/centos7-release.yml'),
]
OLD = 'find /opt/python -maxdepth 3 \\( -name python -o -name python3 \\) -print | sort'
NEW = 'find /opt/python -mindepth 3 -maxdepth 3 \\( -name python -o -name python3 \\) -print | sort'

for path in WORKFLOWS:
    text = path.read_text()
    if text.count(OLD) != 1:
        raise SystemExit(f'{path}: expected exactly one Python search expression')
    path.write_text(text.replace(OLD, NEW, 1))
