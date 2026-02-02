import os
import requests
from datetime import datetime, timedelta, timezone

# 環境変数から設定を読み込み
NOTION_TOKEN = os.environ["NOTION_TOKEN"]
DATABASE_ID = os.environ["NOTION_DATABASE_ID"]

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def create_page():
    # 日本時間の今日の日付を取得
    jst = timezone(timedelta(hours=9))
    today = datetime.now(jst).strftime("%Y-%m-%d")
    
    url = "https://api.notion.com/v1/pages"
    
    data = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "名前": {  # データベースのタイトル項目の名前に合わせる
                "title": [{"text": {"content": f"{today}の日記"}}]
            },
            "日付": {  # データベースの日付項目の名前に合わせる
                "date": {"start": today}
            }
        },
        "children": [
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {"rich_text": [{"text": {"content": "今日のトピック"}}] }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": [{"text": {"content": ""}}] }
            }
        ]
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print(f"Successfully created: {today}")
    else:
        print(f"Error: {response.text}")

if __name__ == "__main__":
    create_page()
