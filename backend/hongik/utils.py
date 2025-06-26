import os
import time
import subprocess
import re
from django.conf import settings
from django.core.cache import caches


class HongikInterpreter:
    def __init__(self):
        self.process = subprocess.Popen(
            [settings.HONGIK_INTERPRETER_PATH],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            bufsize=1,
        )
        # 환영 메시지 건너뛰기
        welcome_pattern = re.compile(r'^.*?>>>', re.DOTALL)
        welcome_output = ""
        start_time = time.time()
        while (time.time() - start_time) < 5:
            char = self.process.stdout.read(1)
            if not char: break
            welcome_output += char
            if welcome_pattern.search(welcome_output):
                break

    def execute(self, code_line):
        self.process.stdin.write(code_line + "\n")
        self.process.stdin.flush()
        output = ""
        start_time = time.time()
        prompt_pattern = re.compile(r'>>> |\.\.\. ')  # 정규식 확장
        while (time.time() - start_time) < 5:
            char = self.process.stdout.read(1)
            if not char: break
            output += char
            if prompt_pattern.search(output):
                break
            # 프롬프트 제거
        parts = output.split(">>>")
        return parts[0].strip()


# 세션별 인터프리터 인스턴스 관리
user_sessions = {}
cache = caches['default']

def get_interpreter(session_id):
    if cache.get(session_id) is None:
        cache.set(session_id, HongikInterpreter(), timeout=3600)  # 1시간 유지
    return cache.get(session_id)


def run_code(code):
    process = subprocess.Popen(
        [settings.HONGIK_INTERPRETER_PATH],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding='utf-8',
        bufsize=1,
    )
    # 환영 메시지 건너뛰기
    welcome_pattern = re.compile(r'^.*?>>>', re.DOTALL)
    welcome_output = ""
    start_time = time.time()
    while (time.time() - start_time) < 5:
        char = process.stdout.read(1)
        if not char: break
        welcome_output += char
        if welcome_pattern.search(welcome_output):
            break

    output_lines = []
    code_lines = [line.strip() for line in code.split('\n') if line.strip()]
    for line in code_lines:
        process.stdin.write(line + "\n")
        process.stdin.flush()
        output = ""
        start_time = time.time()
        prompt_found = False
        while (time.time() - start_time) < 5:
            char = process.stdout.read(1)
            if not char: break
            output += char
            if ">>>" in output:
                prompt_found = True
                break
        if prompt_found:
            parts = output.split(">>>")
            result = parts[0].strip()
            if result:
                output_lines.append(result)
    try:
        process.stdin.close()
        process.terminate()
        process.wait(timeout=1)
    except:
        pass
    return '\n'.join(output_lines)
