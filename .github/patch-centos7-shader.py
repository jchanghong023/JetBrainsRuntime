from pathlib import Path

WORKFLOWS = [
    Path('.github/workflows/centos7-verify.yml'),
    Path('.github/workflows/centos7-release.yml'),
]

ANCHOR = '              echo "Build libc:"\n'
MARKER = 'GLSLANG_COMMIT=77551c429f86c0e077f26552b7c1c0f12a9f235e'
BLOCK = r'''              GLSLANG_VERSION=11.13.0
              GLSLANG_COMMIT=77551c429f86c0e077f26552b7c1c0f12a9f235e
              rm -rf /tmp/glslang /tmp/glslang-build
              git clone --depth 1 --branch "$GLSLANG_VERSION" https://github.com/KhronosGroup/glslang.git /tmp/glslang
              test "$(git -C /tmp/glslang rev-parse HEAD)" = "$GLSLANG_COMMIT"
              cmake -S /tmp/glslang -B /tmp/glslang-build \
                -DCMAKE_BUILD_TYPE=Release \
                -DENABLE_OPT=OFF \
                -DBUILD_TESTING=OFF \
                -DENABLE_HLSL=OFF \
                -DINSTALL_GTEST=OFF
              cmake --build /tmp/glslang-build --target glslangValidator --parallel 2
              install -m 0755 /tmp/glslang-build/StandAlone/glslangValidator /usr/local/bin/glslangValidator
              glslangValidator --version
              printf "%s\n" "#version 450" "layout(local_size_x = 1) in;" "void main() {}" > /tmp/jbr-vulkan-smoke.comp
              glslangValidator --target-env vulkan1.2 -x -DSTAGE_COMP -o /tmp/jbr-vulkan-smoke.h /tmp/jbr-vulkan-smoke.comp
              test -s /tmp/jbr-vulkan-smoke.h

'''

for path in WORKFLOWS:
    text = path.read_text()
    if MARKER in text:
        raise SystemExit(f'{path}: shader compiler block already present')
    if text.count(ANCHOR) != 1:
        raise SystemExit(f'{path}: expected exactly one insertion anchor')
    path.write_text(text.replace(ANCHOR, BLOCK + ANCHOR, 1))
