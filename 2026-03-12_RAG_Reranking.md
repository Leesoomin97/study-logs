## 1. 머리글

RAG 시스템에서 Retrieval 품질은 전체 성능을 결정하는 가장 중요한 요소 중 하나이다. 하지만 실제로는 단순한 vector similarity 검색만으로 충분한 Retrieval 품질을 얻기는 어렵다.

Embedding 기반 검색은 의미적으로 유사한 문서를 빠르게 찾는 데에는 효과적이지만, 질문에 실제로 답이 되는 문서인지를 판단하는 능력은 제한적이다. 그 결과 검색 결과 상위에는 질문과 관련 있어 보이지만 실제로는 도움이 되지 않는 문서가 포함되는 경우가 자주 발생한다.

이러한 문제를 해결하기 위해 Retrieval 단계에서는 단순한 vector search 이후에 추가적인 정제 과정을 거친다. 그 대표적인 방법이 reranking이다. Reranking은 검색된 후보 문서를 다시 평가하여 질문과 가장 관련성이 높은 문서를 상위에 배치하는 과정이다.

---

## 2. 기본 Retrieval 파이프라인

일반적인 RAG 시스템의 Retrieval 과정은 다음과 같은 구조를 가진다.

| 단계 | 역할 |
|---|---|
| Query Encoding | 질문을 embedding 벡터로 변환 |
| Vector Search | 벡터 유사도를 이용해 후보 문서 검색 |
| Top-k Selection | 상위 k개의 문서 선택 |
| Reranking | 질문과 문서의 실제 관련성 재평가 |

Vector search는 빠르지만 정밀도가 낮고, reranking은 정확하지만 연산 비용이 높다. 따라서 대부분의 시스템에서는 vector search로 후보군을 줄인 뒤 reranking으로 정밀도를 높이는 방식을 사용한다.

---

## 3. Reranking의 필요성

Vector search는 일반적으로 cosine similarity나 inner product를 기반으로 한다. 이 방식은 문장의 의미적 유사성을 기준으로 검색을 수행한다.

하지만 의미적 유사성이 항상 질문에 대한 답변 가능성을 의미하는 것은 아니다. 예를 들어 다음과 같은 질문을 생각해 볼 수 있다.

질문: 서비스 설정을 변경하려면 어떤 권한이 필요한가?  
검색 결과: 서비스 설정 방법에 대한 개요

두 문장은 주제가 비슷하기 때문에 embedding 공간에서는 가까운 위치에 있을 가능성이 높다. 그러나 실제로 질문에 필요한 정보는 '권한 조건'에 대한 문서일 수 있다.

이처럼 embedding 기반 검색에서는 주제 유사성과 질문 적합성이 동일하지 않다. reranking은 이러한 문제를 해결하기 위해 사용된다.

---

## 4. Cross-encoder 기반 Reranking

Reranking에서 가장 많이 사용되는 방식은 cross-encoder 모델이다. Cross-encoder는 질문과 문서를 동시에 입력으로 받아 두 텍스트 간의 관련성을 직접 계산한다.

Vector search에서는 질문과 문서를 각각 독립적으로 embedding한 뒤 유사도를 계산한다.

sim(q, d) = cosine(embedding(q), embedding(d))

반면 cross-encoder는 질문과 문서를 하나의 입력으로 처리한다.

score = CrossEncoder([query, document])

이 방식은 계산 비용이 높지만, 문맥을 함께 고려하기 때문에 질문-문서 적합도를 더 정확하게 평가할 수 있다.

---

## 5. Reranking의 적용 방식

실제 시스템에서는 모든 문서에 reranking을 적용하지 않는다. 연산 비용이 매우 높기 때문이다. 대신 일반적으로 다음과 같은 구조를 사용한다.

① Vector search로 Top-k 문서 검색  
② 후보 문서를 reranker에 입력  
③ 상위 n개 문서를 최종 컨텍스트로 선택

예를 들어 Top-20 문서를 검색한 뒤 reranker를 통해 Top-5 문서만 LLM에 전달하는 방식이다. 이 방식은 검색 속도와 정확도 사이의 균형을 유지할 수 있다.

---

## 6. Retrieval 개선 전략

Reranking은 Retrieval 품질을 개선하는 중요한 방법이지만, 이것만으로 모든 문제가 해결되지는 않는다. Retrieval 성능은 여러 설계 요소의 영향을 동시에 받는다. 대표적으로 다음 요소들이 있다.

| 요소 | 영향 |
|---|---|
| Chunking 전략 | 문서 분할 방식 |
| Embedding 모델 | 의미 표현 품질 |
| Similarity 기준 | 검색 기준 |
| Query rewriting | 질의 표현 개선 |
| Reranking | 문서 순위 재조정 |

이 요소들은 서로 독립적인 옵션이 아니라, 하나의 Retrieval 설계를 구성하는 요소들이다. 예를 들어 chunk 크기가 지나치게 크면 reranking의 효과가 제한될 수 있으며, embedding 품질이 낮으면 reranker 이전 단계에서 후보 문서 자체가 누락될 수 있다.

따라서 Retrieval 개선은 특정 기법 하나로 해결되는 문제가 아니라 여러 설계 요소를 함께 조정하는 과정에 가깝다.

---

## 7. 마무리

RAG 시스템에서 Retrieval 단계는 단순한 검색 기능 이상의 역할을 한다. 이 단계에서 어떤 문서를 선택하느냐에 따라 생성 단계의 품질이 결정된다.

Vector search는 빠른 검색을 가능하게 하지만, 질문에 실제로 도움이 되는 문서를 항상 상위에 배치하지는 않는다. 이러한 한계를 보완하기 위해 reranking이 사용되며, 이는 질문-문서 적합도를 더 정밀하게 평가하는 역할을 한다.

또한 Retrieval 품질은 reranking 하나로 결정되지 않는다. Chunking, embedding, similarity 기준, query rewriting 등 여러 설계 선택이 함께 작용한다.

따라서 RAG 시스템의 성능을 개선하기 위해서는 단순히 LLM 모델을 교체하는 것보다 Retrieval 설계 전체를 함께 조정하는 접근이 필요하다.
---