# 1. 머리글

Transformer는 Self-Attention을 통해 시퀀스를 병렬로 처리할 수 있는 구조를 제시했다. 이 구조를 기반으로 등장한 대표적인 모델이 BERT와 GPT이다. 두 모델은 모두 Transformer를 사용하지만, 목표 태스크, 학습 방식, 아키텍처 선택에서 근본적으로 다른 결정을 내렸다.

이번 글에서는 BERT와 GPT를 성능 측면이 아니라 **어떤 문제를 풀기 위해 어떻게 설계되었는가**라는 관점에서 비교해 보고자 한다.

---

# 2. 공통 기반(Transformer)과 핵심 차이

## (1) 공통 기반

BERT와 GPT는 모두 Transformer를 기반으로 한다. Self-Attention을 통해 토큰 간 관계를 직접 계산하고, Positional Encoding으로 순서 정보를 보완한다.

차이는 Transformer를 어느 방향으로, 어떤 목적에 맞게 사용했는지에서 발생한다.

## (2) 핵심 차이 ①: Encoder vs Decoder

가장 중요한 구조적 차이는 사용하는 Transformer 블록이다.

- **BERT**: Transformer **Encoder** 스택  
- **GPT**: Transformer **Decoder** 스택  

Encoder는 입력 전체를 동시에 보고 각 토큰을 인코딩한다.  
Decoder는 미래 토큰을 보지 못하도록(masking) 제한된 상태에서 다음 토큰을 예측한다.

사용 블록의 차이는 BERT와 GPT의 성격 차이를 직접적으로 야기한다.

## (3) 핵심 차이 ②: Attention 구조

### BERT – Bidirectional Self-Attention

BERT는 입력 문장의 양쪽 문맥을 모두 참조한다. 각 토큰은 좌우 모든 토큰과 Self-Attention을 수행한다.

여기서 중요한 점은 **mask가 없다는 것**이다. 즉, 모든 위치가 서로를 자유롭게 참고할 수 있다.  
이로 인해 BERT는 문맥 이해, 의미 표현, 토큰 수준 분류에 매우 강한 성능을 보인다.

### GPT – Causal (Masked) Self-Attention

GPT는 언어 모델링을 목표로 설계되었다. 따라서 토큰 t는 자기 자신과 이전 토큰만 볼 수 있다. 이를 위해 Attention score 계산 시 **causal mask**를 적용한다.

여기서 M은 미래 토큰 위치에 -∞를 주는 mask다.  
이 구조 덕분에 GPT는 자연스러운 문장 생성, 자동 회귀적 텍스트 생성에 최적화된다.

## (4) 핵심 차이 ③: 학습 목표(Objective)

### BERT – Masked Language Model (MLM)

BERT는 입력 문장의 일부 토큰을 **[MASK]**로 가리고, 해당 토큰을 예측하도록 학습한다.  
이로 인해 BERT는 양방향 문맥 활용이 가능하고, 문장 전체 의미를 학습하며, 생성 모델로 사용하기는 부적합하다.

BERT는 본질적으로 **이해(encoding) 중심 모델**이다.

### GPT – Autoregressive Language Model

GPT는 다음 토큰을 순차적으로 예측한다.

이 방식은 텍스트 생성에 자연스럽고, 학습과 추론 구조가 일관되며, 프롬프트 기반 확장이 용이하다.  
GPT는 **생성(decoding) 중심 모델**이다.

---

# 3. 구조 선택이 만들어낸 성격 차이

| 구분 | BERT | GPT |
|---|---|---|
| Transformer 블록 | Encoder | Decoder |
| Attention | Bidirectional | Causal |
| 학습 목표 | MLM | Autoregressive |
| 강점 | 문맥 이해 | 텍스트 생성 |
| 대표 사용처 | 분류, QA | 생성, 대화 |

BERT는 학습 시 **[MASK]** 토큰을 사용한다. 하지만 실제 추론 단계에서는 [MASK]가 존재하지 않는다. 이로 인해 학습-추론 불일치가 발생하고, 순차적 생성이 자연스럽지 않다.

GPT는 단방향 구조이지만, 모델 크기 증가와 프롬프트 설계로 이해 태스크까지 확장되었다. 이는 구조의 우수성이라기보다 **Autoregressive 학습의 단순성**, **대규모 데이터 스케일링 가능성**, **하나의 objective로 다양한 태스크 처리**라는 설계 선택의 결과이다.

---

# 4. 마무리

BERT와 GPT는 같은 Transformer를 사용하지만, 서로 다른 문제를 풀기 위해 정반대의 선택을 했다. BERT는 이해를 극대화하기 위해 양방향 인코딩을 선택했고, GPT는 생성을 극대화하기 위해 단방향 디코딩을 선택했다.

이 차이는 이후 등장하는 모든 NLP 모델 설계의 기준점이 된다.

---
