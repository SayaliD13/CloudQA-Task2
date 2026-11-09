import json
from pathlib import Path
from datetime import datetime


def save_report(result):
    folder = Path("reports")
    folder.mkdir(exist_ok=True)

    file_name = "report_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".json"
    file_path = folder / file_name

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(result, file, indent=4, ensure_ascii=False)

    return str(file_path)
