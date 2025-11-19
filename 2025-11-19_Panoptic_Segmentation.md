# Panoptic Segmentation (2025.11.19)

## 1. 머리말

이전 글에서는 Semantic Segmentation과 Instance Segmentation을 각각 분석하며, 픽셀 단위의 분류 또는 객체 단위의 구분이라는 서로 다른 목적을 수행함을 설명했다. 하지만 실제 컴퓨터 비전 응용에서는 이 두 작업만으로는 충분하지 않은 경우가 많다.

예를 들어 자율주행에서는 도로, 차선, 보도블록 같은 배경 요소도 중요하고, 동시에 보행자, 차량 같은 객체를 개별적으로 인식해야 한다.

그렇기에 단순히 픽셀 분류만 하거나 객체 분리만 하는 방식으로는 장면 전체의 구조를 한 번에 이해하는 일이 불가능하다.

Panoptic Segmentation은 이러한 실무적 요구를 해결하기 위해 등장한 기술로, Semantic과 Instance의 장점을 결합해 모든 픽셀에 대해 정보 손실 없이 클래스, 인스턴스 ID를 부여하는 문제이다.

따라서 Panoptic은 개별 객체만 예측하는 Detection, Instatnce보다 더 높은 수준의 장면 이해를 가능하게 하며, 자율주행, 로보틱스, 디지털 트윈, 인식 기반 제어 시스템 등에서 사실상 기본 구조로 채택되고 있다.

---

## 2. Panoptic Segmentation의 개념

Panoptic Segmentation의 목적은 장면의 모든 픽셀을 완전하게 설명하는 것이다. 이를 위해 각 픽셀마다 다음 두 정보를 동시에 예측한다.

### 📌 Stuff vs Thing 비교

| 구분 | Semantic 정보 | Instance 정보 |
|------|----------------|----------------|
| **예측 단위** | 픽셀 단위 클래스 분류 | 객체(인스턴스) 단위 분리 |
| **대상** | 하늘, 도로, 벽, 풀, 물 등 배경 요소 | 사람, 자동차 등 개별 객체 |
| **출력 형태** | class_label만 존재 | class_label + instance_id |
| **인스턴스 구분** | 없음(동일 클래스는 하나의 영역) | 동일 클래스 내에서도 instance를 분리 |
| **예시** | (sky, id=0), (road, id=0) | (person, id=1), (person, id=2), (car, id=1) |

즉, Panoptic에서는 픽셀 하나가 다음과 같이 표현된다.

```
(pixel) -> (class_label, instance_id)
```

- Stuff 클래스: instance_id = 0  
- Thing 클래스: instance_id = 1, 2, 3 ... 개별 객체 분리  

이 구조는 Semantic의 전체 영역 이해와 Instance의 객체 개별 분리 기능을 통합하여 실제 장면 전체를 구조적으로 이해할 수 있게 한다.

---

## 3. Panoptic Segmentation이 필요한 이유

Panoptic이 필요해진 배경은 크게 세 가지 방향으로 설명할 수 있다.

### (1) 실세계 장면은 Stuff와 Thing이 항상 공존함

현장의 이미지에는 배경과 객체가 항상 함께 존재한다. 도로, 하늘, 건물 같은 Stuff가 제공하는 환경적 맥락은 사람, 차량 같은 객체의 행동을 이해하는 데 필수다. Panoptic은 이 둘을 하나의 출력 구조에서 자연스럽게 통합한다.

### (2) Instance Segmentation만으로는 Scene-level 해석이 불가능

Instance Segmentation은 객체 개수와 위치는 잘 예측하지만 객체가 위치한 배경 정보와 주변 구조를 설명하지는 못한다. Panoptic은 객체가 어떤 환경 위에 존재하는지를 함께 표현하여 장면의 전체적 맥락을 해석할 수 있도록 한다.

### (3) 최신 비전 백본은 통합 구조를 전제로 설계됨

DETR, Mask2Former, Segment Anything 같은 최신 모델들은 Detection/Segmentation을 나누지 않고 통합 파이프라인으로 처리한다. Panoptic은 이러한 통합 구조의 목적 함수 역할을 하며 현대 Vision 모델의 방향성을 가장 잘 반영하는 문제 정의이다.

---

## 4. Panoptic 평가 지표 + Fusion 구조

### (1) 평가 지표

Panoptic은 Semantic과 Instance를 통합하는 문제이기 때문에 일반 mloU, AP만으로는 품질을 평가하기 어렵다. 이를 위해 PQ(Panoptic Quality) 지표가 사용된다.

| 지표 | 의미 | 설명 |
|------|--------|---------|
| **SQ** | Segmentation Quality | 매칭된 객체 쌍의 평균 IoU. 마스크 자체의 품질을 나타냄 |
| **RQ** | Recognition Quality | 객체 매칭의 정확도(Detection 품질). F1-score 방식의 평가 |

SQ가 높으면 마스크를 잘 그렸다는 의미이며,  
RQ가 높으면 객체를 제대로 찾았다는 의미이다.

둘 중 하나만 좋아도 PQ는 높게 나오지 않기 때문에 Panoptic은 Detection + Segmentation 모두 잘해야 하는 문제임을 알 수 있다.

---

### (2) Panoptic Fusion (Stuff + Thing 통합 규칙)

Panoptic 출력은 Semantic 결과와 Instance 결과를 규칙에 따라 통합하여 생성한다.

① **Thing 우선 규칙**  
- 동일 영역에 Stuff, Thing이 모두 존재하면 Thing을 우선 배치  
- 객체 경계 보존을 위함  

② **Stuff는 단일 영역 처리**  
- 하늘 하나, 도로 하나 같은 동일 클래스를 하나로 합침  

③ **Instance 간 겹침 처리**  
- IoU 기반 priority  
- 낮은 confidence instance 제거  
- 필요시 soft-merging 적용  

Fusion 규칙은 모든 Panoptic 모델이 공통적으로 따라야 하는 출력 통합의 핵심 설계 요소이다.

---

## 5. Panoptic Segmentation의 주요 모델 구조

### (1) Panoptic FPN (2019)

① **기본 아이디어**  
- Faster R-CNN + FPN 구조 기반  
- Semantic Head + Instance Head → Panoptic Fusion  

② **기술적 특징**  
- 다중 스케일 Feature 활용  
- Instance Branch는 FCN 구조  
- 두 출력을 Panoptic Fusion으로 결합  

③ **한계 및 의의**  
- 가장 기본적인 Panoptic 구조 제시  
- 분리된 두 Branch로 인해 joint optimization은 제한적  

---

### (2) UPSNet (2019)

① **기본 아이디어**  
- Fusion 모듈 자체를 최적화하여 Panoptic 품질을 높인 모델  

② **기술적 특징**  
- Panoptic Fusion Module(PFM) 탑재  
- Stuff/Thing 충돌 영역 자동 조정  
- Soft-weighted blending 방식 적용  

③ **한계 및 의의**  
- 구조는 복잡하지만, 실제 Panoptic 품질은 크게 향상  
- Fusion 전략 고도화의 대표적인 사례  

---

### (3) Mask2Former (2021)

① **기본 아이디어**  
- Query 기반 Mask Prediction으로 모든 세그멘테이션 유형을 하나의 구조로 처리  

② **기술적 특징**  
- Transformer Decoder 기반 mask attention  
- Instance/Semantic/Panoptic 모두 동일 구조로 처리  
- COCO, ADE20K 등 다수 벤치마크에서 SOTA 기록  

③ **한계 및 의의**  
- 연산량이 높지만 성능은 사실상 최고  
- 현대 Panoptic Segmentation의 표준 구조  

---

### (4) Segment Anything Model (SAM, 2023)

① **기본 아이디어**  
- Prompt 기반 Zero-shot Segmentation을 수행하는 Foundation Model  

② **기술적 특징**  
- 수백억 개의 마스크로 대규모 사전학습  
- 박스, 포인트 기반 Prompt 입력 가능  
- 마스크 생성기 기반 구조  

③ **한계 및 의의**  
- Panoptic 전용 모델은 아니지만 장면 전체를 자동 마스킹하는 기능이 Panoptic-like  
- 범용 Segmentation 시대를 여는 중요한 전환점  

---

## 6. 종합 정리 및 마무리

Panoptic Segmentation은 Semantic의 전역(Scene) 분류 능력과 Instance의 객체 분리 능력을 통합한 최종 형태의 Segmentation이다.

핵심 정리는 다음과 같다.

- 문제 정의: 모든 픽셀에 (class, instance_id) 부여  
- 필요성: Stuff-Thing 공존 환경에서 완전한 Scene Understanding 가능  
- 평가 지표: PQ = SQ * RQ  
- Fusion 규칙: Thing 우선, Stuff 단일화, Instance 겹침 처리  
- 주요 모델: Panoptic FPN → UPSNet → Mask2Former → SAM  
- 의의: 최신 Vision Transformer 기반 모델의 기본 문제 정의로 자리 잡음  

Panoptic은 Segmentation의 마지막 단계가 아니라, "Scene Understanding 전체"를 위한 핵심 구성 요소이며, 이후의 Vision Transformer 모델을 이해하기 위한 기반이 된다.
