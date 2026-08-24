from pathlib import Path

WORKFLOWS = [
    Path('.github/workflows/centos7-verify.yml'),
    Path('.github/workflows/centos7-release.yml'),
]

MARKER = 'PYTHON3_CANDIDATE'
ANCHOR = '''              cmake -S /tmp/glslang -B /tmp/glslang-build \\
                -DCMAKE_BUILD_TYPE=Release \\
'''
REPLACEMENT = '''              PYTHON3_CANDIDATE=
              if [[ -d /opt/python ]]; then
                while IFS= read -r candidate; do
                  if [[ -x "$candidate" ]] && "$candidate" -c "import sys; raise SystemExit(sys.version_info[0] != 3)" >/dev/null 2>&1; then
                    PYTHON3_CANDIDATE="$candidate"
                    break
                  fi
                done < <(find /opt/python -maxdepth 3 \\( -name python -o -name python3 \\) -print | sort)
              fi
              test -n "$PYTHON3_CANDIDATE"
              "$PYTHON3_CANDIDATE" --version

              cmake -S /tmp/glslang -B /tmp/glslang-build \\
                -DPYTHON_EXECUTABLE="$PYTHON3_CANDIDATE" \\
                -DCMAKE_BUILD_TYPE=Release \\
'''

for path in WORKFLOWS:
    text = path.read_text()
    if MARKER in text:
        raise SystemExit(f'{path}: Python 3 discovery block already present')
    if text.count(ANCHOR) != 1:
        raise SystemExit(f'{path}: expected exactly one glslang CMake anchor')
    path.write_text(text.replace(ANCHOR, REPLACEMENT, 1))
