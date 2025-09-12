# 머신러닝 프로젝트 Validation 기법 정리

## 머리말
2주동안 머신러닝 프로젝트를 진행했다. 성적은 3등.  
오늘 1등한 팀의 방법을 들으며 마무리를 하면서 우리 조가 조금 더 높은 등수를 받지 못한 건 feature에 대한 조사가 부족한 게 아니었을까 하는 생각이 들었다.  
그래서 추가적으로 프로젝트의 목표에 영향력 있는 feature를 고르는 방법을 찾아보다가 validation 기법을 조사하게 되었다.

---

## 본문

| 구분 | 기법 이름 | 목적 | 장점 | 단점 | 자주 쓰이는 상황 |
|------|-------------|------|------|------|------------------|
| 일반 Validation | Hold-out (Train/Valid/Test Split) | 단순 분할로 성능 평가 | 빠르고 단순 | 데이터 적으면 불안정 | 데이터 충분할 때 |
| 일반 Validation | K-Fold | 모든 데이터를 골고루 학습/검증 | 안정적 성능 추정 | K배 느림 | 일반적 대회 |
| 일반 Validation | Stratified K-Fold | 클래스 비율 유지 | 불균형 데이터 대응 | K배 느림 | 분류 문제 |
| 일반 Validation | Group K-Fold | 그룹 단위 분리 (ID 단위) | 데이터 누수 방지 | 그룹 불균형 가능 | 사용자/환자 단위 데이터 |
| 일반 Validation | Leave-One-Out (LOOCV) | 데이터 최대 활용 | 데이터 적어도 사용 가능 | 계산량 큼 | 데이터 적은 연구 |
| 일반 Validation | Time Series Split | 시계열 순서 고려 | 미래 예측 반영 | 데이터 활용도 낮음 | 시계열 문제 |
| 일반 Validation | Nested CV | 성능 평가 + 하이퍼파라미터 튜닝 | 편향 없는 평가 | 계산량 매우 큼 | 연구/논문 |
| 일반 Validation | Bootstrap Validation | 성능 분산 추정 | 불확실성 추정 가능 | 중복 샘플 문제 | 데이터 적을 때 |
| 보조적 Validation | Adversarial Validation | Train/Test 분포 차이 탐지 | 모델 기반으로 차이 측정 | 계산량 추가 필요 | Dacon/Kaggle 대회 |
| 보조적 Validation | Target Leakage Detection | Label 누수 여부 탐지 | 성능 왜곡 방지 | 자동화 어려움 | EDA/실무 |
| 보조적 Validation | Covariate Shift Detection | 입력 분포 차이 확인 | 분포 차이 수치화 | 통계량 계산 필요 | Train/Test 분포 검증 |
| 보조적 Validation | Concept Drift Detection | 시간에 따른 타깃/특성 분포 변화 탐지 | 실제 서비스 환경 반영 | 탐지 민감도 조절 어려움 | 시계열, 운영 환경 |
| 보조적 Validation | Permutation Test | Feature 중요도 검정 | 직관적 중요도 확인 | 계산량 많음 | Feature selection |
| 보조적 Validation | KS Test | 두 분포 비교 (통계적 검정) | 간단, 빠름 | 다차원 데이터에는 약함 | Train/Test feature 비교 |
| 보조적 Validation | PSI (Population Stability Index) | 운영 중 분포 안정성 확인 | 간단한 수치화 | 기준값 해석 필요 | 신용평가, 운영 모니터링 |
| 보조적 Validation | Jackknife / Bootstrap | 성능 안정성 추정 | 분산, 불확실성 확인 | 느림 | 모델 신뢰성 검증 |

---

## 마무리
출처는 chat GPT.  
나중에 필요하면 두고두고 와서 봐야지.  
아파트 가격 예측이라는 주제에 맞춰 K-hold 기법과 Time split 기법을 사용했었지만,  
다른 보조적 기법도 함께 사용했더라면 하는 아쉬움이 남는다.
