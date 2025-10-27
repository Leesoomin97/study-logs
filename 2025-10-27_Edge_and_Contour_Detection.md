# Edge & Contour Detection — 이미지의 경계를 검출하는 방법

## 1. 머리말

이미지 처리의 핵심은 어디까지가 객체고, 어디부터 배경인가를 구분하는 것이다.

즉, 경계를 찾는 일(Edge Detection)과 윤곽을 정리하는 일(Contour Detection)은 이미지 분석의 출발점이라 할 수 있다.

이전 글 Morphological Transformation에서는 침식, 팽창과 같은 연산으로 노이즈를 제거하고 객체의 구조를 정제하는 전처리 방법을 다뤘다. 그 단계가 이미지 정제 과정이었다면, 이번 글은 그다음 단계인 형태 인식 단계이다.

정제된 이미지에서 어디까지가 경계인지(Edge)를 찾고, 그 경계를 따라 형태를 구조화(Contour) 하는 전 과정을 다룬다.

---

## 2. Edge Detection - 픽셀 단위의 경계 감지

### (1) 개념

에지(Edge)는 명암이나 색상이 급격히 변하는 부분을 의미한다. 이 변화는 보통 물체의 경계, 질감 변화, 그림자 경계 등에 해당한다. 컴퓨터는 밝기의 변화율(Gradient)을 수학적으로 계산해 경계를 감지한다.

경계를 검출하는 방법은 여러 가지가 있지만, OpenCV에서는 주로 Sobel, Laplacian, Canny 세 가지가 가장 널리 사용된다.

| 알고리즘 | 원리 | 특징 | 주요 활용 예시 |
|-----------|-------|--------|----------------|
| **Sobel** | 1차 미분 기반. x/y 방향의 경계 계산 | 수평/수직 방향성 분석에 유리. 노이즈에 비교적 강함 | 도로 차선, 텍스트, 기하학적 구조 |
| **Laplacian** | 2차 미분 기반. 방향성 없음 | 세밀한 텍스처나 점 구조 검출. 단, 잡음 민감. | 세포, 금속 표면, 재질 분석 |
| **Canny** | 다단계 검출(노이즈 제거 → Gradient 계산 → 비최대 억제 → Hysterisis Thresholding) | 경계 명확도와 안정성이 뛰어나 실무 표준. | 문서 스캔, 객체 분리, 결함 검출 |

---

### (2) 구현 코드

```python
import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('coins.jpg', 0)

# Sobel Edge
sobelx = cv2.Sobel(img, cv2.CP_64F, 1, 0, ksize=3)
sobely = cv2.Sobel(img, cv2.CP_64F, 0, 1, ksize=3)
sobel = cv2.magnitude(sobelx, sobely)

# Laplacian Edge
laplacian = cv2.Laplacian(img, cv2.CP_64F)

# Canny Edge
canny = cv2.Canny(img, 100, 200)

titles = ['Original', 'Sobel', 'Laplcian', 'Canny']
images = [img, sobel, laplacian, canny]

for i in range(4):
    plt.subplot(2,2,i+1)
    plt.imshow(images[i], cmap='gray')
    plt.title(titles[i])
    plt.axis('off')
plt.show()
```

위 결과를 보면

- Sobel은 수평/수직 방향 경계가 강조되어 구조적인 선을 잘 잡아낸다.  
- Lablacian은 모든 방향의 경계를 찾지만 잡음까지 함께 검출될 수 있다.  
- Canny는 불필요한 경계를 억제하고 깔끔한 윤곽선을 남긴다.  

그러므로 실무에서 사용될 때에는

- Sobel은 방향성 분석용으로 많이 활용되며, 특정 축의 변화만 보고 싶을 때 적합하다.  
- Laplacian은 미세 패턴 분석용으로 주로 활용되나, 잡음 문제로 블러(`cv2.GaussianBlur`)로 노이즈를 줄인 뒤 적용해야 한다.  
- Canny는 Contour 검출 전 단계로 가장 안정적이며, 문서, 객체 검출에 필수적이다.

---

## 3. Contour Detection - 윤곽선의 구조적 표현

### (1) 개념

Contour(윤곽선)는 Edge를 기반으로 연속된 픽셀 경계를 연결한 선이다. 즉, Edge가 변화가 발생하는 곳이라면 Contour는 그 변화가 그리는 전체적인 형태를 말한다.

Contour를 검출하면 객체의 크기, 모양, 위치를 수치로 분석할 수 있다. 이는 단순 시각화뿐 아니라 객체 인식(Object Detection), 세기(Counting), 치수 측정 등으로 확장된다.

---

### (2) 기본 절차

① 이미지를 이진화(`cv2.threshold` 또는 Canny 결과 사용)  
② `cv2.findContours()`로 윤곽선 검출  
③ `cv2.drawContours()`로 시각화  

```python
img = cv2.imread('shapes.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(img, contours, -1, (0, 255, 0), 2)
```

함수 옵션으로는 아래를 고려할 수 있다.

- `RETR_EXTERNAL`: 외곽 윤곽선만 탐색(속도 빠름)  
- `RETR_TREE`: 내부 윤곽까지 계층적으로 탐색  
- `CHAIN_APPROX_SIMPLE`: 선분을 단순화해 점 개수를 줄임  

---

### (3) Contour 속성 계산

윤곽선을 검출한 뒤, 각 객체의 면적, 중심, 외곽 사각형 등을 계산할 수 있다.  
이 정보는 '몇 개의 객체가 있는가'뿐 아니라 '크기 분포는 어떠한가'를 분석하는데 쓰인다.

| 항목 | 함수 | 설명 |
|------|------|------|
| 면적 | `cv2.contourArea()` | 객체의 크기 계산 |
| 둘레 | `cv2.arcLength()` | 윤곽선의 길이 |
| 외접 사각형 | `cv2.boundingRect()` | 위치 및 너비, 높이 추정 |
| 중심점 | `cv2.moments()` | 무게 중심 계산 |
| 볼록 껍질(convex hull) | `cv2.convexHull()` | 외곽선 단순화(결함 보정) |

```python
for cnt in contours:
    area = cv2.contourArea(cnt)
    peri = cv2.arcLength(cnt, True)
    x, y, w, h = cv2.boundingRect(cnt)
    M = cv2.moments(cnt)
    cx, cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
    cv2.circle(img, (cx, cy), 3, (255, 0, 0), -1)
```

*) `cv2.convexHull()`은 복잡한 외곽선을 단순화해 형태 인식의 안정성을 높여준다.

---

## 4. 실제 사용 사례

### (1) 문서 스캔 자동 경계 검출

```python
img = cv2.imread('document.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5,5), 0)
edges = cv2.Canny(gray, 50, 150)

contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
doc = max(contours, key=cv2.contourArea)

cv2.drawContours(img, [doc], -1, (0, 255, 0), 3)
```

- Canny를 사용해 불필요한 내부 선을 제거한 후, 문서의 외곽선만 남긴다.  
- 가장 큰 윤곽선(`max(contours, key=...)`)을 선택하면 문서 영역이 된다.  
- `cv2.approxPolyDP()`을 적용하면 정확히 4개의 모서리를 얻어 Perspective 보정까지 가능하다.

---

### (2) 객체 개수 세기 (Object Counting)

```python
img = cv2.imread('coins.jpg', 0)
blur = cv2.GaussianBlur(img, (5,5), 0)
edges = cv2.Canny(blur, 100, 200)

contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print("객체 개수:", len(contours))

areas = [cv2.contourArea(c) for c in contours]
print("평균 면적:", np.mean(areas))
```

- 각 동전의 윤곽선이 독립적으로 검출되므로, `len(contours)`로 개수를 셀 수 있다.  
- `contourArea` 값을 이용하면 객체 크기의 분포도 쉽게 확인 가능하다.

---

## 5. 마무리

| 구분 | 핵심 역할 | 주요 함수 | 특징 |
|------|------------|-----------|-------|
| **Edge Detection** | 픽셀 단위에서 경계 감지 | `cv2.Sobel`, `cv2.Laplacian`, `cv2.Canny` | 경계 후보를 빠르고 정확하게 추출 |
| **Contour Detection** | 객체 단위의 윤곽 구조화 | `cv2.findContours`, `cv2.drawContours` | 면적, 중심, 형태 분석 가능 |

Edge Detection은 이미지의 밝기 변화량(gradient)을 계산해 경계의 위치를 찾으며, Contour Detection은 그 경계를 연속된 윤곽선으로 연결해 객체의 형태를 표현한다.

이 두 과정은 이미지에서 구조를 이해하기 위한 전처리의 핵심 단계이며, 이후의 객체 인식(Object Detection) 및 영역 분할(Segmentation)로 확장된다.

그러므로 **Edge와 Contour Detection을 배울 때는**, 단순히 경계를 그리는 것에서 멈추지 말고,  
그 경계가 이후의 분석 단계(특징 추출, 분류, 인식)과 어떻게 연결되는지를 이해하는데 유의해야 한다.

---
