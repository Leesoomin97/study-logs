# 1. 머리글

Attention 메커니즘은 RNN의 문맥 병목 문제를 해결했지만, 구조적으로는 여전히 RNN 위에 얹혀 있었다. 즉, 문맥 선택은 가능해졌지만 순차 처리라는 제약 자체는 그대로 남아 있었다. 이로 인해 병렬화가 어렵고, 긴 시퀀스를 처리할수록 계산 효율이 급격히 떨어지는 문제는 해결되지 않았다.

Transformer는 이 지점에서 한 걸음 더 발전한다. 시퀀스를 반드시 순차적으로 처리해야 하는가에 대한 질문을 던지고, 그 답으로 Self-Attention 만으로 시퀀스를 모델링하는 구조를 제안했다.

이번 글에서는 Transformer가 어떤 구조적 결정을 통해 RNN을 제거할 수 있었는지, 그리고 그 핵심이 되는 Self-Attention이 어떻게 작동하는지를 중심으로 살펴보고자 한다.

---

# 2. Transformer의 핵심 가정

Transformer은 시퀀스 내 각 토큰이 다른 모든 토큰과의 관계를 직접 계산할 수 있다는 가정 하에 출발한다.

이 가정이 성립한다면, 이전 토큰의 계산 결과를 기다릴 필요 없이 모든 토큰을 동시에 처리할 수 있다. 즉, 순차 처리의 필요성이 사라진다.

이 역할을 수행하는 구조가 바로 Self-Attention이다.

---

# 3. Self-Attention의 구조적 차이

Self-Attention은 이전 글에서 다룬 Attention과 계산 형태는 유사하지만, Query, Key, Value가 모두 동일한 시퀀스에서 생성된다는 점에서 차이가 있다.

입력 시퀀스를 \( X \in \mathbb{R}^{n \times d} \)라고 하면, 각 토큰은 다음과 같은 선형 변환을 거쳐 Q, K, V로 매핑된다.


- Q = X · W_Q
- K = X · W_K
- V = X · W_V

여기서 \( W_Q, W_K, W_V \)는 학습 가능한 파라미터이다.

즉, 각 토큰은

- **Query**로서 무엇을 찾을지를 표현하고  
- **Key**로서 자신이 어떤 정보를 가지고 있는지를 나타내며  
- **Value**로서 실제로 전달할 정보를 담는다  

---

# 4. Self-Attention 계산 과정

Self-Attention은 다음과 같이 계산된다.

- Attention(Q, K, V) = softmax(QK^T / √d_k) V

이 식은 다음 의미를 가진다.

- **QKᵀ**: 모든 토큰 쌍 간의 유사도 계산  
- **√d_k**: dot-product 값의 스케일 조정  
- **softmax**: 각 토큰이 다른 토큰에 얼마나 집중할지 정규화  
- **최종 결과**: 각 토큰이 다른 모든 토큰을 참고해 재구성된 표현  

이 결과로 생성된 벡터는 단순한 임베딩이 아니라, 문맥 정보를 반영한 토큰 표현이다.

---

# 5. 왜 병렬화가 가능한가

RNN에서는 시점 t의 hidden state가 t-1에 의존했기 때문에, 계산이 본질적으로 순차적이었다.

반면 Self-Attention에서는 모든 토큰의 Q, K, V가 동시에 계산되고, QKᵀ 연산 역시 행렬 곱으로 한 번에 처리된다.

즉, 시퀀스 길이와 관계없이 한 레이어 내에서는 모든 토큰이 병렬로 계산된다. 이 점이 Transformer가 대규모 데이터와 긴 문맥에서 압도적인 효율을 가지는 이유이다.

---

# 6. Position 정보는 어떻게 처리되는가

Transformer는 RNN처럼 순서를 따라 처리하지 않기 때문에 토큰의 위치 정보가 자연스럽게 반영되지 않는다. 이를 보완하기 위해 Transformer는 입력 임베딩에 **Positional Encoding**을 더한다.

대표적인 방식은 사인 함수와 코사인 함수를 이용하는 고정 인코딩이다.

PE(pos, 2i) = sin(pos / 10000^(2i/d))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d))

이를 통해 모델은 토큰의 절대 위치와 토큰 간 상대적 거리를 간접적으로 학습할 수 있다.

---

# 7. Multi-Head Attention의 필요성

단일 Attention은 하나의 관점으로만 관계를 바라본다. 하지만 자연어에서는 다양한 관계가 동시에 존재한다.

Multi-Head Attention은 Q, K, V를 여러 하위 공간으로 분할한 뒤, 각각 독립적인 Attention을 수행한다.

이를 통해 모델은 문법적 관계, 의미적 유사성, 장거리 및 단거리 의존성 등을 서로 다른 head에서 동시에 포착할 수 있다.

---

# 8. Transformer Encoder의 전체 구조

하나의 Transformer Encoder 레이어는 다음으로 구성된다.

- Multi-Head Self-Attention  
- Add & Layer Normalization  
- Position-wise Feed Forward Network  
- Add & Layer Normalization  

Residual connection과 LayerNorm은 깊은 네트워크에서도 안정적인 학습을 가능하게 한다.

---

# 9. 마무리

Transformer는 Attention을 보조 메커니즘이 아니라 시퀀스 모델링의 중심 연산으로 끌어올린 구조이다. 이는 순차 처리를 제거함으로써 병렬화를 가능하게 했고, Self-Attention을 통해 문맥 정보를 직접 계산하게 만들었다.

이 구조적 선택은 이후 등장하는 BERT, GPT 등 대부분의 현대 NLP 모델의 기반이 된다.

---

