서버 실행 (가짜 OTA 서버를 띄움)
``` terminal
cd attack_scenarios/Man-in-the-middle_attack/scenario_Proxy_Redirection/reference_code/server
python fake_ota_server.py
```
클라이언트 실행 (차량 모듈 시뮬레이션)
``` terminal
cd ../client
python vehicle_module.py
```
hosts 파일 설정 (Windows 예시: 관리자 권한으로 'hosts' 열기)
``` terminal
url = "http://127.0.0.1:8000/ota"
```
이렇게 하면 vehicle_module.py에서 http://127.0.0.1:8000/ota 요청 시, 내 로컬 서버(가짜 서버)로 연결됩니다.
