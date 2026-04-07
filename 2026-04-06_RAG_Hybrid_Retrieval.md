## 1. 머리글

Embedding 기반 Retrieval은 의미 기반 검색이 가능하다는 점에서 강력한 접근 방식이다. 하지만 실제 시스템에서는 embedding만으로 모든 검색 문제를 해결하기 어렵다.

특히 숫자, 고유명사, 코드, 정확한 키워드 매칭이 중요한 경우에는 embedding 기반 검색이 오히려 성능이 떨어질 수 있다. 이 때문에 많은 RAG 시스템에서는 BM25와 Dense Retrieval을 함께 사용하는 Hybrid Retrieval 구조를 채택한다.

Hybrid Retrieval은 두 가지 서로 다른 검색 방식을 결합하여, 각각의 한계를 보완하는 접근이다.

---

## 2. Dense Retrieval의 특징

Dense Retrieval은 embedding 기반 검색 방식이다. 텍스트를 벡터로 변환한 뒤, 벡터 간 유사도를 계산하여 관련 문서를 찾는다.

이 방식의 장점은 다음과 같다.

- 의미 기반 검색 가능  
- 표현 방식이 달라도 유사 문서 검색 가능  
- 자연어 질문에 강함  

하지만 다음과 같은 한계도 존재한다.

- 정확한 키워드 매칭에 약함  
- 숫자, 코드, 고유명사 처리 취약  
- irrelevant 문서가 상위에 노출될 가능성  

즉, Dense Retrieval은 “의미는 맞지만 답은 아닌 문서”를 가져오는 경향이 있다.

---

## 3. BM25의 특징

BM25는 전통적인 키워드 기반 검색 방식이다. 문서 내 단어의 빈도와 역문서 빈도(IDF)를 기반으로 점수를 계산한다.

이 방식의 특징은 다음과 같다.

- 정확한 키워드 매칭에 강함  
- 숫자, 코드, 고유명사 처리에 유리  
- 검색 결과의 해석 가능성이 높음  

하지만 단점도 명확하다.

- 의미 기반 검색 불가능  
- 표현 방식이 다르면 검색 실패  
- 자연어 질문에 취약  

즉, BM25는 “정확히 같은 단어”가 있는 문서는 잘 찾지만, 의미적으로 유사한 문서는 놓칠 수 있다.

---

## 4. Hybrid Retrieval의 필요성

Dense Retrieval과 BM25는 서로 다른 강점을 가진다.

| 방식 | 강점 | 약점 |
|---|---|---|
| Dense Retrieval | 의미 기반 검색 | 키워드 매칭 약함 |
| BM25 | 키워드 매칭 정확 | 의미 기반 검색 불가 |

이 두 방식은 경쟁 관계가 아니라 상호 보완 관계에 있다.

예를 들어 다음과 같은 상황을 생각해볼 수 있다.

질문: “HTTP 403 오류 해결 방법”

Dense Retrieval은 “오류 해결 방법”과 관련된 일반적인 문서를 가져올 수 있다. BM25는 “HTTP 403”이 정확히 포함된 문서를 가져온다.

Hybrid Retrieval은 이 두 결과를 결합하여 더 안정적인 검색 결과를 만든다.

---

## 5. Hybrid Retrieval 구조

Hybrid Retrieval은 일반적으로 다음과 같은 구조를 가진다.

① Dense Retrieval 수행  
② BM25 Retrieval 수행  
③ 두 결과를 결합  
④ 최종 ranking 수행  

이때 중요한 것은 단순히 결과를 합치는 것이 아니라, 어떻게 결합할 것인가이다. 대표적인 방법은 다음과 같다.

- Score-based merging  
- Rank-based merging  
- RRF (Reciprocal Rank Fusion)  

---

## 6. RRF (Reciprocal Rank Fusion)

RRF는 Hybrid Retrieval에서 자주 사용되는 방식이다. 각 검색 결과의 순위를 기반으로 점수를 계산하여 결합한다.

RRF score = Σ (1 / (k + rank_i))

여기서 rank_i는 각 retrieval 방식에서의 순위를 의미한다. 이 방식의 장점은 다음과 같다.

- 서로 다른 scoring 체계를 통합 가능  
- 특정 방식에 과도하게 의존하지 않음  
- 안정적인 성능  

즉, Dense와 BM25 중 하나가 실패하더라도 다른 방식이 이를 보완할 수 있다.

---

## 7. Hybrid Retrieval의 한계

Hybrid Retrieval은 성능을 개선할 수 있지만, 몇 가지 고려할 점이 있다.

첫 번째는 연산 비용 증가이다. 두 가지 retrieval을 모두 수행하기 때문에 비용과 latency가 증가한다.

두 번째는 결합 방식의 복잡성이다. 단순 병합이 아니라 ranking 전략까지 포함되기 때문에 시스템 설계가 복잡해진다.

세 번째는 후처리 필요성이다. Hybrid Retrieval만으로는 irrelevant 문서를 완전히 제거할 수 없기 때문에, reranking이 함께 사용되는 경우가 많다.

---

## 8. 마무리

Hybrid Retrieval은 Dense Retrieval과 BM25의 장점을 결합하여 Retrieval 성능을 개선하는 접근이다.

Embedding 기반 검색은 의미를 잘 반영하지만, 키워드 기반 검색의 정확성을 대체할 수는 없다. 반대로 BM25는 정확한 매칭에는 강하지만 의미 기반 검색에는 한계가 있다.

이 두 방식을 함께 사용하는 것은 단순한 성능 개선이 아니라, 검색 문제를 서로 다른 관점에서 해결하는 전략이다.

결국 RAG 시스템에서 중요한 것은 하나의 방법을 최적화하는 것이 아니라, 서로 다른 방법을 어떻게 조합할 것인가이다.
---

#RAG #HybridRetrieval #BM25 #DenseRetrieval #RRF #SearchSystem #Retrieval #LLM #AI공부 #기술블로그