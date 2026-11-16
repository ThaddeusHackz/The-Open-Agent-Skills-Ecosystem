---
name: payslip-converter
description: Korean payslip PDF (급상여명세서_YYYYMM_name.pdf)를 Markdown (payslip_YYYY-MM_name.md)로 변환. Zero hours, 상여, 연장근무, 세금 환급, negative deductions 등 edge cases 처리. PDF to Markdown 변환 요청 시 사용.
version: 1.0.0
---

# Payslip Converter
Korean payslip PDFs (급상여명세서)를 structured Markdown으로 변환

## 1. 입출력 형식
Input: `급상여명세서_YYYYMM_<name>.pdf` (예: `급상여명세서_202504_홍길동.pdf`)
Output: `payslip_YYYY-MM_<name>.md` (예: `payslip_2025-04_홍길동.md`)

## 2. Reference Examples

처리 전 `examples/` 디렉토리의 예시 파일 쌍을 읽어볼 것:
- `examples/pdfs/` - 9개 원본 PDF
- `examples/markdowns/` - 9개 예상 출력

유사한 예시 선택:
- Standard: `급상여명세서_202505_홍길동.pdf` → `payslip_2025-05_홍길동.md`
- Zero hours: `급상여명세서_202301_홍길동.pdf` → `payslip_2023-01_홍길동.md`
- Partial hours: `급상여명세서_202501_홍길동.pdf` → `payslip_2025-01_홍길동.md`
- Large bonus: `급상여명세서_202405_홍길동.pdf` → `payslip_2024-05_홍길동.md`
- Overtime + refund: `급상여명세서_202502_홍길동.pdf` → `payslip_2025-02_홍길동.md`
- Max tax refund: `급상여명세서_202302_홍길동.pdf` → `payslip_2023-02_홍길동.md`
- High allowance: `급상여명세서_202412_홍길동.pdf` → `payslip_2024-12_홍길동.md`
- Negative insurance: `급상여명세서_202211_홍길동.pdf` → `payslip_2022-11_홍길동.md`
- Data anomaly: `급상여명세서_202210_홍길동.pdf` → `payslip_2022-10_홍길동.md`

## 3. Processing Steps

### 3-1. Read Reference Example
`examples/pdfs/`와 `examples/markdowns/`에서 유사한 예시를 읽어 변환 패턴 이해

### 3-2. Read User's PDF
제공된 PDF 경로에서 내용 추출

### 3-3. Extract Information
Page 1: 급여지급일, 근로시간 (소정/야간/연장/휴일), 지급내역 (기본급, 식대, 차량유지비, 육아수당, 연구수당, 기타비과세수당, 상여, 연장수당, 야간수당, 휴일수당, 기타과세수당, 지급액 계)

Page 2: 공제내역 (국민연금, 건강보험, 고용보험, 장기요양보험료, 기타공제액, 소득세, 지방소득세, 연말정산 소득세, 연말정산 지방세, 공제액 계), 실지급액

### 3-4. Generate Markdown
- Filename: PDF 파일명에서 YYYYMM과 이름 추출 → `payslip_YYYY-MM_<name>.md`로 변환
- Format: `examples/markdowns/`와 정확히 일치
- Numbers: 콤마로 포맷 (3,500,000)
- Negative values: 음수 기호 유지 (-806,360)
- Zero values: `0`으로 표시

### 3-5. Save Output
사용자 지정 경로에 저장 (기본값: 입력 PDF와 동일한 디렉토리)

## 4. Critical Rules

1. 음수 값 보존 (예: 세금 환급 -806,360, 보험료 조정 -4,390)
2. 콤마로 숫자 포맷 (예: 3,500,000 not 3500000)
3. 0은 `0`으로 표시 (blank 아님)
4. 예시 포맷과 정확히 일치 - `examples/markdowns/` 파일 참조
5. PDF 파일명의 모든 직원 이름에서 작동

## 5. Edge Cases

모든 edge cases는 `examples/` 디렉토리에 예시 있음:
- Zero working hours (0시간 / 0일)
- Partial working hours (80시간 / 15일)
- Large bonuses (5.4M+)
- Overtime pay with tax refunds
- Negative deductions (insurance adjustments, tax refunds)
- Data anomalies (hours without days)

## 6. Error Handling

PDF를 읽거나 파싱할 수 없는 경우:
- 구체적인 문제를 사용자에게 알림
- 불완전한 출력 생성 금지
- 파일 경로/형식 확인 제안
