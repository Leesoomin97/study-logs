# 1. 머리말

SegFormer는 Transformer 기반 semantic segmentation을 현실적인 수준에서 완성한 모델로 평가된다.

Pure Transformer 구조를 유지하면서도 hierarchical feature를 도입하고, 경량 decoder를 통해 고해상도 입력에서도 안정적인 성능을 확보했다는 점에서, SegFormer는 기존 Transformer 기반 segmentation 모델들이 안고 있던 연산 비용과 구조 복잡성 문제를 효과적으로 해결했다.

그러나 SegFormer 이후 등장한 segmentation 모델들은 SegFormer의 구조를 그대로 확장하거나 변형하는 방향으로 발전하지 않았다. 오히려 연구의 초점은 성능을 끌어올리는 것이 아닌, segmentation을 어떻게 더 큰 비전 시스템 안으로 통합할 것인가로 이동했다.

이 글에서는 SegFormer 이후 등장한 대표적인 segmentation 모델들이 어떤 기술적 방향 전환을 보였는지를 중심으로 정리하고자 한다.

---

# 2. SegFormer 이후의 공통 변화

SegFormer는 semantic segmentation을 dense pixel classification 문제로 다루는 마지막 세대에 가깝다.

SegFormer 이후 모델들의 가장 큰 변화는, segmentation을 더 이상 모든 픽셀에 클래스를 할당하는 문제로 직접 풀지 않는다는 점이다.

이후 모델들은 공통적으로 다음과 같은 방향을 취한다.

- 픽셀 단위 예측 대신 mask 단위 예측
- semantic, instance, panoptic을 구조적으로 분리하지 않음
- segmentation을 독립 task가 아닌 중간 표현으로 취급

이 변화의 중심에 있는 모델이 Mask2Former이다.

---

# 3. Mask2Former: Segmentation 구조의 일반화

## (1) 구조적 특성

Mask2Former는 MaskFormer의 mask classification 개념을 유지하면서, multi-scale feature와 attention 구조를 명시적으로 결합한 모델이다.

- Backbone(CNN 또는 Transformer)에서 multi-scale feature 추출
- FPN 구조를 통해 feature pyramid 구성
- Query 기반 Transformer Decoder가 각 scale의 feature를 순차적으로 참조
- 각 query는 하나의 mask와 class를 일대일로 담당

특히 Mask2Former는 Masked Attention을 도입한다.

Decoder의 attention은 전체 feature map을 보는 대신, 이전 단계에서 예측된 mask 영역을 중심으로 제한된 영역에만 집중한다.

이를 통해 multi-scale feature와 global context를 동시에 활용하면서도 연산 효율을 확보한다.

## (2) 기술적 의미

Mask2Former의 핵심은 성능 향상이 아니라 문제 정의의 통합이다.

- Semantic segmentation
- Instance segmentation
- Panoptic segmentation

위 세 문제는 모두 동일한 구조, 동일한 decoder, 동일한 학습 방식으로 처리된다. Segmentation은 더 이상 task별로 다른 파이프라인을 갖지 않는다.

---

# 4. SAM의 기술적 특징

## (1) 구조적 개요

Segment Anything Model(SAM)은 기존 segmentation 모델과 구조적 목적 자체가 다르다.

- Image Encoder: 대규모 데이터로 학습된 Vision Transformer
- Prompt Encoder: point, box, mask prompt를 embedding
- Mask Decoder: prompt-conditioned mask prediction

SAM은 semantic label을 직접 예측하지 않는다. 대신, 사용자 입력(prompt)에 조건화된 mask 생성에 집중한다.

## (2) 기술적 차별점

SAM의 핵심은 zero-shot segmentation이다.

- 사전 정의된 클래스 없음
- 데이터셋 특정 fine-tuning 없이 동작
- segmentation을 질문에 대한 응답으로 처리

이 구조에서는 segmentation이 더 이상 최종 목적이 아니다. Segmentation은 이미지 이해를 위한 기본 연산 primitive에 가깝다.

---

# 5. SegFormer 이후 흐름의 기술적 정리

SegFormer 이후 segmentation 모델들의 변화는 다음과 같이 요약할 수 있다.

1. Dense prediction 중심 설계의 종료  
   픽셀 단위 분류 구조에서 탈피

2. Mask-centric 표현의 일반화  
   query와 mask 구조가 표준이 됨

3. Task-specific 모델에서 foundation capability로 이동  
   segmentation은 독립 task가 아니라 공통 기능

이는 segmentation 모델의 진화라기보다는, segmentation이 비전 모델 내부로 흡수되는 과정에 가깝다.

---

# 6. 발전 흐름 요약표

| 구분 | SegFormer | Mask2Former | SAM |
|---|---|---|---|
| 주요 대상 | Semantic Segmentation | All Segmentation Tasks | Prompt-based Segmentation |
| 출력 단위 | Pixel-wise | Mask-wise | Prompt-conditioned Mask |
| 구조 초점 | Lightweight Transformer | Multi-scale and Query | Foundation Capability |
| 역할 | 완성형 모델 | 통합 구조 | 기본 비전 기능 |

---

# 7. 마무리

SegFormer는 Transformer 기반 semantic segmentation을 실무적으로 완성한 모델이다. 그러나 SegFormer 이후의 연구는 해당 구조를 더 정교하게 다듬는 방향으로 나아가지 않았다.

Mask2Former는 segmentation 구조를 범용화했고, SAM은 segmentation을 foundation model의 기본 능력으로 재정의했다.

이러한 변화는 segmentation 자체의 종결이 아니라, segmentation이 더 이상 독립된 연구 주제가 아니게 되었음을 의미한다.

이후의 비전 모델들은 segmentation을 직접 다루기보다는, 멀티모달 이해, 장면 추론, 로보틱스 인지 등 더 큰 문제 안에서 이를 활용하게 된다.
