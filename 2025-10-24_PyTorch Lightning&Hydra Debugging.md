#  PyTorch Lightning + Hydra Debugging


---

## 1. 개요

PyTorch Lightning은 PyTorch의 학습 루프를 모듈화하여 관리성을 높이는 프레임워크이다.  
이는 모델, 데이터, 옵티마이저, 학습 루프를 구조적으로 분리해 코드 가독성과 재현성을 개선한다.  
Hydra는 설정 파일을 계층적으로 관리하고, 다양한 하이퍼파라미터 조합을 자동 실험할 수 있게 해준다.  

이 두 도구를 함께 사용하면 모델의 실험 관리 효율이 높아지지만,  
코드 실행 경로가 추상화되어 디버깅 난이도는 오히려 올라간다.  
특히 학습이 '조용히 멈추거나', '정상 실행되지만 값이 틀린 경우' 같은 현상이 자주 발생한다.  

이 글은 이러한 Lightning/Hydra 환경에서 자주 마주치는 문제를 단계별로 진단하고 해결하는 절차를 공부하고 정리한 것이다.

---

## 2. Lightning/Hydra 환경에서 디버깅이 자주 필요한 이유

Lightning과 Hydra는 코드 구조를 깔끔하게 정리해주지만,  
이 추상화가 오히려 에러의 원인을 숨기는 방향으로 작동하기도 한다.  

디버깅이 필요한 주요 원인은 다음과 같다.  

### (1) 자동화된 학습 루프

Lightning은 내부적으로 `fit()`, `validate()`, `test()`를 자동 실행한다.  
그 과정에서 batch 전송, backward 호출, gradient clipping이 자동 수행되므로  
실제 에러가 어디서 발생했는지 직접 보기 어렵다.  

> **ex)** `RuntimeError: Expected all tensors to be on the same device`  
> → 코드에는 `.to(device)`가 있으나 Lightning의 내부 루프에서 CPU 텐서가 전달된 경우 발생한다.  

### (2) 설정 병합 충돌(Hydra)

YAML 설정이 중첩 병합될 때 동일 키가 덮어쓰여서 실제 적용된 값이 의도와 달라지는 경우가 많다.  

> **ex)** `train.yaml`과 `default.yaml`에서 둘 다 `batch_size` 선언 시,  
> 마지막에 호출된 config의 값이 최종 적용된다.  

### (3) 로그 및 체크포인트 경로 불일치

Hydra는 실행마다 별도 폴더(`outputs/2025-10-24/00-00-00/`)를 생성한다.  
반면 Lightning은 logger의 기본 경로를 별도로 관리한다.  
결과적으로 로그, 체크 포인트가 분리되어 TensorBoard가 실험을 통합 인식하지 못한다.  

### (4) 분산 학습 및 멀티 GPU 환경의 예외 처리

DDP 모드에서 통신 오류(`NCCL error`)나 초기화 deadlock이 발생할 수 있다.  
이런 오류는 traceback이 불완전하게 출력되어 디버깅 난이도가 높다.  

---

## 3. 디버깅 체크리스트(점검 루틴)

해당 표는 Lightning/Hydra 환경에서 문제가 발생했을 때  
우선적으로 확인해야 하는 항목과 즉시 실행 가능한 명령을 정리한 것이다.  

| 단계 | 점검 항목 | 즉시 실행 명령 / 방법 |
|------|------------|--------------------|
| 1 | 학습 루프 구조 | `pl.Trainer(fast_dev_run=True)` |
| 2 | 데이터 파이프라인 | `limit_train_batches=5`, `limit_val_batches=2` |
| 3 | 디바이스 일관성 | `accelerator="cpu"`, `devices=1`로 축소 테스트 |
| 4 | 설정 병합 결과 | `python train.py hydra.verbose=True` |
| 5 | 로그/출력 경로 | Logger `save_dir=cfg.output_dir` |
| 6 | 연산-그라디언트 오류 | `detect_anomaly=True` / `torch.autograd.set_detect_anomaly(True)` |
| 7 | 중간 값 추적 | `breakpoint()` 삽입 후 텐서 shape, loss 확인 |
| 8 | 분산 통신 문제 | `CUDA_LAUNCH_BLOCKING=1`, `NCCL_DEBUG=INFO` 환경변수 설정 |

문제 발생 시 위에 따라 **증상 범위를 좁히고 → 원인 구간을 특정**하는 것이 Lightning 디버깅의 핵심이다.  

---

## 4. Lightning의 빠른 구조 점검

Lightning은 `Trainer`를 통해 최소 루프 실행으로 오류를 확인할 수 있다.  

```python
trainer = pl.Trainer(
    fast_dev_run=True,  # 전체 학습을 단 한 번만 실행
    limit_train_batches=5,
    limit_val_batches=2
)
```

이 설정은 데이터로더, 모델, 손실 계산이 정상적으로 연결되어 있는지 빠르게 검증한다.  
특히 데이터셋에서 transform, collate_fn, GPU 전송 관련 오류가 이 단계에서 가장 많이 발생한다.  

또한 `fast_dev_run` 실행 후 바로 터지지 않더라도,  
학습 로그(`train_loss`, `val_loss`)가 모두 0 또는 NaN이면 데이터 파이프라인을 우선 의심해야 한다.  

---

## 5. 모델 내부 디버깅(forward, training_step)

Lightning에서는 `forward()`가 순전파만 담당하고,  
`training_step()`이 손실 계산 및 backward 호출을 담당한다.  

따라서 대부분의 오류는 `training_step()` 안에서 발생한다.  

```python
def training_step(self, batch, batch_idx):
    breakpoint()
    x, y = batch
    y_hat = self()
    loss = self.criterion(y_hat, y)
    print(f"[Debug] x: {x.shape}, y: {y.shape}, loss: {loss.iten():.4f}")
    self.log("train_loss", loss)
    return loss
```

- `breakpoint()`로 코드 실행을 일시 중단해 변수 상태를 직접 확인할 수 있다.  
- GPU 환경에서는 멀티 프로세스(`ddp`) 모드로 인해 디버거가 비활성화될 수 있으므로  
  반드시 `accelerator="cpu"` 또는 `devices=1`로 전환한 뒤 실행한다.  

> 실무에서 가장 흔한 패턴은 `y_hat`과 `y`의 차원 불일치이다.  
> → `RuntimeError: size mismatch, m1: [128 x 64], m2: [32 x 10]`  

이 경우 `print(tensor.shape)` 또는 위와 같이 로그를 남기는 것이  
Stack trace보다 빠른 해결책이 된다.  

---

## 6. Hydra 설정 충돌 진단

Hydra는 여러 YAML 파일을 병합하여 최종 설정을 생성한다.  
설정 중복이 있거나 상대경로가 잘못되면 다음과 같은 오류가 발생한다.  

```
hydra.errors.ConfigCompositionException:
Could not load configuration 'train': Config not found
```

문제 원인으로는  
- `@hydra.main()` 데코레이터에서 지정한 `config_path`가 실제 폴더 구조와 불일치하거나  
- `defaults` 리스트에 선언된 config가 존재하지 않거나 잘못된 이름을 사용하는 경우가 있다.  

진단 방법으로는 다음과 같다.  

1. 병합된 설정 경로와 값을 모두 출력한다.  
   ```bash
   python train.py hydra.verbose=true
   ```
2. 최종 적용된 설정을 확인한다.  
   ```bash
   python train.py +experiment=baseline print_config=true
   ```

같은 key가 여러 config에 존재할 경우 **마지막에 병합된 파일이 항상 우선한다.**  
따라서 의도한 설정 파일이 마지막에 오도록 `defaults` 순서를 조정해야 한다.  

---

## 7. 로그 및 체크포인트 경로 일관화

Hydra는 실행 시마다 고유 디렉토리를 생성한다.  
Lightning Logger의 저장 경로를 Hydra의 출력 경로로 통합하면 로그를 쉽게 관리할 수 있다.  

```python
@hydra.main(config_path="conf", config_name="config")
def main(cfg: DictConfig):
    logger = TensorBoardLogger(save_dir=cfg.output_dir, name="logs")
    trainer = pl.Trainer(logger=logger, ...)
```

이 방식은 `outputs/날짜-시간/` 디렉토리마다 로그를 자동 정리해주며,  
TensorBoard에서 실험별 비교가 한눈에 가능해진다.  

만약 W&B나 MLflow Logger를 사용하는 경우에도 `cfg.output_dir`을 상위 디렉토리로 지정하면  
실험 재현 시 로그 추적이 훨씬 쉬워진다.  

---

## 8. 분산 및 멀티 GPU 환경 디버깅

멀티 GPU 환경에서는 오류 재현이 어렵다.  
Lightning은 DDP 프로세스를 자동 관리하므로,  
문제가 발생하면 CPU 단일 환경으로 축소 후 동일 코드를 실행하는 것이 첫 단계이다.  

```python
trainer = pl.Trainer(
    accelerator="cpu",
    devices=1,
    detect_anomaly=True  # backward anomaly 감지
)
```

추가로 환경변수를 설정하면 디버깅 로그를 자세히 볼 수 있다.  

```bash
export CUDA_LAUNCH_BLOCKING=1
export NCCL_DEBUG=INFO
```

- **CUDA_LAUNCH_BLOCKING=1**: CUDA 커널을 동기 실행하여 에러 발생 지점을 명확히 한다.  
- **NCCL_DEBUG=INFO**: 프로세스 통신 로그를 출력하여 deadlock 여부를 확인한다.  

이 밖에도 자주 등장하는 에러로는  
1. `RuntimeError: CUDA out of memory` → 배치 크기 축소, `gradient_accumulation_steps` 적용  
2. `RuntimeError: NCCL communicator was aborted` → GPU 개수/통신 포트 불일치  
3. `Segmentation fault (core dumped)` → PyTorch 버전과 CUDA 드라이버 호환성 문제  

---

## 9. 결론

Lightning과 Hydra는 대규모 실험 관리에 강력하지만,  
내부 동작이 추상화되어 문제 발생 원인을 직접 파악하기 어렵다.  

이에 Lightning 디버깅은 학습 루프 단위로 문제를 좁혀가면서,  
Hydra 디버깅은 최종 config와 경로를 명시적으로 확인하면서,  
**CPU 단일 실행 → anomaly 탐지 → 경로 확인 → 분산 테스트** 순서로 진행한다.  

결과적으로 Lightning/Hydra 디버깅은  
자동화된 코드 흐름 속에서 통제권을 회수하는 과정이다.  
