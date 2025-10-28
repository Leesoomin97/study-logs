# 🧠 Convolutional Neural Network (CNN) 기본 개념 정리

---

## 1️⃣ 머리말 — Edge Detection에서 CNN으로

이전 글에서는 **Edge Detection**과 **Contour Detection**을 통해  
이미지 내의 윤곽선, 경계선, 형태 정보를 사람이 직접 추출하는 방식을 살펴보았다.  

이 방식은 이미지의 특징을 수동적으로 정의해야 하기 때문에,  
환경 변화(밝기, 회전, 노이즈)에 매우 취약하고 대규모 데이터에 확장하기 어렵다.  

이 한계를 극복하기 위해 등장한 것이 **Convolutional Neural Network (CNN)** 이다.  
CNN은 입력 이미지로부터 **유용한 특징(feature)** 을 **자동으로 학습**하는 신경망 구조이며,  
이 과정에서 **필터(커널)** 의 값이 **데이터 기반으로 학습**된다는 점이 핵심이다.  

즉, CNN은 사람이 설계한 Sobel, Canny 필터 대신  
**손실함수와 역전파(backpropagation)** 를 통해 스스로 최적의 필터를 학습한다.

---

## 2️⃣ 대표 CNN 모델 발전사

CNN의 기본 구조는  
**합성곱(Convolution) → 활성화(ReLU) → 풀링(Pooling) → 완전연결층(FC)** 으로 구성된다.  
이 틀을 기반으로 다양한 모델이 등장해 성능과 효율성을 높였다.  

| 모델명 | 핵심 특징 | 발표년도 |
|--------|------------|-----------|
| **LeNet-5** | 최초의 CNN, 손글씨 숫자 인식(MNIST) | 1998 |
| **AlexNet** | GPU 학습, ReLU·Dropout 도입, ImageNet 우승 | 2012 |
| **VGGNet** | 3×3 필터만 사용해 깊이를 확장한 단순 구조 | 2014 |
| **GoogLeNet (Inception)** | 다양한 필터 크기를 병렬로 결합한 효율적 구조 | 2014 |
| **ResNet** | Residual Block으로 gradient 소실 문제 해결 | 2015 |
| **DenseNet** | 층 간 직접 연결로 feature 재사용 극대화 | 2017 |
| **EfficientNet** | 깊이·너비·해상도를 균형적으로 확장 (Compound Scaling) | 2019 |

---

## 3️⃣ CNN의 학습 과정

CNN의 학습은 크게 세 단계로 이루어진다.  
보통 “순전파와 역전파”로 요약되지만, 실제로는 **손실 계산(loss computation)** 이  
두 단계를 연결하는 핵심 중간 과정이다.  

> **입력 → 순전파(Forward) → 손실 계산(Loss) → 역전파(Backward)**

---

### (1) 순전파 (Forward Propagation)
- 입력 이미지를 여러 합성곱층과 풀링층을 거쳐  
  **저수준 특징 → 고수준 특징**으로 변환한다.  
- 합성곱 연산 결과는 활성화 함수(ReLU)를 통해 비선형성을 갖는다.  
- 완전연결층(FC Layer)에서 softmax를 적용해 각 클래스 확률을 산출한다.  

**예시:**  
입력 224×224×3 → Conv(3×3, stride=1, padding=1, filters=64) → 출력 224×224×64  

---

### (2) 손실 계산 (Loss Computation)
- 예측값과 실제 정답 간의 차이를 손실함수(loss function)로 계산한다.  
- 분류 문제에서는 **Cross Entropy Loss**,  
  회귀 문제에서는 **MSE(Mean Squared Error)** 를 주로 사용한다.  
- 손실값은 모델의 예측이 얼마나 정확한지를 수치로 표현하며,  
  역전파의 기울기 계산 기준이 된다.  

---

### (3) 역전파 (Backward Propagation)
- 손실값을 기준으로 각 가중치의 기울기(gradient)를 계산하고,  
  옵티마이저(SGD, Adam 등)를 이용해 파라미터를 갱신한다.  
- 연쇄법칙(chain rule)을 따라 출력층 → 입력층 순으로 기울기가 전파된다.  
- 이 과정을 반복하면서 커널은 점점 유용한 시각적 패턴을 학습하게 된다.

---

## 4️⃣ CNN의 학습 특성

| 특성 | 설명 |
|------|------|
| **지역 연결(Local Connectivity)** | 각 뉴런은 전체 입력이 아닌 인접 영역(receptive field)에만 연결됨 |
| **가중치 공유(Weight Sharing)** | 동일한 커널이 전체 이미지에 반복 적용되어 파라미터 수 감소 |
| **계층적 표현(Hierarchical Representation)** | 초기층은 edge, 중간층은 texture, 상위층은 object 형태를 학습 |
| **Translation Invariance** | 동일한 객체가 위치만 달라도 동일하게 인식 가능 |
| **Parameter Efficiency** | 완전연결 신경망(MLP)에 비해 훨씬 적은 파라미터로 높은 표현력 확보 |

이러한 구조적 특성 덕분에 CNN은  
이미지, 음성, 영상 등 **공간적 구조를 가진 데이터**에 특히 적합하다.

---

## 5️⃣ CNN의 주요 구성 요소

CNN의 성능과 일반화 능력은 각 구성 요소의 역할에 의해 결정된다.  

### (1) Convolution Layer
- 입력의 지역 영역(local region)에 커널(kernel)을 적용해 feature map을 생성한다.  
- 커널 크기(K), 패딩(P), 스트라이드(S)에 따라 출력 크기가 결정된다.  
  ```
  Output size = (H - K + 2P) / S + 1
  ```
- 학습을 통해 커널이 특정 방향성·질감·형태에 반응하게 된다.  

**예시:**  
입력 32×32, 커널 3×3, 패딩 1, 스트라이드 1 → 출력 32×32 유지  

---

### (2) Activation Function
- 합성곱 결과에 비선형성을 부여해 복잡한 패턴 학습을 가능하게 한다.  
- 대표적으로 **ReLU (Rectified Linear Unit)** 사용.  
  ```
  f(x) = max(0, x)
  ```
- gradient 소실 문제를 완화하고 계산 효율이 높다.  

---

### (3) Pooling Layer
- feature map의 공간 크기를 줄여 연산량을 감소시키고 과적합을 방지한다.  
- 대표 방식:  
  - **Max Pooling:** 영역 내 최댓값  
  - **Average Pooling:** 영역 내 평균값  
- 위치 변화에 대한 불변성을 확보한다.  

**예시:** 4×4 입력 → 2×2 Max Pooling → 2×2 출력  

---

### (4) Fully Connected Layer
- Flatten을 통해 feature map을 1차원 벡터로 변환하고  
  이를 입력으로 받아 최종 분류(Classification)를 수행한다.  
- softmax를 사용해 클래스별 확률 분포를 산출한다.  

---

## 마무리

| 구분 | 내용 요약 |
|------|------------|
| **핵심 개념** | CNN은 합성곱 연산을 통해 입력 데이터의 지역적 특징을 자동 학습하는 신경망 구조 |
| **학습 단계** | 순전파 → 손실 계산 → 역전파 |
| **학습 특성** | 지역성, 가중치 공유, 계층적 표현, 위치 불변성 |
| **구성 요소** | Convolution, ReLU, Pooling, Fully Connected |
| **대표 모델** | AlexNet, VGG, ResNet, EfficientNet |

---

## 🔜 다음 글 예고

이번 글에서는 CNN의 기본적인 구조와 그 특성에 대해 알아보았다. 다음 글에서는  
**AlexNet → VGG → ResNet → EfficientNet** 으로 이어지는  
CNN 구조의 발전 과정을 다루며,  
각 모델이 해결하고자 한 문제(깊이, 효율성, gradient 소실 등)를  
구체적으로 분석할 예정이다.
