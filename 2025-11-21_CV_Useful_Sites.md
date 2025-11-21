1. 머리말

컴퓨터 비전(Computer Vision)을 학습할 때는 논문만 읽는 것으로는 부족하다.

보다 자세하게 공부를 하기 위해서는 실제 모델이 어떻게 작동하는지, 어떤 데이터셋을 기반으로 평가되는지, 최신 성능은 어디에서 확인할 수 있는지 등을 직접 보고 실험할 수 있는 도구가 필요하다.

많은 CV 강의에서는 다음과 같은 여러 사이트들을 활용하여 모델 구조, 데이터셋, 평가지표를 공부할 것을 추천한다.

이에 이 글에서는 CV 학습에 가장 자주 등장하는 대표 사이트들을 목적별로 정리하고자 한다.

2. COCO Dataset Explorer

(1) 링크: https://cocodataset.org/#explore

(2) 주요 기능
COCO 이미지, GT Annotation 시각화
BBox, Instance Mask, Keypoints를 실제 이미지와 함께 확인
클래스별 샘플 탐색
annotation 구조(JSON) 이해에 적합

(3) 실무 활용 포인트
Object Detection, Instance Segmentation이 어떻게 라벨링되는지 직접 확인
COCO의 annotation 포맷을 이해하면 대부분의 비전 데이터셋을 이해 가능
마스크가 어떤 방식으로 저장되는지와 같은 구조적 이해 필요시 활용

3. OpenCV 공식 문서

(1) 링크: https://docs.opencv.org/

(2) 주요 기능
Edge Detection, Contour Detection, Blur, Morphology 등 영상처리 기초 연산 설명
코드 예시 포함
각 연산의 수학적 정의 + OpenCV 함수 사용법 제공

(3) 실무 활용 포인트
Preprocessing 단계에서 사용하는 대부분의 이미지 처리 기법 검증
Sobel, Canny, GaussianBlur 등 구현 방식을 기술적으로 학습 가능
딥러닝 이전의 영상처리 기법을 정확하게 이해하는 데 도움

4. Roboflow Universe

(1) 링크: https://universe.roboflow.com/

(2) 주요 기능
Detection/Segmentation 데이터셋 브라우저 제공
Annotation 확인, Augmentation 시각화 제공
다양한 오픈 데이터셋 다운로드 및 변환 지원 (YOLO, COCO 등)

(3) 실무 활용 포인트
데이터셋 수집 - 가공 - 확인 전체를 UI로 확인 가능
바운딩 박스/마스크 구조를 직관적으로 확인
경량 모델, 프로토타입 단계의 실험에 적합

5. HuggingFace Spaces

(1) 링크: https://huggingface.co/spaces

(2) 주요 기능
최신 CV 모델 데모를 웹에서 즉시 실행
Segment Anything, YOLOv8, DETR, Mask2Former 등 실제 동작 확인
이미지 업로드 후 결과 시각화

(3) 실무 활용 포인트
논문에서 본 모델이 실제로 어떤 출력이 나오는지 즉시 확인 가능
Zero-shot Segmentation 등 최신 모델 실험
프로젝트 적합성 검토에 매우 유용

6. 정리

CV 학습을 하는 과정에 있어서 위 사이트들을 활용하면 모델 이해, 데이터셋 구조 확인, 최신 모델 실험이 모두 빠르게 가능해진다.

COCO Explorer - 정답 구조/Annotation 포맷 이해
OpenCV Docs - 영상처리 기반 원리 학습
Roboflow - 실제 데이터셋 구조, Annotation 확인
HuggingFace Spaces - 최신 모델 즉시 실행

이 사이트들에 익숙해지면 모델 구조 이해 속도가 한층 더 빨라지고, 프로젝트와 연구에 적합한 모델 선택 역시 훨씬 쉬워질 것이다.
