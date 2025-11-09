# Detector 내부 구조 분석: Anchor, FPN, NMS의 최적화 과정  

---

## 1. 머리말  

이전 글에서는 Object Detection 모델의 발전 과정을 살펴보았다.  
R-CNN에서 YOLO, SSD, EfficientDet로 이어지는 흐름은  
정확도, 속도, 효율성의 균형을 찾아온 기술적 진화였다.  

하지만 탐지기의 성능을 결정짓는 근본적인 요인은  
모델 이름이 아니라 **탐지기 내부의 구조적 설계(Architecture)** 이다.  

탐지기는 보통 다음 세 부분으로 구성된다.  

1️⃣ **Feature 추출 및 결합부 (FPN, PAN, BiFPN 등)**  
2️⃣ **탐지 헤드 (Anchor-Based → Anchor-Free로 발전)**  
3️⃣ **후처리부 (NMS, Soft-NMS, NMS-Free)**  

이번 글에서는 이 세 가지 핵심 구조의 기술적 역할과  
그 발전 과정을 단계별로 분석한다.  

---

## 2. Feature 추출 및 결합부 – FPN 계열 구조  

탐지는 다양한 크기의 객체를 다뤄야 하므로,  
단일 해상도의 Feature Map만으로는 작은 객체를 인식하기 어렵다.  
이 문제를 해결하기 위해 도입된 구조가 **Feature Pyramid Network (FPN)** 이다.  

### (1) FPN의 개념  
- CNN의 하위 계층(고해상도, 저의미)과 상위 계층(저해상도, 고의미)을 결합  
- Top-down + Lateral Connection 구조로 피처 통합  
- 다양한 스케일의 객체를 동시에 탐지 가능  

### (2) 효과  
- 작은 객체 인식률 향상  
- 피처 간 정보 손실 감소  
- 다중 해상도 학습으로 안정적 성능 확보  

### (3) 발전형 구조  
| 구조 | 주요 특징 | 적용 모델 |
|------|-------------|------------|
| **PANet (2018)** | Bottom-up Path 추가 → 양방향 피처 흐름 | Mask R-CNN, YOLOv4 |
| **BiFPN (2019)** | Feature 중요도 가중치 학습 → 연결 효율 최적화 | EfficientDet |
| **FPNv2 / HRFPN** | 해상도 간 균형 유지 및 고해상도 정보 보존 | 최신 Segmentation·Detection 모델 |

---

## 3. 탐지 헤드 – Anchor 기반에서 Anchor-Free로  

탐지기의 핵심은 **Bounding Box와 클래스(Class)** 를 예측하는 “탐지 헤드(Detection Head)”이다.  
이 구조는 크게 두 세대로 구분된다.  

### (1) Anchor-Based 구조  

초기 탐지기(Faster R-CNN, SSD, RetinaNet)는  
**Anchor Box** 라는 사전 정의된 후보 영역을 사용했다.  

- 각 Feature Map 위치마다 여러 비율·크기의 Anchor를 배치  
- 모델은 각 Anchor가 객체일 확률과 그 위치 보정을 예측  
- 다양한 비율의 객체를 안정적으로 처리 가능  

하지만 이 방식은 연산량과 튜닝 비용이 크고,  
대부분의 Anchor가 실제 객체가 아닌 “배경”이기 때문에  
학습 효율이 떨어진다는 단점이 있었다.  

### (2) Anchor-Free 구조  

이 한계를 해결하기 위해 등장한 것이 **Anchor-Free Detector** 이다.  

- Anchor를 사전 정의하지 않고, Feature Map의 각 픽셀이  
  **객체의 중심점(center)** 혹은 **keypoint** 를 직접 예측  
- Bounding Box 좌표 (x, y, w, h)를 회귀로 학습  
- 대표 모델: **FCOS, CenterNet, YOLOv8, DETR**  

#### 장점  
- Anchor 튜닝 불필요 → 구조 단순화  
- Negative Sample 불균형 완화  
- 계산 효율성 향상  

#### 단점  
- Anchor의 초기 정보가 없으므로 작은 객체 탐지가 어려움  
- Bounding Box 조정 정밀도는 여전히 보조 구조(FPN 등)에 의존  

### (3) 발전 흐름 요약  

| 세대 | 대표 모델 | 특징 |
|------|-------------|------|
| **Anchor-Based** | Faster R-CNN, SSD, RetinaNet | 고정된 Anchor로 탐지 안정성 확보 |
| **Anchor-Free** | FCOS, CenterNet, YOLOv8 | Anchor 제거, 중심점 기반 회귀 |
| **NMS-Free (End-to-End)** | DETR, RT-DETR | Anchor와 NMS 모두 제거, Transformer 구조 |

즉, Anchor-Free는 Anchor 구조의 **대체·진화형**이며,  
탐지 헤드의 설계 복잡도를 줄이는 방향으로 발전해왔다.  

---

## 4. 후처리부 – NMS의 개선과 제거  

탐지기는 종종 하나의 객체에 대해 여러 박스를 동시에 예측한다.  
이 중 가장 신뢰도 높은 박스만 남기는 과정이 **NMS (Non-Maximum Suppression)** 이다.  

### (1) 기본 원리  
1️⃣ Confidence Score로 박스 정렬  
2️⃣ 가장 높은 점수를 가진 박스를 기준으로  
   IoU(Intersection over Union)가 일정 임계값 이상인 박스를 제거  

### (2) 문제점  
- IoU 기준이 고정되어 객체 밀집 이미지에서 False Suppression 발생  
- 크기나 배경 복잡도에 따른 동적 대응이 불가능  

### (3) 개선 및 대체 기법  

| 방식 | 주요 특징 | 적용 모델 |
|------|------------|------------|
| **Soft-NMS** | IoU가 높을수록 Confidence를 연속적으로 감소 | RetinaNet |
| **Adaptive NMS** | 객체 크기·밀도에 따라 임계값 조정 | Cascade R-CNN |
| **Weighted NMS** | 다수의 박스를 가중 평균으로 병합 | EfficientDet |
| **NMS-Free** | Transformer 기반 End-to-End 예측 | DETR, RT-DETR |

---

## 5. Detector의 구조 통합  

최근 탐지기는 이전 세대의 개별 요소(FPN, Anchor, NMS)를 단순히 채택하는 수준을 넘어,  
**세 구조를 통합적으로 설계하여 정확도–속도–효율성의 균형**을 찾는 방식으로 진화하고 있다.  

### (1) 모듈 통합의 의의  
과거에는 탐지기 내부 구성요소가 독립적으로 존재했다.  
예를 들어 R-CNN 계열에서는  
- Feature 추출부 → FPN 없음(단일 피처맵)  
- 탐지 헤드 → Anchor 기반 Region Proposal  
- 후처리 → 기본 NMS  

이렇게 별도로 작동했다.  
하지만 효율성 요구가 높아지면서 **탐지 파이프라인을 엔드투엔드로 연결하고, 모듈 간 중복을 줄이는** 방향으로 변했다.  

### (2) 통합 전략  
- **Feature Fusion + Detection Head 결합:** BiFPN 등은 피처맵 결합 과정에서 탐지 헤드가 필요로 하는 정보(해상도, 의미 깊이)를 직접 반영한다.  
- **Anchor-Free + FPN 조합:** Anchor 없이도 FPN의 다중 스케일 피처를 활용해 다양한 크기의 객체를 탐지.  
- **NMS-Free + Transformer 결합:** DETR 계열은 피처 결합과 탐지 출력을 Transformer Attention으로 통합해 후처리를 완전히 제거했다.  

### (3) 통합 사례 비교  

| 구성 요소 | 적용 구조 | 대표 모델 | 통합 효과 |
|------------|------------|------------|------------|
| Feature 결합부 | BiFPN / PAN / FPNv2 | EfficientDet, YOLOv5 | 다중 스케일 정보 효율 통합 → 작고 큰 객체 모두 정확도 향상 |
| 탐지 헤드 | Anchor-Free | YOLOv8, FCOS | Anchor 튜닝 제거 → 구조 단순화, 추론 속도 상승 |
| 후처리 | NMS-Free (Transformer) | DETR, RT-DETR | End-to-End 학습 → 후처리 제거, 연산 효율 향상 |

---

## 6. 마무리  

Detector의 내부 구조는 단순히 “박스를 그리는 과정”이 아니라,  
탐지기의 정확도와 효율성을 결정짓는 핵심 엔진이다.  

현대 탐지기는 단일 모듈의 성능 개선이 아니라,  
**“모듈 간 정보 흐름을 최적화한 통합형 탐지기(Integrated Detector)”** 로 발전했다.  
이로써 각 요소가 서로 보완하며 다음과 같은 결과를 얻는다.  

- Feature 결합으로 작은 객체 탐지 성능 상승  
- Anchor-Free 탐지 헤드로 추론 속도 향상  
- NMS-Free 후처리로 완전한 End-to-End 학습 가능  

탐지기의 발전은 결국 세 가지 방향으로 수렴하고 있다.  

1️⃣ **탐지 헤드 단순화:** Anchor-Free 및 NMS-Free 구조  
2️⃣ **Feature 결합 효율화:** BiFPN 등 가중치 기반 피처 융합  
3️⃣ **End-to-End 학습:** 후처리 제거 및 Transformer 기반 설계  

이러한 변화는 YOLOv8, EfficientDet, DETR로 대표되는  
**“단순하지만 강력한 구조(Simple but Powerful)”** 로 이어지고 있다.  

---

