# 1. 머리말

CNN 기반 Segmentation 모델은 국소적 패턴(local pattern) 추출에 장점이 있지만, 다음과 같은 구조적 한계가 존재한다.

① Convolution은 고정된 크기의 resceptive field를 갖기 때문에 장거리(long-range) 의존성을 충분히 학습하기 어렵다.  
② Multi-scale 대응을 위해 별도의 구조(FPN, ASPP 등)을 추가해야 한다.  
③ 객체 수가 늘어나거나 복잡한 장면(Scene)이 등장하면 경계 정보와 전역 문맥(global context)을 동시에 최적화하기 쉽지 않다.

Vision Transformer(ViT)의 등장 이후, Segmentation에서도 CNN의 한계를 극복하기 위한 Transformer 기반 구조가 빠르게 확산되었다.

해당 구조는 CNN 없이도 global context를 직접 학습하고, fixed receptive field를 제거하며, multi-scale 문제를 구조적으로 해결하고 Detection-Segmentation을 통합하는 범용 아키텍처를 구축하고자 한다.

이 글에서는 SETR → MaskFormer → Mask2Former → SAM으로 이어지는 Transformer 기반 Segmentation의 기술 발전 흐름을 정리하고자 한다.

---

# 2. Transformer 기반 Segmentation의 핵심 개념

Transformer가 Segmentation에 적용되면서 생긴 구조적 변화는 크게 세 가지이다.

## (1) 이미지 패치화(Patch Embedding)

- CNN의 convolution receptive field 제한을 제거  
- 입력 형태를 Transformer 구조와 자연스럽게 연결  

이미지를 고정 크기의 패치로 분할하고 각 패치를 벡터 형태로 임베딩한다. 이 과정에서 이미지의 2D 구조는 제거되지만, 모든 패치가 동일한 토큰 시퀀스로 처리되기 때문에 추후 Attention 연산에서 전체 패치 간 상호작용을 학습할 수 있다.

## (2) Self-Attention을 통한 장거리 관계 학습

- 전통 CNN이 여러 계층을 거쳐야만 확보할 수 있던 global view를 단일 attention으로 달성함  
- 복잡한 장면에서 유리함(도로+보행자+차량 관계 등)

Transformer의 장점은 모든 패치가 서로를 참조한다는 점이다. 즉, 멀리 떨어져 있는 객체, 경계, 패턴도 동일한 attention 공간에서 처리되므로 전역적 장면 이해(global scene understanding)가 가능하다.

## (3) Mask Classification: Query ↔ Mask 1:1 매핑

- Semantic/Instance/Panoptic이 동일 구조로 통합  
- 출력 파이프라인이 단순화되며 중복 모듈 제거  
- DETR 이후 등장한 대부분의 segmentation 모델들의 공통 철학  

Transformer 기반 Segmentation의 가장 중요한 전환점은 각 Query가 하나의 Mask를 담당하는 구조이다. 모든 segmentation 작업을 'mask를 분류하는 문제'로 통합하며, query들이 자신의 역할(semantic/instance)을 자동 학습하는 형태가 된다.

-Query -> Mask
-Mask -> Class label(semantic or instance)


이 방식은 기존 CNN 기반 파이프라인의 복잡한 anchor, proposal, FPN 구조를 대체하며, 연산 흐름을 단순화하는 동시에 성능을 높인다.

---

# 3. 주요 모델별 기술적 발전

## (1) SETR(2020)

### ① 특징
- Vision Transformer(ViT)를 최초로 Segmentation에 적용  
- CNN 기반 Encoder 제거 → 완전한 Transformer Encoder  
- Decoder는 FCN 기반 upsampling 구조 사용  

### ② 장점
- 매우 강력한 global context 학습  
- receptive field 제한 없음  
- 대규모 데이터셋에서 높은 성능  

### ③ 한계
- multi-scale 처리 구조 부재  
- Decoder가 단순해 boundary 품질 미흡  
- 고해상도 입력에서 연산량 급증  

---

## (2) MaskFormer(2021)

### ① 특징
- Mask Classification이라는 새로운 문제 정의 도입  
- 픽셀 분류 대신 mask + class = only entity로 취급  
- Query 기반 mask prediction  
- Panoptic / Semantic / Instance를 완전 통합된 구조 하나로 해결  

### ② 장점
- Segmentation 문제 정의 자체를 단순화  
- CNN, Transformer 어디든 적용 가능  
- multi-task 처리가 쉬움  

### ③ 한계
- Mask 생성 정확도는 backbone, decoder 품질에 의존  
- global context는 학습하지만 boundary는 다소 제한적  

---

## (3) Mask2Former(2022)

### ① 특징
- Segmentation의 SOTA 모델  
- MaskFormer의 구조를 확장하여 Masked Attention 도입  
- FPN 기반 multi-scale feature + Query 기반 mask decoding  
- 모든 Segmentation 유형을 단일 구조로 해결  

### ② 장점
- 현재까지 최고의 Task-agnostic segmentation 구조  
- instance, semantic, panoptic 모두 높은 성능  
- multi-scale + global attention 완전 융합  

### ③ 한계
- 연산량 매우 높음  
- 실시간 응용에는 무거움  

---

## (4) SAM(Segment Anything Model, 2023)

### ① 특징
- Meta AI가 구축한 초거대 Promptable Segmentation 모델  
- 11억 개 이상의 마스크로 학습  
- 포인트/박스/prompt 기반 interactive segmentation  

### ② 장점
- Zero-shot 성능 우수  
- 어떤 이미지에도 즉시 마스크 생성 가능  
- CV 분야에서 foundation model 역할 수행  

### ③ 한계
- 정확한 semantic consistency는 부족  
- Panoptic 품질은 Mask2Former에 비해 낮음  
- 추론 비용 높음  

---

# 4. 발전 과정 정리표

| 모델 | 핵심 아이디어 | 특징 | 장점 | 한계 |
|------|---------------|--------|--------|--------|
| SETR(2020) | pure Transformer Encoder로 segmentation 수행 | 패치→토큰→ Transformer | 전역 문맥 기반 성능 강함 | Decoder 복잡, 연산량이 큼 |
| DETR(2020) | Query 기반 Object Detection | Matching+Query 구조 도입 | Post-processing 단순화, 구조적 혁신 | 수렴이 느림 |
| Segmeter(2021) | ViT Backbone+Mask Transformer | Semantic Segmentation 전용 | ViT 기반 전역 특징 활용 | 작은 객체에서 제한 |
| MaskFormer(2021) | mask classification + query | Semantic/Instance/Panoptic 통합 구조 | task 통합 가능(파이프라인 간소화) | 일부 fine-grained 작업 약하여 boundary 약함 |
| Mask2Former(2022) | masked attention + multi-scale | 모든 segmentation의 범용 구조 | 모든 segmentation SOTA 성능, 높은 효율 | 무거운 모델로 연산량 증가함 |
| SAM(2023) | Prompt 기반 Zero-shot Masking | Foundation Model 기반 | zero-shot 강력하여 범용성 최고 | semantic 품질 낮음, Panoptic 전용 아님 |

---

# 5. 실무 활용 사례

| 분야 | 적합 모델 | 이유 |
|------|-----------|-------|
| 자율주행 | Mask2Former | 복잡한 도로 scene + multi-scale 대응 |
| 의료 영상 | SETR, Mask2Former | global info + boundary trade-off |
| 대규모 데이터 플랫폼 | SAM | zero-shot + 범용 segmentation |
| 영상 편집-창작 | SAM | 인터랙티브 편집 적합 |
| 로보틱스 | MaskFormer/M2F | instance+semantic 통합 필요 |

---

# 6. 마무리

Transformer 기반 Segmentation은 CNN 기반 구조에서 해결하기 어려웠던 global context + multi-scale + 통합 구조 문제를 근본적으로 해결했다.

SETR: pure Transformer 시도  
MaskFOrmer: segmentation 문제 정의 자체 재정의  
Mask2Former: 통합적 SOTA 구조 완성  
SAM: 실사용 가능한 foundation segmentation 모델 등장  

이러한 변화는 단순한 모델 교체를 넘어, 향후 비전 모델의 설계 패러다임이 '통합적 장면 이해(Scene Understanding)'으로 이동하고 있음을 의미한다.

따라서 Transformer 기반 Segmentation은 차세대 비전 기술의 출발점이자, 이후 등장할 멀티모달, 3D, 로보틱스 비전 모델의 핵심 기반으로 작동하게 될 것이다.

