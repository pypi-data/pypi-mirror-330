import re
from .예약어 import 한국어_파이썬_예약어

def 코드_번역(코드: str) -> str:
    패턴_맵 = []
    for 한국어, 파이썬 in 한국어_파이썬_예약어.items():
        정규식 = r"\b" + re.escape(한국어) + r"\b"
        패턴_맵.append((re.compile(정규식), 파이썬))

    줄들 = 코드.splitlines()
    번역된_줄들 = []

    for 줄 in 줄들:
        새_줄 = 줄
        for (정규식_패턴, 교체) in 패턴_맵:
            새_줄 = 정규식_패턴.sub(교체, 새_줄)
        번역된_줄들.append(새_줄)

    return "\n".join(번역된_줄들)
