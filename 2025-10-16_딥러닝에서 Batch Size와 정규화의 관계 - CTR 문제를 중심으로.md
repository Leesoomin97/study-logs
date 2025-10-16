# 🧠 딥러닝에서 Batch Size와 정규화의 관계  
### CTR(Click-Through Rate) 문제를 중심으로

딥러닝 모델을 학습할 때 우리는 수많은 하이퍼파라미터를 조정한다.  
그중에서도 **batch size(배치 크기)** 와 **정규화(normalization)** 는 학습 안정성과 성능을 결정짓는 핵심 축이다.  
이번 글에서는 특히 **클릭률 예측(CTR)** 과 같이 **극단적인 불균형 + 대규모 데이터 환경**에서  
이 두 요소가 어떤 의미를 가지는지 정리해 본다.

---

## 1. Batch Size란 무엇인가

### (1) 정의
Batch size는 한 번의 forward/backward 연산에서 처리하는 샘플 개수를 뜻한다.  
너무 작거나 너무 크면 학습이 불안정해지거나 느려질 수 있다.

### (2) 작을 때 (예: 32~128)
- gradient의 noise가 크다 → 학습이 불안정하지만 일반화에 도움  
- GPU 메모리 사용량이 적다  
- 클래스 불균형 데이터(CTR 등)에서 양성 샘플이 자주 등장할 확률이 높음

### (3) 클 때 (예: 1024~4096)
- gradient가 안정적이고 loss 곡선이 매끄럽다  
- 연산 효율이 좋지만 클릭(양성)이 거의 포함되지 않을 수 있다  
- 지나치게 큰 배치는 underfitting을 유발하기도 한다

### (4) 결론
CTR 데이터처럼 양성 비율이 1~2% 이하인 경우,  
너무 큰 배치는 오히려 학습 신호를 희석시키는 결과를 낳을 수 있다.  

> 따라서 CTR 문제에서는 보통 **batch_size = 256~512** 정도가 가장 안정적이다.  
> 큰 데이터셋이더라도 "희소한 신호를 자주 관찰할 수 있는 크기"가 중요하다.

---

## 2. 정규화(Normalization)의 필요성

딥러닝의 깊은 구조는 내부 공변량 변화(Internal Covariate Shift) 문제를 일으킨다.  
각 층의 입력 분포가 계속 달라지면 학습이 느려지고, 수렴이 불안정해진다.  

이를 완화하기 위해 다양한 정규화 기법이 등장했다.  
대표적으로는 Batch Normalization, Layer Normalization, Instance Normalization, Group Normalization이 있다.

---

## 3. 주요 정규화 기법 비교

| 구분 | 정규화 기준 | 배치 의존성 | 대표 사용 모델 | 특징 |
|------|--------------|--------------|----------------|------|
| **BatchNorm** | 배치 내 동일 채널 | O | CNN | 학습 빠름, large batch 필요 |
| **LayerNorm** | 한 샘플 내 전체 뉴런 | X | Transformer, RNN | 배치 크기 무관, 안정적 |
| **InstanceNorm** | 한 샘플의 한 채널 | X | Style Transfer | 스타일 일관성, 생성 모델용 |
| **GroupNorm** | 한 샘플 내 채널 그룹 | X | CNN(소배치) | BatchNorm 대체, 작은 배치에서도 안정 |

---

## 4. CTR 모델에서 BatchNorm이 어려운 이유

CTR 데이터는 일반적으로 tabular 구조 + embedding + MLP 형태를 가진다.  
즉, 이미지처럼 spatial correlation이 명확하지 않다.

이런 구조에서는 BatchNorm이 다음과 같은 한계를 가진다.

- Batch 통계량이 불안정 → 클릭(1)이 거의 없으면 배치마다 분포가 달라진다.  
- Batch 크기 의존성 높음 → 작은 배치에서는 mean/var 추정이 왜곡된다.  
- 특징 스케일 차이 큼 → categorical embedding과 numeric feature가 섞여 있어서 채널 정규화가 어렵다.

그래서 CTR용 딥러닝 모델(DCN, DeepFM, Wide&Deep 등)에서는  
보통 LayerNorm이나 InstanceNorm을 선호한다.  

> 특히 Transformer 기반 CTR 모델(DSTN, AutoInt)은 거의 항상 LayerNorm을 사용한다.

---

## 5. Layer Normalization의 장점

LayerNorm은 한 샘플 내부의 모든 뉴런을 기준으로 정규화하기 때문에  
- 배치 크기와 무관하게 작동하고,  
- 극단적인 분포(클릭률 낮음)에서도 안정적인 학습이 가능하다.  

또한 inference 시에도 별도의 moving average 통계가 필요 없어서  
배포와 재현성 측면에서도 안정적이다.

---

## 6. 실무에서의 조합 전략

| 모델 구조 | Batch Size | 정규화 기법 | 이유 |
|------------|-------------|--------------|------|
| CNN 이미지 기반 CTR (예: 광고 이미지 포함) | 512~1024 | BatchNorm | 시각 피처 안정화 |
| Dense Feature 기반 CTR (Toss, Criteo 등) | 256~512 | LayerNorm | tabular + embedding 구조 |
| Transformer 기반 CTR (AutoInt, DeepCTR) | 128~512 | LayerNorm | self-attention 안정화 |
| GAN / Style Transfer형 광고 생성 | 64~128 | InstanceNorm | 스타일 표현 일관성 |

---

## 7. 마무리

CTR 데이터에서는  
> "Batch는 너무 크면 신호를 잃고, 너무 작으면 불안정하다."  
> "정규화는 BatchNorm보다 LayerNorm이 현실적이다."

딥러닝은 결국 데이터의 분포와 구조에 맞춰 세밀하게 조정되어야 한다.  

CTR처럼 대용량이면서 불균형한 데이터에서는  
- batch_size = 256~512  
- 정규화 = LayerNorm 중심  
- pos_weight나 focal loss로 보조  

이 조합이 가장 실무적이고 안정적이다.

---

