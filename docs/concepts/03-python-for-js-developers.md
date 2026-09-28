# 03. 자바스크립트 개발자를 위한 파이썬 대응표

## 도구
| 역할 | JS/TS | 파이썬 | 메모 |
|---|---|---|---|
| 프로젝트 선언 | package.json | pyproject.toml | |
| 의존성이 놓이는 곳 | node_modules | 가상환경 `.venv` | 가상환경은 직접 만들고 켠다. 안 켜면 전역에 설치된다 |
| 패키지 관리자 | npm, pnpm | pip | |
| 린트와 포맷 | ESLint, Prettier | ruff | |
| 테스트 | Jest, Vitest | pytest | |
| 타입 검사 | tsc | pyright, mypy | 선택 사항 |

## 언어
| 주제 | JS/TS | 파이썬 | 주의 |
|---|---|---|---|
| 타입 | 컴파일할 때 검사한다 | 타입 힌트는 실행할 때 무시된다 | 힌트가 틀려도 실행된다 |
| 인터페이스 | `interface` | `typing.Protocol` | M5에서 쓴다 |
| 불변 객체 | `Object.freeze`, `readonly` | `@dataclass(frozen=True)` | |
| 구조 분해 | `const [a, b] = f()` | `a, b = f()` | 튜플로 여러 값을 돌려주는 것이 관용적이다 |
| 배열 변환 | `map`, `filter` | 리스트 컴프리헨션 | |
| 동등 비교 | `===` | `==`는 값, `is`는 같은 객체 | `None`과는 `is None`으로 비교한다 |
| 없음 | `null`, `undefined` | `None` 하나 | |
| 빈 배열의 참거짓 | `[]`는 참 | `[]`는 거짓 | 조건문에서 자주 틀린다 |
| 나머지 연산 | `-1 % 5`는 `-1` | `-1 % 5`는 `4` | 각도 정규화에서 중요하다 |
| 나눗셈 | `7 / 2`는 `3.5` | `7 / 2`는 `3.5`, `7 // 2`는 `3` | |
| 기본 인자 | 호출할 때마다 새로 평가 | 함수를 정의할 때 한 번 평가 | `def f(x=[])`의 리스트는 호출 사이에 공유된다 |
| `this` | 암묵적 | `self`를 첫 인자로 적는다 | |
| 접근 제한 | `private`, `#field` | 관례로 `_name` | 강제되지 않는다 |
| 비동기 | Promise, async/await | asyncio, async/await | 이벤트 루프를 직접 돌려야 한다 |
| 동시성 | 단일 스레드와 이벤트 루프 | 스레드, 프로세스, asyncio | M9에서 다룬다 |

## 모듈과 패키지
- 폴더에 `__init__.py`가 있으면 패키지다.
- 이 프로젝트는 src 레이아웃을 쓴다. 코드는 `src/brainbot/`에 있고, `pip install -e .`를 하면 어디서든 `import brainbot`이 된다.
- `-e`는 editable의 약자다. 파일을 고치면 다시 설치하지 않아도 반영된다. `npm link`와 비슷하다.

## dataclass
```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    x: float
    y: float
```
생성자, 비교(`==`), 출력용 문자열이 자동으로 생긴다. `frozen=True`면 만든 뒤에 값을 바꿀 수 없다.
값을 바꾸고 싶으면 새 객체를 만든다. React에서 state를 직접 고치지 않고 새 객체로 바꾸는 것과 같다.

## 부동소수 비교
`0.1 + 0.2 == 0.3`은 자바스크립트와 똑같이 거짓이다. 테스트에서는 `pytest.approx`나 `math.isclose`를 쓴다.
```python
assert 0.1 + 0.2 == pytest.approx(0.3)
```

## 예외
잘못된 인자를 받으면 `ValueError`를 던진다. 자바스크립트의 `throw new Error()`에 해당한다.
파이썬은 예외의 종류를 세분해서 쓰는 문화다. `ValueError`(값이 틀림), `TypeError`(타입이 틀림), `KeyError`(키 없음)를 구분한다.
