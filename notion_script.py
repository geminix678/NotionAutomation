import os
import requests

# Lấy giá trị từ biến môi trường
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
DATABASE_ID = os.getenv("DATABASE_ID")

# Headers yêu cầu API
headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def get_database_items():
    """ Lấy tất cả các item trong database Notion """
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    response = requests.post(url, headers=headers)

    if response.status_code == 200:
        return response.json()["results"]
    else:
        print(f"❌ Lỗi khi lấy dữ liệu: {response.status_code} - {response.text}")
        return []

def update_page_checkbox(page_id, completed_value):
    """ Cập nhật giá trị checkbox của cột 'Completed' """
    url = f"https://api.notion.com/v1/pages/{page_id}"
    data = {
        "properties": {
            "Completed": {
                "checkbox": completed_value  # False = uncheck
            }
        }
    }

    response = requests.patch(url, headers=headers, json=data)

    if response.status_code == 200:
        print(f"✅ Cập nhật thành công cho Page ID: {page_id}")
    else:
        print(f"❌ Lỗi khi cập nhật Page ID {page_id}: {response.status_code} - {response.text}")

def process_notion_database():
    """ Kiểm tra điều kiện DailyTask == 'Yes' để uncheck Completed """
    items = get_database_items()

    for item in items:
        page_id = item["id"]
        properties = item["properties"]

        # Lấy giá trị từ cột "DailyTask" và "Completed"
        daily_task = properties.get("DailyTask", {}).get("select", {}).get("name", "")
        completed_status = properties.get("Completed", {}).get("checkbox", False)

        # Kiểm tra nếu "DailyTask" là "Yes" thì mới uncheck "Completed"
        if daily_task == "Yes" and completed_status:
            print(f"🔄 Unchecking 'Completed' for Page ID: {page_id}")
            update_page_checkbox(page_id, False)
        else:
            print(f"✅ Bỏ qua Page ID: {page_id} (DailyTask: {daily_task}, Completed: {completed_status})")

if __name__ == "__main__":
    process_notion_database()
