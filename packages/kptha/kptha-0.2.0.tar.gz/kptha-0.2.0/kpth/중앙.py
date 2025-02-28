import sys
import os
from .번역기 import 코드_번역

def 주_실행():
    if len(sys.argv) < 2:
        print("⚠️  오류: 실행할 .kpy 파일을 지정해야 합니다.")
        print("예: ㅋㅍ 파일.kpy")
        sys.exit(1)

    파일_경로 = sys.argv[1]

    # 확장자 검사 (.kpy가 아닐 경우 오류)
    if not 파일_경로.endswith(".kpy"):
        print(f"⚠️  오류: 지원되지 않는 파일 확장자입니다. .kpy 파일만 실행 가능합니다. ({파일_경로})")
        sys.exit(1)

    # 파일 존재 여부 검사
    if not os.path.exists(파일_경로):
        print(f"⚠️  오류: 지정한 파일이 존재하지 않습니다. 경로를 확인하세요. ({파일_경로})")
        sys.exit(1)

    # 파일 읽기 및 실행
    try:
        with open(파일_경로, "r", encoding="utf-8") as 파일:
            한글코드 = 파일.read()

        변환된_코드 = 코드_번역(한글코드)
        exec(변환된_코드, globals())  # 변환된 코드 실행

    except Exception as 오류:
        print(f"⚠️  실행 중 오류 발생: {오류}")
