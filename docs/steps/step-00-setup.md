# Step 00 — 환경, 저장소, 진단

| | |
|---|---|
| 마일스톤 | M0 |
| 예상 시간 | 2~3시간 |
| 읽을 것 | `docs/concepts/00-big-picture.md`, `docs/concepts/03-python-for-js-developers.md` |
| 결과물 | GitHub 저장소, 가상환경, 빨간 테스트 확인, 진단 답안 |

## 왜 필요한가
현업에서 새 프로젝트에 들어가면 첫날 하는 일이 환경을 세우고 테스트를 돌려 보는 것이다.
파이썬은 Node와 달리 가상환경을 직접 만들고 켜야 한다. 여기서 헷갈리면 이후 단계의 오류 절반이 환경 문제가 된다.

## 1. Git 사용자 정보
설정되어 있는지 확인한다.
```bash
git config --global user.name
```
아무것도 나오지 않으면 설정한다.
```bash
git config --global user.name "이름"
```
```bash
git config --global user.email "GitHub에 등록한 이메일"
```
공개 저장소에 개인 이메일을 남기고 싶지 않으면 GitHub의 noreply 주소를 쓴다 (GitHub → Settings → Emails).

## 2. 가상환경 만들기
프로젝트 폴더에서 실행한다.
```bash
python -m venv .venv
```
켜기 (PowerShell):
```powershell
.\.venv\Scripts\Activate.ps1
```
켜기 (Git Bash):
```bash
source .venv/Scripts/activate
```
PowerShell이 스크립트 실행을 막으면 실행 정책을 바꿔야 한다. 보안 설정을 바꾸는 일이므로 무엇을 하는 명령인지 먼저 찾아보고 직접 판단한다. 바꾸고 싶지 않으면 Git Bash를 쓴다.

확인:
```bash
python -c "import sys; print(sys.prefix)"
```
출력이 `.venv`로 끝나면 가상환경 안이다.

## 3. 의존성 설치
```bash
python -m pip install -e ".[dev]"
```
- `.[dev]`는 이 프로젝트와, `pyproject.toml`의 `dev` 묶음(pytest, ruff)을 함께 설치한다는 뜻이다.
- `-e`는 editable. 코드를 고쳐도 다시 설치할 필요가 없다.

## 4. 빨간 테스트 확인
```bash
pytest -m "not bonus"
```
`ModuleNotFoundError: No module named 'brainbot.core.diffdrive'`가 나오면 정상이다. 테스트는 있고 구현이 없다. Step 01에서 이것을 초록으로 바꾼다.

다른 오류가 나오면 환경 문제다. 오류 메시지 전체를 가져온다.

## 5. 린트
```bash
ruff check .
```
`All checks passed!`가 나와야 한다.

## 6. 저장소
이 저장소는 공개로 만든다. `.mentor/` 폴더에는 개인 기록이 들어 있고 `.gitignore`가 이 폴더를 제외한다.
기록은 PC에만 남으므로 따로 백업한다.

```bash
git init -b main
```
```bash
git add .
```
```bash
git status
```
올라갈 파일 목록을 눈으로 확인한다. `.venv`나 `.mentor`가 보이면 안 된다.
```bash
git commit -m "chore: project skeleton"
```
GitHub에서 빈 공개 저장소를 만든다. README나 .gitignore를 추가하는 옵션은 끈다.
```bash
git remote add origin https://github.com/<계정>/brainbot-sim.git
```
```bash
git push -u origin main
```
push한 뒤 GitHub의 Actions 탭을 본다. CI가 빨갛게 실패해야 정상이다.

## 7. VS Code
- 확장: Python, Ruff
- 명령 팔레트에서 "Python: Select Interpreter" → `.venv`

## 8. 진단
`.mentor/diagnostics/step-00-diagnostic.md`에 답을 적는다. 이 파일은 저장소에 올라가지 않는다.
- AI와 검색 없이, 아는 만큼만 쓴다. 모르면 "모름"이라고 쓴다.
- 점수를 매기려는 것이 아니다. 어디서부터 설명해야 하는지 알기 위한 것이다.
- 20분 안에 끝낸다.

## 완료 기준
- [ ] `python -c "import sys; print(sys.prefix)"`가 `.venv`를 가리킨다
- [ ] `pytest -m "not bonus"`가 `ModuleNotFoundError`로 실패한다
- [ ] `ruff check .` 통과
- [ ] GitHub에 첫 커밋이 올라갔다
- [ ] GitHub에 올라간 파일 목록에 `.mentor`가 없다
- [ ] Actions에서 CI가 돌았다 (빨간색)
- [ ] 진단 답안을 썼다

## 설명 확인 질문 (AI 없이, 다음 세션에서 말로 답한다)
1. 가상환경을 켜지 않고 `pip install`을 하면 어디에 설치되는가? 그것이 왜 문제인가?
2. `pip install -e .`에서 `-e`를 빼면 코드를 고칠 때마다 무엇을 해야 하는가?
3. `requires-python`을 `>=3.13`으로 올리면 나중에 어떤 문제가 생기는가?
4. CI가 3.10과 3.13 두 버전으로 도는 이유는 무엇인가?

## 이 단계의 AI 사용 규칙
오류 메시지 해석과 개념 질문은 해도 된다. 진단 답안과 설명 확인 질문은 AI 없이 쓴다.
