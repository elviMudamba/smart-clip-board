# import json
# import os

# HISTORY_FILE = "clipboard_history.json"

# def load_history():
#     if not os.path.exists(HISTORY_FILE):
#         return []
#     try:
#         with open(HISTORY_FILE, "r", encoding="utf-8") as f:
#             return json.load(f)
#     except json.JSONDecodeError:
#         return []

# def save_history(history):
#     with open(HISTORY_FILE, "w", encoding="utf-8") as f:
#         json.dump(history, f, ensure_ascii=False, indent=2)
