# generate_study_log_index.py
import os
import subprocess
from datetime import datetime

# 각 폴더별 헤더 설명
FOLDER_HEADER = {
    "study-logs": (
        "# 🗂️ Study Logs\n"
        "> 개인 학습 기록(TIL)과 기술 실험 노트들을 모아둔 공간입니다.\n"
        "> 실습 복기, 모델링 아이디어, 부트캠프 수업 회고 등을 Markdown 형태로 정리했습니다.\n"
    ),
    "paper-notes": (
        "# 📖 Paper Notes\n"
        "> 논문, 강의, 아티클 등 심화 학습 내용을 요약·분석한 공간입니다.\n"
        "> 데이터 과학, 딥러닝, 추천시스템 관련 최신 리서치 정리를 포함합니다.\n"
    ),
}

# 자동으로 인덱스를 생성할 폴더들
TARGET_DIRS = ["."]


def generate_index(folder):
    """폴더 내 .md 파일을 인덱싱하고 README.md를 자동 생성"""
    files = [
        f for f in os.listdir(folder)
        if f.endswith(".md") and f != "README.md"
    ]
    files.sort(reverse=True)

    rows = ["| 날짜 | 제목 | 링크 |", "|------|------|------|"]

    for f in files:
        name = f.replace(".md", "")
        parts = name.split("_", 1)

        # 파일명에서 날짜 인식 or 오늘 날짜
        if len(parts[0]) == 10 and parts[0][4] == "-" and parts[0][7] == "-":
            date = parts[0]
            title = parts[1].replace("_", " ") if len(parts) > 1 else "(제목 없음)"
        else:
            date = datetime.today().strftime("%Y-%m-%d")
            title = name.replace("_", " ")

        # ✅ 상대경로 수정
        file_path = os.path.join(folder, f).replace("\\", "/")
        rows.append(f"| {date} | {title} | [보기]({file_path}) |")

    # 상단 설명문 가져오기
    header = FOLDER_HEADER.get(
        folder,
        f"# 🗂️ {folder.capitalize()}\n> 자동 생성된 목록입니다."
    )

    readme_content = f"""{header}
> 마지막 업데이트: {datetime.now().strftime("%Y-%m-%d")}

{chr(10).join(rows)}
"""

    with open(os.path.join(folder, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_content)

    print(f"✅ {folder}/README.md 갱신 완료 ({len(files)}개 파일)")


if __name__ == "__main__":
    for folder in TARGET_DIRS:
        if os.path.exists(folder):
            generate_index(folder)
        else:
            print(f"⚠️ {folder} 폴더가 존재하지 않습니다.")

    # 모든 변경사항 자동 푸시
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", "Auto-update README index"], check=False)
    subprocess.run(["git", "push", "origin", "main"], check=False)
