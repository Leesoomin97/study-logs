## 1. 머리글

Retrieval 단계에서 문서를 가져온 것이 곧바로 좋은 답변으로 이어지는 것은 아니다. 실제 RAG 시스템에서는 '문서를 찾는 것'보다 '어떤 문서를 먼저 보여줄 것인가'가 더 중요한 문제가 된다.

Dense Retrieval이나 Hybrid Retrieval은 관련 문서를 일정 수준까지 찾아내는 데는 효과적이지만 그 순서(rank)가 항상 질문의 의도와 일치하지는 않는다. 이 때문에 상위에 질문과 관계가 없는 문서가 포함되는 문제가 발생한다.

이 문제를 해결하기 위한 단계가 Reranking이다. Reranking은 Retrieval 결과를 다시 평가하여 질문에 더 적합한 문서를 상위로 재정렬하는 과정이다.

---

## 2. Retrieval과 Ranking의 차이

Retrieval과 Ranking은 서로 다른 문제를 다룬다.

| 단계 | 역할 |
|---|---|
| Retrieval | 관련 문서를 넓게 찾는 단계 |
| Ranking | 그 중에서 가장 적합한 문서를 선택하는 단계 |

Retrieval은 recall 중심이기 때문에 가능한 많은 관련 문서를 놓치지 않는 것이 중요하다. 반면 Ranking은 precision 중심으로 상위 문서가 실제로 질문에 답이 되는 것이 중요하다.

이 두 목표는 서로 충돌할 수 있기 때문에 RAG 시스템에서는 Retrieval 이후에 별도의 Ranking 단계가 필요하다.

---

## 3. Reranker의 기본 개념

Reranker는 query와 document를 함께 입력받아, 해당 문서가 질문에 얼마나 적합한지를 평가한다.

Dense Retrieval이 query와 document를 각각 embedding한 뒤 비교하는 방식이라면, Reranker는 두 텍스트를 동시에 고려한다는 점에서 차이가 있다. 이 차이는 아래의 예시를 통해 살펴볼 수 있다.

Retrieval: 이 문서는 비슷한가?  
Reranker: 이 문서는 답이 되는가?  

이 차이가 Reranking의 핵심이다.

---

## 4. Cross-encoder 기반 Reranking

Reranking에서 가장 많이 사용되는 방식은 cross-encoder 구조이다. 이 방식에서는 query와 document를 하나의 입력으로 결합하여 모델에 전달한다.

Input: [Query] + [Document]  
Output: relevance score  

이 방식의 특징은 다음과 같다.

- query와 document 간 상호작용을 직접 반영  
- 문맥 기반 relevance 평가 가능  
- 높은 precision  

하지만 단점도 존재한다.

- 연산 비용이 높음  
- latency 증가  
- 대규모 문서 처리에 비효율적  

따라서 cross-encoder는 보통 top-k 문서에만 적용된다.

---

## 5. Reranking 구조

일반적인 RAG 시스템에서 Reranking은 다음과 같이 구성된다.

Retrieval (top-k 문서 확보)  
Reranker 적용  
상위 n개 문서 선택  
LLM 입력  

이 구조에서 중요한 것은 k 값과 n 값의 설정이다. k가 너무 작으면 recall이 부족하고, k가 너무 크면 비용이 증가한다. 즉, Retrieval과 Reranking 사이의 균형이 필요하다.

---

## 6. Reranking이 필요한 이유와 그 한계

Reranking은 다음과 같은 문제를 해결한다.

첫 번째는 semantic similarity와 relevance의 차이이다. embedding 기반 검색은 “비슷한 문서”를 찾지만, 그것이 반드시 답이 되는 문서는 아니다. 두 번째는 Hybrid Retrieval의 노이즈 문제이다. BM25와 Dense 결과를 합치면 recall은 증가하지만, irrelevant 문서도 함께 증가한다. 세 번째는 LLM 입력 품질 문제이다. LLM은 입력된 문서를 그대로 활용하기 때문에, 잘못된 문서가 포함되면 hallucination 가능성이 증가한다.

그러나 Reranking 역시 완벽한 해결책은 아니다.

첫 번째는 비용 문제이다. cross-encoder는 query-document 쌍마다 계산이 필요하기 때문에 비용이 빠르게 증가한다. 두 번째는 context length 제한이다. 문서가 길 경우 일부 정보만 반영될 수 있다. 세 번째는 모델 의존성이다. reranker의 성능은 모델에 크게 의존하며, 도메인에 따라 성능 차이가 발생할 수 있다.

따라서 reranking은 단독으로 사용하는 것이 아니라, Retrieval 설계와 함께 고려되어야 한다.

---

## 7. 마무리

Reranking은 Retrieval 단계에서 확보한 문서를 다시 평가하여, 질문에 더 적합한 문서를 상위로 정렬하는 과정이다. Retrieval이 가능한 문서를 찾는 단계라면 Reranking은 실제로 사용할 문서를 선택하는 단계이다.

이 과정은 단순한 후처리가 아니라, RAG 시스템의 답변 품질을 결정하는 핵심 단계 중 하나이다. 결국 중요한 것은 문서를 많이 찾는 것이 아니라, 정확한 문서를 상위에 배치하는 것이다.

---