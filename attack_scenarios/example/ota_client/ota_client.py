import zipfile
import io
import os
from paho.mqtt.client import Client
from paho.mqtt.enums import CallbackAPIVersion
import requests

vehicle_id = "vehicle_1234"  # 차량 ID

def on_message(client, userdata, msg):
    try:
        file_name = msg.payload.decode()
        print(f"Update notice received: {file_name}")
        get_update_file(file_name)
    except Exception as e:
        print(f"Error processing message: {e}")

def mqtt_client(broker_address: str, port=1883, keepalive=60):
    try:
        client = Client(callback_api_version=CallbackAPIVersion.VERSION2)
        client.on_message = on_message
        client.username_pw_set("mose", "3103")
        client.connect(broker_address, port, keepalive)
        client.subscribe("ota/updates")
        client.loop_forever()
    except Exception as e:
        print(f"Error connecting to MQTT broker: {e}")

def get_update_file(update_file_name):
    # 서버의 URL
    try:
        url = f"http://write server ip or domain/get_update?update_file_name={update_file_name}"

        # HTTPS 요청 보내기
        response = requests.get(url, verify=False)  # 스트리밍 모드로 요청

        if response.status_code == 200:
            # ZIP 파일을 메모리에 로드
            zip_file = zipfile.ZipFile(io.BytesIO(response.content))
            
            # ZIP 파일의 내용을 추출
            zip_file.extractall(f"./{vehicle_id}_update_files")
            print(f"Update files extracted for {vehicle_id} in ./{vehicle_id}_update_files")
        else:
            print(f"Error: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    broker_address = "203.246.114.61"  # Replace with your MQTT broker address
    mqtt_client(broker_address=broker_address, port = 12010)
