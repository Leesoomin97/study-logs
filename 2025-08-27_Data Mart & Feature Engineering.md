
<머리말>

지난 이틀동안 데이터 분석 과정 중 1, 2번째 절차인 기획, Readiness check&Sampling에 대해 알아보았다. 오늘은 3단계 절차인 Data Mart&Featuring Engineering에 대해 배워봄으로써 앞 단계에서 정리한 데이터들을 모델링하기 전 과정에 대해 알아보고자 한다.


<사전 지식>

-Data Mart란?
: 특정 부서나 주제 영역의 요구에 맞춰 데이터 웨어하우스에서 추출하고 정리한 데이터의 하위 집합을 말한다. 이는 데이터 웨어하우스보다 규모가 작고 특정 목적에 집중되어 있어, 사용자들은 더 빠르고 쉽게 필요한 데이터에 접근할 수 있다.(출처: 구글)

-Data Mart 진행 단계
: 이는 Data Mart 기획 및 설계, Data 추출 및 Mart 개발, Integer Feature Enginnering, Categoical Feature Engineering의 순서로 진행된다.


<본론> (인터넷 쇼핑 플랫폼 유입고객의 재구매율 향상 목적 데이터 분석 과정)

1. Data Mart 기획 및 설계
: Sampling 완료 후 월 별 기준이 되는 Customer ID를 추출하여 Mart를 구성하기 위한 준비를 모두 완료함
: 가설을 수립하고, 가설에 해당하는 다양한 변수 Category의 List를 생성함
: 풍부한 Data Mart를 기획해야 좋은 모델의 성능과 다양한 해석이 가능

2. Data 추출 및 Mart 개발
(1) Data Mart 기획서 데이터 추출
: 상위 단계에서 정의한 Date Mart를 기반으로 변수를 추출하는 내용
: 변수 추출은 Sampling한 Data로 선정
(2) Mart 개발 준비 및 Mart 추출 시작

3. Integer Feature Engineering
(1) Feature Engineering이란?
: 모델링의 목적인 성능향상을 위해 Feature을 생성, 선택, 가공하는 일련의 모든 활동

(2) Target 변수와의 의미있는 변수 선택하는 방법
-Regression(회귀): 상관계수 분석을 통해 유의미한 변수 선택
-Classification(분류): bin(통)으로 구분 후 Target 변수와의 관계 파악

(3) IV(Infomation Value)
: Feature 하나가 Good(Target)과 Bad(Non-target)을 잘 구분해줄 수 있는지에 대한 정보량을 표현하는 방법론
: IV 수치가 클수록 Target과 Non-target을 잘 구분할 수 있는 정보량이 많은 Feature이고, IV 수치가 작을수록 정보량이 적은 Feature이다.
: (Target data 구성비 - Non-target date 구성비) * WoE
: WoE(Weight of Evidence) = ln(Target data 구성비 / Non-target data 구성비)
: ln(자연로그)를 취하는 이유 = WoE의 최대, 최소값의 범위를 맞춰주기 위해서

4. Categoical Feature Engineering
(1) Target 변수와의 의미있는 변수 선택하는 방법
: 차원이 너무 많은 경우에는 차원을 Domain 지식을 활용하여 축소할 것
(2) Catplot
-Categorical Plot: 색상(hue)과 행(row)을 동시에 사용하여 3개 이상의 카테고리 값에 의한 변화를 그려볼 수 있음
-Categorical data를 파악하는데 용이함


<마무리>

지금까지 배워왔던 개념들보다 심화된 내용이어서 그런지 선생님의 수업을 듣는 것만으로는 이해하기 어려웠다. 무엇보다 여러가지의 카테고리를 동시에 다루면서 코딩의 길이가 늘어나 더욱 어렵게 느껴지는 것 같았다. 그렇기에 오늘 블로그 작성이 끝난 후 코랩으로 수업시간에 배웠던 내용을 하나하나 직접 작성해보는 시간을 가지는 것이 좋을 것 같다.


출처: 패스트캠퍼스 온라인 수업
#패스트캠퍼스 #패스트캠퍼스AI부트캠프 #업스테이지패스트캠퍼스 #UpstageAILab #국비지원 #패스트캠퍼스업스테이지에이아이랩 #패스트캠퍼스업스테이지부트캠프
﻿
