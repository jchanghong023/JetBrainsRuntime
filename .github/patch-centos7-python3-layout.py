from pathlib import Path

WORKFLOWS = [
    Path('.github/workflows/centos7-verify.yml'),
    Path('.github/workflows/centos7-release.yml'),
]
OLD = '                done < <(find /opt/python -path "*/bin/python*" -print | sort)\n'
NEW = '''                done < <(\n                  {\n                    find /usr/local/bin -maxdepth 1 -name "python3*" -print 2>/dev/null || true\n                    find -L /opt/python -path "*/bin/python" -print 2>/dev/null || true\n                  } | sort -V\n                )\n'''

for path in WORKFLOWS:
    text = path.read_text()
    if text.count(OLD) != 1:
        raise SystemExit(f'{path}: expected exactly one Python candidate search')
    path.write_text(text.replace(OLD, NEW, 1))
