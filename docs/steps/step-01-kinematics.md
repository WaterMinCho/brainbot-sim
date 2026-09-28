# Step 01 — 자세와 차동 구동 기구학

| | |
|---|---|
| 마일스톤 | M1 |
| 예상 시간 | 3~5시간 |
| 선행 | Step 00 완료 |
| 읽을 것 | `docs/concepts/01-coordinates-and-pose.md`, `docs/concepts/02-differential-drive.md` |
| 결과물 | `src/brainbot/core/pose.py`, `src/brainbot/core/diffdrive.py`, 초록 테스트, 적분 오차 표 |

## 왜 이것부터 하는가
화면보다 먼저 "로봇이 Δt 뒤에 어디에 있는가"를 계산하는 함수를 만든다. 시뮬레이터의 나머지가 전부 이 함수 위에 올라간다.
화면 없이 테스트로만 검증하는 이유는 세 가지다.
- 숫자가 틀리면 화면에서는 "뭔가 이상하다"로만 보인다. 테스트는 어디가 틀렸는지 알려 준다.
- 나중에 화면을 바꾸거나 ROS2를 붙여도 이 코드는 그대로 쓴다.
- 학습용 브레인을 돌릴 때는 화면 없이 수천 배 빠르게 돌려야 한다.

현업 연결: 실제 로봇이 바퀴 회전량으로 자기 위치를 추정할 때(오도메트리) 같은 식을 쓴다. ROS2의 `/odom` 토픽이 이 계산의 결과다.

## 스펙

### `src/brainbot/core/pose.py`
| 이름 | 시그니처 | 설명 |
|---|---|---|
| `normalize_angle` | `(theta: float) -> float` | 각도를 −π 이상 π 이하로 접는다. 방향은 그대로여야 한다 |
| `Pose2D` | 필드 `x`, `y`, `theta` (이 순서, 모두 `float`) | 불변. 값으로 비교된다 |

`Pose2D`는 받은 값을 그대로 저장한다. 정규화는 자세를 계산해서 돌려주는 함수의 책임이다.

### `src/brainbot/core/diffdrive.py`
| 이름 | 시그니처 | 설명 |
|---|---|---|
| `wheels_to_body` | `(v_left, v_right, wheel_base) -> tuple[float, float]` | 바퀴 속도를 (v, ω)로 |
| `body_to_wheels` | `(v, w, wheel_base) -> tuple[float, float]` | (v, ω)를 (v_left, v_right)로 |
| `step_unicycle` | `(pose: Pose2D, v, w, dt) -> Pose2D` | dt 뒤의 자세. 돌려주는 theta는 정규화되어 있다 |

오류 처리:
- `wheel_base`가 0 이하이면 `ValueError`
- `dt`가 음수이면 `ValueError`. 0이면 자세가 그대로다

단위는 m, m/s, rad, rad/s, s. docstring에 적는다.

## 수용 기준
```bash
pytest tests/test_step01_kinematics.py -m "not bonus"
```
전부 통과하고,
```bash
ruff check .
```
도 통과한다.

선택 과제:
```bash
pytest tests/test_step01_kinematics.py -m bonus
```

## 권장 순서
1. 테스트 파일을 처음부터 끝까지 읽는다. 스펙 표보다 테스트가 정확하다.
2. `pose.py`를 쓴다. `pytest -k "NormalizeAngle or Pose2D"`로 이 부분만 돌린다.
3. `wheels_to_body`, `body_to_wheels`를 쓴다. `pytest -k WheelConversion`.
4. `step_unicycle`을 오일러 적분으로 쓴다. `pytest -k StepUnicycle`.
5. 아래 실험 과제를 한다.
6. 시간이 되면 원호 적분으로 바꿔 선택 과제를 통과시킨다.

## 실험 과제 (필수): 적분 오차를 숫자로 본다
`experiments/step01_integration_error.py`를 만든다. 테스트가 아니라 실행해서 표를 출력하는 스크립트다.

- v = 1, ω = 1로 원 한 바퀴(2π초)를 돈다.
- Δt를 0.1, 0.01, 0.001로 바꿔 가며, 출발점으로 돌아왔을 때 위치가 얼마나 어긋났는지 잰다.
- 결과 표를 PR 본문에 붙인다.

| Δt | 스텝 수 | 위치 오차 (m) |
|---|---|---|
| 0.1 | | |
| 0.01 | | |
| 0.001 | | |

이 표에서 무엇이 보이는지 설명 확인 질문 1번에 쓴다.

## 흔한 실수
| 실수 | 증상 |
|---|---|
| 도를 그대로 `math.sin`에 넣는다 | 값이 전부 이상하다 |
| `theta`를 정규화하지 않고 돌려준다 | `test_theta_stays_in_range` 실패 |
| 자바스크립트의 `%`처럼 생각한다 | 음수 각도에서 결과가 다르다. 파이썬의 `%`는 부호가 다르게 동작한다 |
| `Pose2D`를 일반 클래스로 만든다 | `test_is_immutable`, `test_compares_by_value` 실패 |
| `dt == 0`을 오류로 처리한다 | `test_zero_dt_keeps_pose` 실패 |
| ω = 0일 때 v / ω를 계산한다 | `ZeroDivisionError` (원호 적분을 할 때) |

## 힌트
막히면 한 단계씩만 연다. 열었으면 PR의 AI 활용 내역 아래에 "힌트 N단계 사용"이라고 적는다.

<details>
<summary>normalize_angle — 1단계 (개념)</summary>

각도에 2π를 몇 번 더하거나 빼도 방향은 같다. "2π로 나눈 나머지"가 핵심이다.
나머지 연산의 결과는 0 이상 2π 미만인데, 원하는 범위는 −π에서 π다. 범위를 어떻게 옮길 수 있을까?
</details>

<details>
<summary>normalize_angle — 2단계 (절차)</summary>

1. 각도에 π를 더한다.
2. 2π로 나눈 나머지를 구한다.
3. π를 뺀다.

다른 방법: sin과 cos을 구한 뒤 atan2에 넣는다.
</details>

<details>
<summary>Pose2D — 1단계 (개념)</summary>

`docs/concepts/03-python-for-js-developers.md`의 dataclass 절을 본다. 불변으로 만드는 옵션이 있다.
</details>

<details>
<summary>step_unicycle — 1단계 (개념)</summary>

`docs/concepts/02-differential-drive.md`의 오일러 적분 식 세 줄을 그대로 코드로 옮긴다.
기존 `pose`를 고치지 않는다. 새 `Pose2D`를 만들어 돌려준다.
</details>

<details>
<summary>step_unicycle 원호 적분 — 1단계 (개념)</summary>

ω가 0에 가까울 때와 아닐 때를 나눈다. "0에 가깝다"의 기준을 얼마로 잡을지 스스로 정하고 이유를 PR에 적는다.
</details>

## 설명 확인 질문 (AI 없이, PR 본문에 쓴다)
1. 오일러 적분으로 원을 돌면 출발점으로 정확히 돌아오지 않는다. 왜 그런가? Δt를 10분의 1로 줄이면 오차가 어떻게 변하는가? 실험 표의 숫자로 설명한다.
2. `Pose2D`를 불변으로 만든 이유는 무엇인가? React의 state와 비교해 설명한다.
3. 각도를 정규화하지 않으면 생길 수 있는 버그를 하나 구체적으로 든다.
4. 차동 구동 로봇이 옆으로 움직이지 못한다는 것은 운동 방정식의 어느 부분에서 드러나는가?
5. `step_unicycle`이 `dt`를 인자로 받고 현재 시각을 직접 읽지 않는 이유는 무엇인가?

## 제출
1. 브랜치를 만든다: `git switch -c step-01-kinematics`
2. 의미 단위로 커밋한다. 한 번에 몰아서 커밋하지 않는다.
3. PR을 연다. 템플릿의 모든 칸을 채운다.
4. CI가 초록인지 확인한다.
5. 다음 세션에서 PR 링크나 코드를 보여 주면 리뷰한다.

## 리뷰에서 볼 것
- 정확성: 테스트 통과, 경계값 처리
- 설계: 함수 하나가 한 가지 일을 하는가, core가 다른 계층을 모르는가
- 파이썬다움: 타입 힌트, docstring, 이름, 불필요한 클래스가 없는가
- 실험: 표가 있고 해석이 숫자와 맞는가
- 커밋: 기록만 보고 작업 순서를 따라갈 수 있는가

## 이 단계의 AI 사용 규칙
| 해도 되는 것 | 하지 않는 것 |
|---|---|
| 개념 질문 ("오일러 적분이 왜 오차가 나는가") | 함수 구현을 통째로 받기 |
| 오류 메시지 해석 | 설명 확인 질문의 답을 AI로 쓰기 |
| 내가 쓴 코드의 리뷰 요청 | 테스트 파일을 고쳐서 통과시키기 |
| 공식 문서 찾기 | |
