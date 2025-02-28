한국어_파이썬_예약어 = {
    # ----- 파이썬 예약어 (keywords) -----
    # 논리값 / None
    "거짓": "False",
    "참": "True",
    "없음": "None",

    # 논리 연산
    "그리고": "and",
    "또는": "or",
    "아니다": "not",

    # 조건/반복
    "만약": "if",
    "아니고만약": "elif",     # elif
    "아니면": "else",
    "동안": "while",
    "각각": "for",
    "안에": "in",
    "중단": "break",
    "계속": "continue",

    # 예외 처리
    "시도": "try",
    "예외": "except",
    "결국": "finally",
    "발생": "raise",

    # 함수/클래스/람다
    "정의": "def",
    "클래스": "class",
    "람다": "lambda",
    "반환": "return",
    "넘어가기": "pass",      # pass

    # 비동기 처리
    "비동기": "async",
    "기다림": "await",

    # 패턴 매칭 (Python 3.10+)
    "매칭": "match",
    "경우": "case",
    "또는패턴": "|",         # OR 패턴
    "가드": "if",            # 가드 패턴 (case x if x > 0)
    "무시": "_",             # 와일드카드 패턴

    # 기타 키워드
    "삭제": "del",
    "전역": "global",
    "비전역": "nonlocal",
    "로서": "as",
    "은": "is",
    "에서": "from",
    "불러오기": "import",
    "단언": "assert",
    "함께": "with",
    "생성": "yield",
    "모두생성": "yield from", # yield from

    # 컴프리헨션 관련
    "리스트컴프리헨션": "[x for x in iterable]",  # 설명용
    "사전컴프리헨션": "{k:v for k,v in items}",   # 설명용
    "집합컴프리헨션": "{x for x in iterable}",    # 설명용
    "제너레이터컴프리헨션": "(x for x in iterable)", # 설명용

    # 특수 연산자
    "왈러스": ":=",          # 왈러스 연산자 (Python 3.8+)
    "언패킹": "*",           # 시퀀스 언패킹
    "사전언패킹": "**",       # 사전 언패킹

    # 타입 힌트 관련
    "타입힌트": ":",         # 변수 타입 힌트 (x: int = 10)
    "반환타입": "->",        # 함수 반환 타입 힌트

    # 문자열 포맷팅
    "포맷문자열": "f",       # f-string

    # 데코레이터
    "데코레이터": "@",       # 함수/클래스 데코레이터

    # 특수 메서드
    "진입점": "__enter__",   # 컨텍스트 매니저 진입
    "종료점": "__exit__",    # 컨텍스트 매니저 종료
    "초기화": "__init__",    # 객체 초기화
    "문자열화": "__str__",   # 문자열 표현
    "표현": "__repr__",      # 개발자용 문자열 표현
    "길이": "__len__",       # 객체 길이
    "호출": "__call__",      # 호출 가능 객체
    "반복자": "__iter__",    # 반복자 반환
    "다음": "__next__",      # 다음 요소 반환
    "컨테인먼트": "__contains__", # in 연산자
    "덧셈": "__add__",       # + 연산자
    "뺄셈": "__sub__",       # - 연산자
    "곱셈": "__mul__",       # * 연산자
    "나눗셈": "__truediv__", # / 연산자
    "정수나눗셈": "__floordiv__", # // 연산자
    "나머지": "__mod__",     # % 연산자
    "거듭제곱": "__pow__",   # ** 연산자
    "비교": "__eq__",        # == 연산자
    "부등호": "__lt__",      # < 연산자
    "인덱싱": "__getitem__", # [] 연산자
    "인덱스설정": "__setitem__", # [] = 연산자
    "속성겟터": "__getattr__", # 속성 접근
    "속성세터": "__setattr__", # 속성 설정

    # ----- 파이썬 내장 함수 (built-in functions) -----
    "절댓값": "abs",
    "모두참": "all",
    "하나참": "any",
    "아스키": "ascii",
    "이진수": "bin",
    "불리언": "bool",
    "중단점": "breakpoint",
    "바이트배열": "bytearray",
    "바이트": "bytes",
    "호출가능": "callable",
    "문자": "chr",
    "클래스메서드": "classmethod",
    "컴파일": "compile",
    "복소수": "complex",
    "삭제속성": "delattr",
    "사전": "dict",
    "디렉터리": "dir",
    "몫나머지": "divmod",
    "열거": "enumerate",
    "평가": "eval",
    "실행": "exec",
    "필터": "filter",
    "실수": "float",
    "형식": "format",
    "고정집합": "frozenset",
    "속성얻기": "getattr",
    "전역변수": "globals",
    "존재여부": "hasattr",
    "해시": "hash",
    "도움말": "help",
    "16진수": "hex",
    "객체ID": "id",
    "입력": "input",
    "정수": "int",
    "인스턴스여부": "isinstance",
    "서브클래스여부": "issubclass",
    "반복자": "iter",
    "길이": "len",
    "리스트": "list",
    "지역변수": "locals",
    "맵": "map",
    "최대값": "max",
    "메모리뷰": "memoryview",
    "최소값": "min",
    "다음값": "next",
    "객체": "object",
    "8진수": "oct",
    "열기": "open",
    "유니코드값": "ord",
    "거듭제곱": "pow",
    "출력": "print",
    "속성": "property",
    "범위": "range",
    "표현식": "repr",
    "역순": "reversed",
    "반올림": "round",
    "집합": "set",
    "설정속성": "setattr",
    "슬라이스": "slice",
    "정렬": "sorted",
    "정적메서드": "staticmethod",
    "문자열": "str",
    "합계": "sum",
    "슈퍼클래스": "super",
    "튜플": "tuple",
    "타입": "type",
    "변수들": "vars",
    "압축": "zip",
    "모듈가져오기": "__import__",

    # 타입 힌트 관련 모듈
    "타입힌트모듈": "typing",
    "리스트타입": "List",
    "튜플타입": "Tuple",
    "사전타입": "Dict",
    "집합타입": "Set",
    "옵션타입": "Optional",
    "유니온타입": "Union",
    "콜러블타입": "Callable",
    "모든타입": "Any",
    "문자열타입": "str",
    "정수타입": "int",
    "실수타입": "float",
    "불타입": "bool",
    "바이트타입": "bytes",

    # ----- 파이썬 내장 예외 (built-in exceptions) -----
    "예외": "Exception",
    "중단예외": "StopIteration",
    "비동기중단예외": "StopAsyncIteration",
    "산술오류": "ArithmeticError",
    "오버플로우오류": "OverflowError",
    "영으로나눔오류": "ZeroDivisionError",
    "부동소수점오류": "FloatingPointError",
    "어트리뷰트오류": "AttributeError",
    "버퍼오류": "BufferError",
    "EOF오류": "EOFError",
    "입출력오류": "IOError",
    "파일존재오류": "FileExistsError",
    "파일없음오류": "FileNotFoundError",
    "허용되지않는오류": "PermissionError",
    "프로세스찾을수없음오류": "ProcessLookupError",
    "참조오류": "ReferenceError",
    "메모리오류": "MemoryError",
    "인덱스오류": "IndexError",
    "키오류": "KeyError",
    "값오류": "ValueError",
    "타입오류": "TypeError",
    "가명오류": "NameError",
    "언바운드로컬오류": "UnboundLocalError",
    "모듈오류": "ModuleNotFoundError",
    "인포트오류": "ImportError",
    "중단오류": "InterruptedError",
    "시간초과오류": "TimeoutError",
    "런타임오류": "Runtime",
    "재귀오류": "RecursionError",
    "낙찰오류": "NotImplementedError",
    "부착오류": "OSError",
}
