import os
import subprocess
from datetime import datetime

FOLDER_HEADER = {
    ".": (
        "# 🗂️ Study Logs\n"
        "> 개인 학습 기록(TIL)과 기술 실험 노트들을 모아둔 공간입니다.\n"
        "> 실습 복기, 모델링 아이디어, 부트캠프 수업 회고 등을 Markdown 형태로 정리했습니다.\n"
    )
}

TARGET_DIRS = ["."]  # 루트 폴더만 갱신


def generate_index(folder):
    """루트 폴더 내 .md 파일을 인덱싱하고 README.md를 자동 생성"""
    files = [
        f for f in os.listdir(folder)
        if f.endswith(".md") and f != "README.md"
    ]
    files.sort(reverse=True)

    rows = ["| 날짜 | 제목 | 링크 |", "|------|------|------|"]

    for f in files:
        name = f.replace(".md", "")
        parts = name.split("_", 1)

        if len(parts[0]) == 10 and parts[0][4] == "-" and parts[0][7] == "-":
            date = parts[0]
            title = parts[1].replace("_", " ") if len(parts) > 1 else "(제목 없음)"
        else:
            date = datetime.today().strftime("%Y-%m-%d")
            title = name.replace("_", " ")

        # ✅ 루트에서는 그냥 파일명만 (./ 제거)
        file_path = f"{f}"
        rows.append(f"| {date} | {title} | [보기]({file_path}) |")

    header = FOLDER_HEADER.get(
        folder,
        "# 🗂️ Study Logs\n> 자동 생성된 목록입니다."
    )

    readme_content = f"""{header}
> 마지막 업데이트: {datetime.now().strftime("%Y-%m-%d")}

{chr(10).join(rows)}
"""

    with open(os.path.join(folder, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_content)

    print(f"✅ {folder or '.'}/README.md 갱신 완료 ({len(files)}개 파일)")


if __name__ == "__main__":
    for folder in TARGET_DIRS:
        if os.path.exists(folder):
            generate_index(folder)
        else:
            print(f"⚠️ {folder} 폴더가 존재하지 않습니다.")

    subprocess.run(["git", "add", "."], check=False)
    subprocess.run(["git", "commit", "-m", "Auto-update README index"], check=False)
    subprocess.run(["git", "push", "origin", "main"], check=False)
