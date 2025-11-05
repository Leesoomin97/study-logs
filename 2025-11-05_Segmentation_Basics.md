# 🧩 Segmentation의 전반 개념 — Semantic, Instance, Panoptic 비교  

---

## 1. 머리말  

이전 글에서는 Object Detection을 통해 이미지 내 **어디에 어떤 객체가 존재하는가**를 예측하는 과정을 다뤘다.  
하지만 탐지는 객체의 위치를 사각형(Bounding Box)으로 표현하기 때문에,  
**객체의 세부 형태나 정확한 경계 정보는 포함하지 못한다.**

이러한 한계를 해결하기 위해 등장한 기술이 **Segmentation(세분화)** 이다.  
Segmentation은 이미지를 **픽셀 단위로 해석하는 시각적 이해(Visual Understanding)** 기법으로,  
모든 픽셀에 대해 “이 픽셀이 무엇을 의미하는가”를 예측한다.  
즉, 탐지가 ‘어디에 있는가’를 알려준다면, 세분화는 ‘어디까지가 그 객체인가’를 정의하는 문제이다.  

---

## 2. Segmentation의 정의  

Segmentation은 입력 이미지를 구성하는 각 **픽셀(pixel)** 에 대하여  
해당 픽셀이 속한 클래스(Class)를 예측하는 **밀집 예측(Dense Prediction)** 문제이다.  

Detection이 “객체 단위(object-level)” 문제라면,  
Segmentation은 “픽셀 단위(pixel-level)” 문제로 다음과 같이 정의된다:

\[
f: \mathbb{R}^{H \times W \times 3} \rightarrow \mathbb{R}^{H \times W \times C}
\]

여기서  
- \(H, W\) : 이미지의 세로, 가로 해상도  
- \(C\) : 예측할 클래스 개수  
- 출력값은 각 픽셀의 클래스 확률 분포를 나타낸다.  

Segmentation의 목표는 **객체의 형태적 경계를 보존하면서 의미적 분류를 수행하는 것**이다.  
이 때문에 Segmentation 모델은 Detection보다 훨씬 더 세밀한 공간적 표현(spatial precision)을 요구한다.  

---

## 3. Segmentation의 주요 종류  

Segmentation은 **예측 단위(Unit of Prediction)** 와 **모델의 목표(Objective)** 에 따라 다음 세 가지로 구분된다.  

| 구분 | 예측 단위 | 목표 | 출력 형태 | 예시 모델 |
|------|------------|------|------------|------------|
| **Semantic Segmentation** | 픽셀 | 각 픽셀의 의미(Class) 분류 | 동일 클래스는 하나의 영역으로 표현 | FCN, U-Net, DeepLab |
| **Instance Segmentation** | 객체 단위의 픽셀 집합 | 같은 클래스 내 개별 객체 분리 | 객체마다 독립적인 마스크 출력 | Mask R-CNN, YOLACT |
| **Panoptic Segmentation** | 픽셀 + 객체 ID | Semantic + Instance 통합 | 모든 픽셀에 클래스 + 인스턴스 ID 부여 | Panoptic FPN, UPSNet |

- **Semantic Segmentation**은 “무엇이 있는가(what)”를 학습한다.  
- **Instance Segmentation**은 “누가 어디에 있는가(who, where)”를 구분한다.  
- **Panoptic Segmentation**은 “장면 전체가 어떻게 구성되어 있는가(how)”를 이해한다.  

---

## 4. 공통 구조와 차이점  

### (1) 공통 구조: Encoder–Decoder Framework  

Segmentation 모델은 대부분 **Encoder–Decoder 구조**를 사용한다.  

```
입력 이미지
   ↓
[Encoder] Feature 추출
   ↓
[Decoder] 공간 해상도 복원
   ↓
픽셀 단위 클래스 맵 출력
```

| 구성 요소 | 역할 | 주요 기술 |
|------------|------|-----------|
| **Encoder** | CNN/Transformer 기반 특징 추출 | VGG, ResNet, EfficientNet, Swin Transformer |
| **Decoder** | 피처맵 Upsampling, 공간 복원 | Deconvolution, Upsample, Skip Connection |
| **Skip Connection** | 세밀한 경계 복원 | 저층(Edge) 정보와 고층(Semantic) 정보 결합 |

---

### (2) 차이점  

| 구분 | 주요 차이점 | 추가 모듈 |
|------|--------------|------------|
| **Semantic Segmentation** | Encoder-Decoder 구조만 사용, 객체 간 구분 없음 | 없음 |
| **Instance Segmentation** | Detection 구조(Faster R-CNN 등)와 결합 | RPN, ROI Align, Mask Head |
| **Panoptic Segmentation** | Semantic + Instance 결과 융합 | FPN 기반 통합 모듈 |

즉, Instance와 Panoptic은 기본적인 Encoder-Decoder 구조 위에  
**탐지기(Detection Head)** 와 **마스크 융합(Fusion Head)** 을 추가한 확장형 구조라고 볼 수 있다.  

---

## 5. 대표 모델별 구조적 특징  

| 모델 | 구조적 특징 | 기술적 의의 |
|------|---------------|---------------|
| **FCN (2015)** | Fully Connected층 제거, Upsampling으로 복원 | Segmentation의 기본 구조 확립 |
| **U-Net (2015)** | Skip Connection 기반 Encoder–Decoder | 정밀한 구조 복원에 유리 |
| **DeepLab v3+ (2018)** | Atrous Convolution + ASPP 모듈 | 다중 수용 영역 확보 |
| **Mask R-CNN (2017)** | Detection + Mask Head 병렬 구조 | Instance Segmentation의 표준 |
| **Panoptic FPN (2019)** | FPN으로 Semantic + Instance 통합 | 장면 전체 일관성 확보 |

---

## 6. 평가 지표  

Segmentation 모델은 객체의 형태 예측 정확도를 평가하기 위해  
다음과 같은 지표를 사용한다.

\[
IoU = \frac{TP}{TP + FP + FN}, \quad Dice = \frac{2TP}{2TP + FP + FN}
\]

| 지표 | 특징 | 주요 활용 |
|------|------|-----------|
| **IoU (Intersection over Union)** | 전체 예측 영역과 정답 영역의 겹침 비율 | 일반 Segmentation, Detection |
| **Dice Coefficient** | IoU 대비 작은 객체에 민감 | 의료 영상 등 불균형 데이터에 유리 |

---

## 7. 응용 분야  

| 분야 | 구체적 예시 |
|------|--------------|
| **자율주행** | 차선, 도로, 신호등, 보행자 구분 |
| **의료 영상 분석** | 종양, 장기, 병변 영역 세분화 |
| **위성·항공 영상 분석** | 도심, 수역, 산림 구분 |
| **산업 검사** | 제품 불량 부위 탐지 |
| **로보틱스** | 객체 조작 시 픽셀 단위 인식 활용 |

---

## 8. 마무리  

Segmentation은 이미지의 의미를 픽셀 단위로 해석하는 기술로,  
Object Detection의 한계를 극복하며 시각적 이해(Visual Understanding)의 정밀도를 높였다.  

- Semantic Segmentation → 장면의 의미 파악  
- Instance Segmentation → 객체별 구분  
- Panoptic Segmentation → 장면 전체의 통합 표현  

다음 글에서는 이 중 **Instance Segmentation (Mask R-CNN)** 의 구조와  
학습 방식을 구체적으로 분석하여,  
Detection에서 Segmentation으로의 기술적 확장을 살펴볼 예정이다.  

---

🏷️ **해시태그**  
#Segmentation #SemanticSegmentation #InstanceSegmentation #PanopticSegmentation #U-Net #DeepLab #MaskRCNN #딥러닝 #ComputerVision #AI연구 #DeepLearning  
