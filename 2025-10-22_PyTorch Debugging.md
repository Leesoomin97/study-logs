# 1. Pytorch와 디버깅의 정의

PyTorch는 동적 계산 그래프를 기반으로 한 딥러닝 프레임워크이다.  
파이토치는 Tensor 연산과 자동 미분 기능을 중심으로 모델을 구성하고 학습을 수행한다.  
그러나 자유도가 높은 만큼 에러 발생 가능성도 매우 크다.  

디버깅이란 코드의 논리적 오류나 런타임 오류를 찾아 수정하는 과정이다.  
PyTorch 디버깅은 주로 Tensor 차원 불일치, device 불일치, gradient 이상값, 메모리 부족과 같은 문제를 다룬다.  

따라서 에러 메시지를 읽고, 연산 그래프를 추적하고, 중간 결과를 점검하는 방법을 익히는 것이 중요하다.  

---

# 2. 에러 메시지 분석 (Traceback 읽는 법)

PyTorch의 대부분의 에러는 `RuntimeError` 형태로 출력된다.  
에러의 핵심은 마지막 줄이 아니라 **마지막 줄 바로 위 스택**에 있다.  

```
RuntimeError: The size of tensor a (128) must match the size of tensor b (256)
```

이 메시지는 두 tensor의 차원이 다르다는 뜻이다.  
이 경우 forward 과정 중간에 `print(tensor.shape)`를 추가해 실제 차원이 어디서 달라졌는지 추적하는 것이 기본 절차이다.  

---

# 3. autograd 기반 디버깅: `set_detect_anomaly(True)`

PyTorch는 자동 미분 기능을 제공하지만, gradient 계산 중 오류가 발생하면 원인을 찾기 어렵다.  
이때 다음 설정을 통해 문제 지점을 추적할 수 있다.  

```python
torch.autograd.set_detect_anomaly(True)
loss.backward()
```

이 옵션은 backward 과정에서 비정상적인 연산을 감지하면 해당 연산 스택을 출력한다.  
다만 속도가 느려지므로 디버깅 단계에서만 사용하는 것이 좋다.  

---

# 4. 단계별 코드 중단: `breakpoint()`와 `pdb`

PyTorch 코드 역시 일반 파이썬 코드와 동일하게 디버거를 사용할 수 있다.  
가장 간단한 방법은 `breakpoint()`를 사용하는 것이다.  

```python
def forward(self, x):
    breakpoint()
    return self.fc(x)
```

코드 실행이 멈춘 상태에서 지역 변수, 텐서 값, shape 등을 직접 확인할 수 있다.  
`ipdb`를 설치하면 인터랙티브 환경에서 보다 편리하게 탐색할 수 있다.  

---

# 5. 연산 그래프 추적: `grad_fn`과 `torchviz`

각 텐서에는 `grad_fn` 속성이 존재한다.  
이는 해당 텐서가 어떤 연산의 결과로 만들어졌는지 나타내며, 연산 그래프를 역추적하는데 유용하다.  

```python
print(loss.grad_fn)
```

보다 시각적으로 확인하고 싶다면 `torchviz` 패키지를 사용할 수 있다.  

```python
from torchviz import make_dot
make_dot(loss)
```

이 방법은 복잡한 모델에서 gradient가 어디서 잘리는지 확인할 때 특히 유용하다.  

---

# 6. GPU 관련 에러의 원인과 해결

PyTorch는 GPU를 직접 제어하므로 device 불일치나 메모리 부족 오류가 자주 발생한다.  
대표적인 에러는 다음과 같다.  

**(1) CUDA out of memory**  
: 배치 크기를 줄이거나 gradient accumulation을 적용한다.  

**(2) Expected all tensors to be on the same device**  
: `.to(device)` 또는 `.cuda()` 호출 누락으로 발생한다.  
: GPU/CPU 혼용을 피하고, 모델과 입력 데이터를 동일한 device로 맞춘다.  

**(3) 비추천된 CUDA 호출**  
: `.cuda()` 대신 `.to(device)`를 사용하는 것이 유지 보수에 안전하다.  

---

# 7. 디버깅 루틴 정리

PyTorch 디버깅은 결국 '문제의 위치를 좁히는 과정'이다.  
모델 전체를 의심하기보다는 단계별 확인 루틴을 갖추는 것이 효율적이다.  

| 단계 | 점검 항목 | 주요 방법 |
|------|------------|------------|
| 1 | 에러 유형 확인 | RuntimeError 메시지 분석 |
| 2 | 텐서 차원 점검 | `print(tensor.shape)` |
| 3 | gradient 오류 확인 | `set_detect_anomaly(True)` |
| 4 | 중간 연산 중단 | `breakpoint()` / `pdb` |
| 5 | 그래프 추적 | `grad_fn`, `torchviz` |
| 6 | GPU 자원 점검 | `.to(device)` 일관성 유지 |

이 루틴을 정리해두면, 모델이 제대로 학습하지 않을 때 원인을 신속히 추적할 수 있다.  

---

# 8. 결론

PyTorch 디버깅은 에러를 해결하는 기술이 아니라 모델 동작을 이해하는 과정이다.  
에러 메시지를 읽고 연산 경로를 추적하고, 문제를 재현할 수 있는 습관을 가지면 대부분의 오류는 해결된다.  

디버깅은 단순한 버그 수정이 아니라, 모델의 작동 원리를 해석하는 과정이다.  
