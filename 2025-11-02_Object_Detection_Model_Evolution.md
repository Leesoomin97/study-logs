# Object Detection의 발전 과정과 주요 모델 비교

## 1. 머리말

이전 글에서는 Object Detection의 기본 개념과 동작 원리에 대해 알아보았다. 이때 탐지는 단순히 무엇을 분류하는 것을 의미할 뿐만 아니라, 어디에 있는지를 함께 학습해야 하는 문제였다.

이번 글에서는 이러한 탐지 모델이 어떻게 발전해 왔는지, 그리고 각 세대의 모델이 어떤 한계를 해결하며 정확도, 속도, 효율성의 균형을 찾아왔는지를 기술적으로 분석한다.

---

## 2. R-CNN 계열(Two-Stage 구조의 발전)

Object Detection의 시작은 CNN을 직접 탐지에 적용한 R-CNN 계열이다. 이 계열은 객체 후보를 먼저 찾고(Region Proposal) → CNN으로 분류한다는 Two-Stage Detection 구조를 기반으로 한다.

### (1) R-CNN (2014)

- **문제:** 당시 CNN은 이미지 분류에만 사용되었고, 탐지에는 영역 제안(Selective Search)을 통해 약 2000개의 후보를 생성해야 했다. 각 후보 영역은 CNN을 개별로 수행했기 때문에 속도가 매우 느렸다.
- **구조적 개선:** 각 후보(Region Proposal)을 CNN에 개별 입력 → FC Layer에서 클래스 분류 SVM 기반의 후처리를 추가하여 분류 결과를 보정하였다.
- **한계:** 중복 연산이 과도하며, 학습과 추론 속도가 느려 실시간 응용이 불가능하였다.
- **활용:** 연구 목적에 중심적으로 사용되며, 실시간 응용에는 부적합하다.

### (2) Fast R-CNN (2015)

- **문제:** R-CNN은 모든 Region마다 CNN 연산을 수행해야 하므로 GPU 자원 낭비가 심했다.
- **구조적 개선:** Feature Map을 한 번만 계산하고, ROI Pooling을 통해 각 Region Proposal의 크기를 동일하게 정규화하여 FC Layer로 전달하였다.
- **효과:** CNN 연산을 공통화함으로써 연산량이 크게 감소하였고, 이에 따라 학습 효율이 향상되었다.
- **한계:** 여전히 Region Proposal은 외부 알고리즘(Selective Search)에 의존하여 병목 현상이 존재한다.

### (3) Faster R-CNN (2015)

- **문제:** 외부에서 후보 영역을 생성하는 과정이 전체 속도의 한계점에 도달했다.
- **구조적 개선:** RPN(Region Proposal Network)을 도입하여 CNN 내부에서 Region Proposal을 자동으로 생성한다. 이는 완전한 End-to-End 학습 구조로 발전했다고 할 수 있다.
- **효과:** 탐지 속도가 향상되며, Region Proposal 품질 역시 향상되고, Two-Stage Detection의 표준 구조가 확립되었다.
- **한계:** 여전히 실시간 추론에는 부적합하며, 고해상도 이미지에서 속도 저하가 발생한다.

---

## 3. One-Stage 계열(속도 중심의 발전)

R-CNN 계열은 높은 정확도를 달성했지만, 두 단계의 구조적 복잡성 때문에 속도 측면에서 실시간 응용이 어려웠다.

이를 해결하기 위해 만들어진 것이 한 번의 예측(One-Shot Prediction)으로 전체 이미지를 처리하는 One-Stage Detector이다.

### (1) YOLO (You Only Look Once, 2016)

- **개념:** 이미지를 SxS 격자로 분할하고, 각 셀(Cell)에서 객체 존재 확률과 Bounding Box를 동시에 예측한다.
- **구조적 개선:** 단일 CNN이 Classification과 Regression을 동시에 수행하여 완전한 End-to-End 단일 구조가 되었다.
- **효과:** 추론 속도가 획기적으로 향상되었으며, 실시간 영상 탐지가 가능해졌다.
- **한계:** 작은 객체나 복잡한 장면에서 정확도가 저하되며, 그리드 단위 탐지의 해상도 한계를 가지고 있다.
- **활용 예시:** 자율주행, 드론 영상, CCTV 실시간 감지

### (2) SSD (Single Shot MultiBox Detector, 2016)

- **문제:** YOLO는 단일 Feature Map 기반이라 크기가 다양한 객체에 취약하다는 단점이 있다. 이러한 단점을 보완하기 위해 나온 것이 SSD이다.
- **구조적 개선:** 여러 해상도의 Feature Map에서 동시에 탐지를 수행한다. 즉, 다중 스케일 예측(Multi-scale prediction) 구조를 도입한 것이다.
- **효과:** 작은 객체 인식률이 향상되었으며, 속도와 정확도 간의 균형을 확보했다.
- **활용 예시:** 모바일 환경, 실시간 비전 시스템

---

## 4. 후속 모델 및 효율화 추세

### (1) YOLO 시리즈 (v3~v8)

- Backbone 개선: Darknet → CSPNet, ConvNeXt 등  
- Feature Fusion: PAN-FPN 구조로 다층 Feature 결합  
- Anchor-free 구조로 전환, Generalization 향상

### (2) EfficientDet (2019)

- **개선:** EfficientNet의 Compound Scaling을 적용  
- **BiFPN 구조:** Feature Pyramid 간의 연결을 최적화  
- **효과:** 적은 연산량으로 높은 정확도, 효율성 중심의 탐지 구조 완성

---

## 5. 종합 비교

| 모델 | 주요 개선점 | 구조 형태 | 장점 | 한계 | 대표 응용 |
|------|--------------|------------|--------|--------|-------------|
| **R-CNN** | Region 별 CNN 추출 | Two-Stage | 높은 정확도 | 매우 느림 | 초기 연구 |
| **Fast R-CNN** | ROI Pooling | Two-Stage | 속도 개선 | 외부 Region 사용 | 연구, 검증 |
| **Faster R-CNN** | RPN 내장 | Two-Stage | 정확도 향상 | 실시간 불가 | 정밀 탐지 |
| **YOLO** | End-to-End 단일 예측 | One-Stage | 매우 빠름 | 작은 객체 약함 | 실시간 영상 |
| **SSD** | 다중 Feature Map | One-Stage | 속도/정확도 균형 | 작은 개체 한계 | 모바일 탐지 |
| **EfficientDet** | BiFPN, Compound Scaling | One-Stage | 효율성 최고 | 구조 복잡 | 대규모 비전 시스템 |

---

## 6. 마무리

Object Detection의 발전은 단순히 정확도를 높이는 경쟁이 아니라, 정확도, 속도, 효율성의 균형점을 찾아가는 기술적 진화였다.

- **R-CNN → Faster R-CNN:** 정밀 탐지 중심(정확도 중시)  
- **YOLO → SSD:** 실시간 처리 중심(속도 중시)  
- **EfficientDet:** 효율성 중심(모바일, 클라우드 환경 적합)

이러한 발전의 흐름은 오늘날의 Transformer 기반 Vision 모델(ViT, DETR, YOLOv8)의 설계 철학에도 직접적인 영향을 주어, 최근 AI 기술발전에 크게 기여하였다. 이에 우리는 발전의 방향을 살펴 앞으로 어떠한 발전이 추가로 이루어져야 할지 생각하고 도전하여야 할 것이다.

