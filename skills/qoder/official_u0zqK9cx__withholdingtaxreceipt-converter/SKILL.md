---
name: withholdingtaxreceipt-converter
description: Korean withholding tax receipt PDF (YYYY_원천징수 영수증.pdf)를 Markdown (withholdingtaxreceipt_YYYY_name.md)로 변환. Partial year, bonus, tax refunds, 월세공제 등 edge cases 처리. PDF to Markdown 변환 요청 시 사용.
version: 1.0.0
---

# Withholding Tax Receipt Converter
Korean withholding tax receipt PDFs (원천징수영수증)를 structured Markdown으로 변환

## 1. 입출력 형식
Input: `YYYY_원천징수 영수증.pdf` (예: `2024_원천징수 영수증.pdf`)
Output: `withholdingtaxreceipt_YYYY_<name>.md` (예: `withholdingtaxreceipt_2024_홍길동.md`)

## 2. Reference Examples

처리 전 `examples/` 디렉토리의 예시 파일 쌍을 읽어볼 것:
- `examples/pdfs/` - 3개 원본 PDF (2022, 2023, 2024)
- `examples/markdowns/` - 3개 예상 출력

유사한 예시 선택:
- Partial year + tax refund: `2022_원천징수_영수증.pdf` → `withholdingtaxreceipt_2022_홍길동.md`
- Full year, no bonus: `2023_원천징수_영수증.pdf` → `withholdingtaxreceipt_2023_홍길동.md`
- Full year + 월세공제: `2024_원천징수_영수증.pdf` → `withholdingtaxreceipt_2024_홍길동.md`

## 3. Processing Steps

### 3-1. Read Reference Example
`examples/pdfs/`와 `examples/markdowns/`에서 유사한 예시를 읽어 변환 패턴 이해

### 3-2. Read User's PDF
제공된 PDF 경로에서 내용 추출. PDF는 내용에 따라 1, 2, 3 또는 여러 페이지 가능

### 3-3. Extract Information
예시 markdown에 표시된 대로 모든 섹션 정확히 추출:
- 근무기간, 영수증 지급 날짜
- 근무처소득명세 (급여, 상여, 계)
- 비과세 및 감면소득명세
- 세액명세 (결정세액, 기납부세액, 차감징수세액)
- 보험료 (국민건강보험료, 고용보험료, 장기요양보험료, 국민연금보험료)
- 정산명세 (comprehensive breakdown)
- 공제항목
- 연금계좌세액공제
- 월세액 세액공제 명세 (if present in PDF)

### 3-4. Generate Markdown
- Filename: PDF 파일명에서 YYYY와 이름 추출 → `withholdingtaxreceipt_YYYY_<name>.md`로 변환
- Format: `examples/markdowns/`와 정확히 일치 - 한글 필드명만 사용
- Numbers: 콤마로 포맷 (48,527,624)
- Negative values: 음수 기호 유지 (-806,360)
- Zero values: `0`으로 표시

### 3-5. Save Output
사용자 지정 경로에 저장 (기본값: 입력 PDF와 동일한 디렉토리)

## 4. Critical Rules

1. 한글 필드명만 사용 - 영어로 번역하거나 생성 금지
2. 음수 값 보존 (예: 차감징수세액의 세금 환급 -806,360)
3. 콤마로 숫자 포맷 (예: 48,527,624 not 48527624)
4. 0은 `0`으로 표시 (blank 또는 dash 아님)
5. 예시 포맷과 정확히 일치 - `examples/markdowns/` 파일 참조
6. 모든 섹션 포함 - PDF에서 일부 필드가 0이거나 누락되어도

## 5. Edge Cases

모든 edge cases는 `examples/` 디렉토리에 예시 있음:
- Partial year employment (2022: May-December only)
- No bonus payments (2023)
- Bonus payments (2022, 2024)
- Tax refunds (차감징수세액 can be negative)
- 월세액 세액공제 (2024 only - not all years have this)

## 6. Error Handling

PDF를 읽거나 파싱할 수 없는 경우:
- 구체적인 문제를 사용자에게 알림
- 불완전한 출력 생성 금지
- 파일 경로/형식 확인 제안
