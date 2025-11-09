# Object Detection의 기본 개념과 동작 원리

## 1. 머리말

Convolutional Neural Network(CNN)은 이미지 내 무엇(what)을 분류함에 있어 탁월한 성능을 보여왔다. 하지만 실제 비전 과제에서는 무엇이 있는가만으로는 부족하다.

자율주행 차량, CCTV, 의료 영상 진단 등 대부분의 응용에서는 객체가 어디에 있는가(where)를 함께 인식해야 하며, 이 문제를 해결하기 위해 등장한 기술을 Object Detection(객체 탐지)라고 한다.

탐지란 단순히 클래스를 예측하는 분류(classification) 문제를 의미할 뿐만 아니라 위치 정보(Spatial Localization)를 추가로 학습하는 문제로도 확장된다.

이 글에서는 Object Detection의 핵심 개념과 해당 모델이 학습을 수행하는 기술적 과정을 단계적으로 살펴보고자 한다.

---

## 2. Object Detection의 문제 정의

일반적인 CNN 분류(Classification)는 한 장의 이미지에 대하여 하나의 클래스(Label)만을 예측한다. 즉, 분석하는 이미지가 고양이인가, 개인가의 여부만을 판단하는 문제이다.

하지만 Object Detection은 이미지 안의 여러 객체를 찾아내는 것을 목표로 한다. 따라서 모델은 각 객체의 클래스(Class) 뿐만 아니라, 화면 내 좌표(Bounding Box)까지 예측해야 한다.

즉, 탐지는 두 가지 예측을 동시에 수행한다.

- 분류(Classification): 객체의 종류를 판단
- 회귀(Regression): 객체의 위치(x, y, w, h)를 예측

이 구조는 단일 출력 네트워크가 아니라 두 개의 목적함수(Classification Loss + Regression Loss)를 병렬로 최소화하는 형태로 설계된다.

해당 개념은 이후 등장하는 Faster R-CNN, YOLO, SSD의 근간이 된다.

---

## 3. Object Detection의 구성 요소

객체 탐지는 기본적으로 세 단계로 이루어진다.

### (1) Feature Extraction - CNN을 통한 특징 추출

탐지는 CNN의 Feature Map을 기반으로 수행된다. 입력 이미지를 합성곱(Convolution) 연산을 통해 통과시키면 모델은 각 픽셀 주변의 형태, 질감, 윤곽선 등을 수치화하여 다층의 Feature Map으로 표현한다.

- 저층(early layer): 경계선, 색상, 패턴 등 저수준 특징  
- 고층(late layer): 객체 형태, 구조 등 고수준 특징

이 Feature Map은 이후 Bounding Box와 클래스 예측의 핵심 입력이 된다.

### (2) Bounding Box Prediction - 위치와 클래스 동시 예측

이 단계에서 모델은 Feature Map 상에서 객체의 위치를 나타내는 Bounding Box와 객체의 클래스를 동시에 예측한다.

#### Bounding Box의 표현 방식

객체 위치는 일반적으로 네 개의 좌표로 표현된다.  
모델은 이 좌표를 실제 정답 박스(Ground Truth)와 비교하며 회귀 손실(Regression Loss)을 통해 오차를 최소화한다.  
여기에는 Smooth L1 Loss 또는 IoU 기반 손실(GIoU, CIoU) 등이 사용된다.

#### 분류(Classification)

Bounding Box마다 클래스 확률을 예측한다.  
Softmax 또는 Sigmoid 함수를 통해 다중 클래스 확률을 계산하며,  
이 손실은 Cross-Entropy Loss 형태로 학습된다.

### (3) Post-Processing - 중복 제거 및 결과 정제

탐지 모델은 종종 하나의 객체에 대해 여러 박스를 동시에 예측한다. 이를 정제하기 위해 Non-Maximum Suppression(NMS) 알고리즘이 사용된다.

1. 모든 박스를 Confidence Score(신뢰도) 순으로 정렬  
2. 가장 높은 박스를 기준으로, IoU(Intersection over Union)가 일정 임계값(ex. 0.5) 이상인 박스를 제거  
3. 남은 박스만 최종 결과로 사용

IoU는 예측 박스와 정답 박스의 겹치는 비율을 의미하며, 탐지 정확도를 수치화하는 핵심 지표이다.  
IoU가 높을수록 예측이 정확하며, 일반적으로 IoU ≥ 0.5를 정탐(True Positive)으로 간주한다.

모델 전체 성능은 mAP(mean Average Precision)으로 평가한다.

---

## 4. Object Detection의 전체적 동작 흐름

탐지 모델의 내부 동작은 다음 6단계로 요약된다.

1. **Feature Extraction:** CNN을 통해 이미지에서 다층의 Feature Map 추출  
2. **Region Proposal:** 객체가 있을 가능성이 높은 영역 후보 생성 - (R-CNN은 Selective Search, Faster R-CNN은 RPN을 사용)  
3. **Bounding Box Regression:** 후보 영역 좌표를 실제 객체 중심으로 보정  
4. **Object Classification:** 각 영역에 대해 클래스 예측  
5. **NMS:** 중복 박스 제거, 최종 탐지 결과 선택  
6. **Output:** 객체별 Bounding Box와 라벨 출력  

이 과정은 모델 구조에 따라 Two-Stage(R-CNN 계열) 혹은 One-Stage(YOLO, SSD 계열)로 나뉜다.  

하지만 핵심 로직이 '특징 추출 - 위치 회귀 - 클래스 분류 - 중복 제거'의 순환이라는 점은 동일하다.

---

## 5. 마무리

Object Detection은 분류 문제를 공간 인식으로 확장한 결과물이다.  
즉, CNN이 단순히 무엇이 있는가를 분석한다면,  
Object Detection은 어디에 있는가까지 학습할 수 있도록 진화한 구조이다.

오늘은 객체 탐지의 기본 개념과 그 원리에 대해 살펴보았으니,  
다음에는 객체 탐지가 어떻게 구체적인 모델로 구현되었는지 기술적으로 분석해보고자 한다.

---
