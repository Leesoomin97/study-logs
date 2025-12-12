# 1. 머리말

Transformer 기반 Segmentation은 장거리 의존성 학습과 통합 구조라는 강점에도 불구하고, 실제 응용에서는 여러 제약이 존재한다. 특히 ViT 기반 모델들은 연산량이 매우 크고, 고해상도 입력을 처리할 때 메모리 사용량이 급증한다. 이러한 문제는 자율 주행, 로보틱스, 임베디드 시스템처럼 실시간 추론이 필요한 환경에서는 결정적인 한계가 된다.

SegFormer는 이러한 문제를 해결하기 위해 등장한 모델로, 가볍고 빠르면서도 정확도 손실이 적은 Efficient Transformer Encoder를 구성하고, 단순화된 MLP Decoder로 실용성과 성능의 균형을 맞춘 구조를 갖는다.

특히 Backbone과 Decoder가 모두 간결하며, multi-scale feature 처리 능력이 강화되어 기존 CNN 기반 Segmentation(U-Net, DeepLab)과 Transformer 기반 모델(ViT, SETR)의 중간 지점을 기술적으로 설계한 모델이라고 볼 수 있다.


# 2. SegFormer의 핵심 개념

SegFormer는 크게 두 가지 기술적 목표를 갖고 설계되었다.

## (1) Lightweight Transformer Encoder

- hierarchical 구조를 통해 CNN과 유사한 multi-scale feature 생성  
- positional embedding 제거 → 다양한 해상도 입력 대응  
- overlapping patch merging → local 정보 보존 + global attention 결합  

## (2) Simple MLP Decoder

- 복잡한 upsampling/skip-connection 구조 없이 단순한 MLP  
- multi-scale feature를 통합하는데 최적화  
- 실제 FLOPs 대비 높은 성능(accuracy-per-compute 효율 우수)  

이 두 가지 개념 덕분에 SegFormer는 파라미터 수와 연산량을 크게 줄이면서도, ADE20K, Cityscapes, COCO-Stuff 등 주요 데이터셋에서 SOTA에 근접한 성능을 기록했다.


# 3. 모델 전체 구조

SegFormer는 다음과 같은 Encoder-Decoder 구조를 기반으로 하지만, 기존 CNN 기반 구조와 달리 Transformer의 전역 문맥 학습 능력과 CNN의 multi-scale feature 표현 방식을 자연스럽게 결합한 형태로 설계되어 있다. 전체 구성은 Mix Transformer(MiT) Encoder와 Lightweight MLP Decoder 두 부분으로 나뉜다.

## (1) Encoder: Mix Transformer(MiT)

Segformer의 Encoder는 계층적 Transformer 구조로, CNN처럼 multi-scale feature를 생성하면서도 Self-Attention을 통해 global context를 함께 학습한다.

### ① 구성 요소

- 이미지를 4단계(Stage)로 처리하는 hierachical Transformer  
- 각 Stage에서 patch merging으로 해상도 ↓, 채널 ↑  
- Overlapping patch embedding으로 local texture 정보 보존  
- Self-Attention으로 장거리 의존성 모델링  

### ② 기술적 특징

- Positional Embedding 제거 → 입력 해상도 변화에 안정적  
- Multi-scale feature 자연 생성 → DeepLab처럼 별도 모듈(ASPP)이 필요 없음  
- Lightweight 구조 → 동일 FLOPs 대비 높은 표현력  

이 구조는 CNN 기반 특징의 지역성(Locality)과 Transformer의 전역성(Globality)을 함께 얻는 것이 핵심 목표이다.

## (2) Decoder - Lightweight MLP Decoder

SegFormer의 Decoder는 기존 segmentation 모델 대비 매우 단순하며, 모든 Feature Map을 MLP로 정규화 후 통합하는 방식으로 구성된다.

### ① 구성 요소

- Encoder의 Stage 1~4 Feature Map 입력  
- 각 Feature를 MLP로 channel projection  
- 공간 크기를 통일해 upsampling  
- 최종 semantic segmentation map 생성  

### ② 기술적 특징

- No convolution, no attention → 연산량 최소화  
- Multi-scale feature를 단일 경로에서 통합  
- 추론 속도 빠름, GPU/CPU 환경 모두 안정적  

Mask2Former처럼 복잡한 query 기반 구조가 아니며, Tensor 연산 구조가 단순해 GPU, CPU inference 모두 빠르다는 특징을 가지고 있다. 이렇게 기능 중심으로 설계된 구조라 실험 환경, 실무 환경 모두에서 다루기 쉽다.


# 4. SegFormer의 장단점

## (1) 장점

SegFormer의 가장 큰 장점은 효율성과 정확도의 균형이다. MiT Encoder는 hierarchical Transformer 구조로 다양한 스케일의 특징을 안정적으로 추출하며, Decoder는 MLP 기반으로 불필요한 연산을 제거해 경량 모델에서도 높은 성능을 얻는다. 입력 해상도 변화에 둔감한 구조 또한 실무에서 유리한 점이다.

## (2) 단점

반면 SegFormer는 Semantic 전용 설계이기 때문에 Instance 단위 정보가 필요한 작업(Instance Segmentation, Panoptic Segmentation)에서는 구조적 확장이 필요하다. 또한 query 기반 Transformer 모델에 비해 객체 간 관계를 정교하게 모델링하는 능력은 상대적으로 제한적이다.

## (3) 결론

요약하자면, SegFormer는 효율성 Transformer Segmentation의 대표 모델이며, 대규모 장면 이해보다는 실용적, 경량화 기반의 Semantic Segmentation에 최적화된 구조이다.


# 5. 실무 활용 사례

| 분야 | 활용 예시 |
|---|---|
| 자율주행 | 도로 구조 분할, 차선/보도 분리, semantic map 생성 |
| 로보틱스 | navigation 용 공간 분리, occupancy map 생성 |
| 산업 검사 | 결함 segmentation, 영역별 표시 |
| 의료 영상 | 장기/조직 분할, low-parameter 환경에서 활용 |
| 위성, 항공 영상 | 토지 분류, 건물/도로 semantic 분리 |


# 6. SegFormer vs. U-Net/DeepLab 요약 비교

| 모델 | 구조 | 강점 | 한계 |
|---|---|---|---|
| U-Net | CNN encoder-decoder + skip connection | 소규모 데이터에서 강함, 구조 단순 | global context 부족 |
| DeepLabv3+ | Dilated conv + ASPP | multi-scale 수용 영역, 강력한 성능 | 모델 크기 큼 |
| SegFormer | MiT Transformer + MLP decoder | 경량, 고효율, multi-scale 자연 처리 | instance/panoptic은 별도 구조 필요 |


# 7. 마무리

SegFormer는 Transformer 기반 Segmentation의 실용적 형태를 정의한 모델이다.

ViT 기반의 무거운 구조를 실제 응용 단계에서 사용할 수 있도록 최적화했고, multi-scale feature 표현과 단순한 decoder 구조를 통해 정확도, 속도, 메모리 사용량의 균형을 성공적으로 맞췄다.

SegFormer 이후 등장한 Mask2Former, SAM 등 최신 모델들은 더 강력한 전역 표현 또는 prompt 기반 Segmentation으로 확장되었지만, 효율형 Transformer 백본이라는 관점에서 SegFormer는 여전히 강력한 baseline으로 사용된다.

#SegFormer #TransformerSegmentation #VisionTransformer #딥러닝 #ComputerVision #CV모델 #Segmentation #딥러닝블로그 #MLPDecoder #DeepLearningModel
