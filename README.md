# BrainBot Sim

내가 쓴 파이썬 "브레인" 코드로 2D 로봇을 움직여 보는 GUI 시뮬레이터.
센서 읽기 → 판단 → 구동 명령으로 이어지는 로봇 소프트웨어 루프를, 실제 로봇 없이 개발하고 검증하려고 만든다.

> 학습 프로젝트입니다. 프론트엔드 개발자가 로보틱스로 전환하면서 기구학, 센서 모델, 경로계획, ROS2 연동을 단계별로 직접 구현합니다.

## 현재 상태
M0 (환경·저장소) 진행 중. 전체 계획은 [docs/roadmap.md](docs/roadmap.md).

## 개발 환경 준비
```bash
python -m venv .venv
```
가상환경 활성화는 셸마다 다릅니다. [docs/steps/step-00-setup.md](docs/steps/step-00-setup.md) 참고.
```bash
python -m pip install -e ".[dev]"
```
```bash
pytest -m "not bonus"
```

## 구조
| 경로 | 역할 |
|---|---|
| `src/brainbot/core/` | 시뮬레이션 코어. 화면 없이 테스트로 검증 |
| `src/brainbot/gui/` | 화면 (M2부터) |
| `src/brainbot/brains/` | 로봇 판단 로직 (M5부터) |
| `tests/` | 단계별 수용 테스트 |
| `docs/concepts/` | 구현하면서 정리한 배경 지식 |

## 문서
- [로드맵](docs/roadmap.md)
- [배경 지식: 큰 그림](docs/concepts/00-big-picture.md)
