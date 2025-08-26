
<머리말>

어제는 데이터 분석 과정에 대해 배웠다. Data analysis Process가 왜인지 익숙하게 느껴지는 단어라면, Data Readiness Check & Sampling은 어쩐지 생소하게 느껴지는 단어이다. 따라서 머신러닝 기초 개념 중 하나인 Data Readiness Check & Sampling에 대하여 보다 자세히 알고 적용하는 것을 목적으로 정리해보고자 한다.


<기초 지식>

1. 데이터 전처리 과정
: Data info check라고도 한다. 이는 수집된 데이터의 기본 정보들을 확인하는 과정이다.
: Data를 Road하고 데이터의 형태, 타입, 기간 등 전반적인 기본 정보를 파악하는 단계이다.

2. Data Readiness Check
: 데이터 수준 사전 점검 과정으로, 현재 가지고 있는 데이터의 수준으로 문제 해결이 가능한 지 점검하는 것이다.
: 순서대로 Targer label 생성, Targer Ratio 생성, 분석 방향성 결정 순으로 진행된다.

3. Data Sampling
(1) Sampling 수행 여부 결정
: Sampling을 진행하면 효과적으로 데이터 분석 및 모델링을 진행할 수 있다.(데이터 Nart 생성시간 단축, 모델 학습 시간 단축)
: 현재 데이터의 상황에 맞는 Sampling 기법을 선정하고 Sampling을 수행한다.
(2) Data 종류
-Time series data: upsampling(주기를 변경할 때, 결측값 채우기), down-sampling(time window 기준 mean(), max(), min())
-Non-time series data:
: Target data가 너무 적다면(Class-Imbalanced) -> Over-sampling
: Data가 너무 많다면 Under-sampling (Under-sampling시 Stratified sampling(층화추출) 진행)


<본론>

1.데이터 전처리 과정
(1) Data shape(형태) 확인
(2) Data type 확인
(3) Null값 확인
(4) 중복 데이터 확인
(5) Outlier 확인(정상 범주를 벗어난 데이터, 매우 중요한 과정!)

2. Data Readiness Check 과정
(1) Target label 생성
: 당월 구매 고객이 다음달 재구매 시 해당 고객을 재구개 고객으로 정의(타겟 정의)
(2) Target Ratio 확인
: 1번 단계에서 생성한 Target Ratio의 수준을 확인하고, 문제해결이 가능한 수준인지 판단
(3) 분석 방향성 결정
: 1,2번 단계를 종합하여 분석 방향성 결정
: ex. Targer Ratio가 낮다면 전체고객이 아닌, 특정 Segmentation 그룹으로 진행
: ex. +1N 구매 타겟은 +2M/+3M까지 확대하여 Target Ratio를 상승

3. Data Sampling 과정
(1) Over-sampling
: 대표적 기법으로는 SOMTE(Synthetic Minority Over-Sampling Technique)가 있음
: 낮은 비율로 존재하는 클래스의 데이터를 최근접 이웃 알고리즘을 활용하여 새롭게 생성하는 방법

(2)Under-Sampling & Stratified sampling (층화추출)
-층화추출: 모집단을 동질적인 소집단들로 층화시키고 그 집단의 크기에 따라 단순무작위표본추출한 방법
-비례층화추출: 특정 층의 모집단의 비율과 비례해서 표본을 선정하는 방법
-장점: 단순명의 추출보다 신뢰성이 높은 추정치를 구할 수 있음
: 비용 절감 및 자료분석이 용이함
: 각 층에 대한 추정치를 부수적으로 구할 수 있음
-단점: 방대한 모집단의 경우 목록작성의 어려움
: 적절하게 줄을 나누기 위해서는 모집단 각 층에 대한 정확한 정보를 필요

<마무리>

빅데이터분석기사 필기를 공부할 때 up-sampling과 down-sampling에 대해 이론적 개념을 배우긴 했었지만 실제로 프로그램에 적용하여 활용하는 방법에 대해서는 추상적인 상태였다. 이번 수업을 통해 데이터 분석 과정에서 어떻게 코딩을 짜서 분석하는지 알 수 있어서 머리에서 불명확했던 개념이 좀더 명확해진 것 같다. 아직 많이 어려운 감이 있지만 다음 머신러닝 경진대회에서도 직접 잘 활용할 수 있으면 좋겠다.

출처: 패스트캠퍼스 온라인강의
#패스트캠퍼스 #패스트캠퍼스AI부트캠프 #업스테이지패스트캠퍼스 #UpstageAILab #국비지원 #패스트캠퍼스업스테이지에이아이랩 #패스트캠퍼스업스테이지부트캠프
﻿
