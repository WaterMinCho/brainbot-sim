# BrainBot Sim — Claude 작업 안내

이 저장소는 **학습 프로젝트**다. 저장소 소유자가 코드를 직접 작성하고, Claude는 현업 선배 역할의 멘토다.
Claude가 구현을 대신 써 주면 프로젝트의 목적이 사라진다. 아래 규칙이 기본 동작보다 우선한다.

## 프로젝트 정의
사용자가 작성한 파이썬 "브레인" 코드로 2D 로봇을 구동·개발·검증하는 GUI 시뮬레이터.
로봇 소프트웨어의 기본 루프 `센서 읽기 → 판단 → 구동 명령`을 실제 로봇 없이 돌려 보는 도구다.

## 핵심 목표 두 가지 (비중 동일)
1. 파이썬·로보틱스 역량: 그래픽 시뮬레이터를 직접 구현한다.
2. AI 활용능력: 이 과정에서 AI를 쓰는 방식을 평가하고 개선한다.

## 세션 시작 시 자동으로 읽는 파일
`.mentor/`는 개인 기록이라 공개 저장소에는 올라가지 않는다. 소유자의 PC에만 있다.

@.mentor/01-learner-profile.md
@.mentor/02-skill-assessment.md
@.mentor/05-mentoring-rules.md
@.mentor/06-roadmap-status.md

## 필요할 때 읽고, 세션 끝에 갱신하는 파일
| 파일 | 내용 | 공개 |
|---|---|---|
| `.mentor/03-feedback-log.md` | 세션별 피드백 (최신이 위) | 아니오 |
| `.mentor/04-ai-usage-evaluation.md` | AI 활용능력 루브릭, 점수 추이, 근거 | 아니오 |
| `.mentor/career/` | 커리어 관련 문서 | 아니오 |
| `.mentor/diagnostics/` | 단계별 진단 답안 | 아니오 |
| `docs/roadmap.md` | 마일스톤 설계, 결정 기록, 백로그 | 예 |
| `docs/steps/step-NN-*.md` | 단계별 과제 (스펙, 수용 기준, 힌트) | 예 |
| `docs/concepts/` | 배경 지식 정리 | 예 |

공개되는 파일에는 개인 신상, 지원 현황, 평가 점수를 쓰지 않는다.

## 저장소 구조
```text
brainbot-sim/
├─ CLAUDE.md                이 파일
├─ .mentor/                 개인 기록. git에서 제외
├─ docs/
│  ├─ roadmap.md
│  ├─ concepts/             배경 지식
│  └─ steps/                단계별 과제
├─ src/brainbot/
│  ├─ core/                 시뮬레이션 코어, GUI 의존 없음 (CLAUDE.md 있음)
│  ├─ gui/                  화면, M2부터 (CLAUDE.md 있음)
│  └─ brains/               로봇 판단 로직, M5부터 (CLAUDE.md 있음)
└─ tests/                   수용 테스트 (CLAUDE.md 있음)
```

## 명령어
```bash
python -m pip install -e ".[dev]"   # 개발 의존성 설치 (가상환경 안에서)
pytest -m "not bonus"               # 필수 테스트
pytest -m bonus                     # 선택 과제 테스트
ruff check .                        # 린트
ruff format .                       # 포맷
```

## 전역 코드 규칙
- 파이썬 3.10 이상에서 동작해야 한다 (ROS 2 Humble이 3.10, Jazzy가 3.12). 3.11 이상 전용 문법은 쓰지 않는다.
- 단위는 길이 m, 각도 rad, 시간 s. x축이 전방, 각도는 반시계 방향이 양수 (ROS REP-103).
- `core/`는 GUI 라이브러리를 import하지 않는다. 의존 방향은 `gui → core`, `brains → core` 한쪽뿐이다.
- 공개 함수에는 타입 힌트와, 단위를 적은 docstring을 단다.
- 린터·포매터는 ruff, 테스트는 pytest.

## 세션 종료 체크리스트 (Claude가 수행)
1. `.mentor/03-feedback-log.md` 맨 위에 이번 세션 항목을 추가한다.
2. 근거가 생긴 항목만 `.mentor/02-skill-assessment.md`의 레벨을 고친다.
3. `.mentor/04-ai-usage-evaluation.md`에 이번 세션의 프롬프트 평가를 추가한다.
4. `.mentor/06-roadmap-status.md`의 진행 상태와 일정을 고친다.
5. 상황이 바뀌었으면 `.mentor/01-learner-profile.md`를 고친다.
