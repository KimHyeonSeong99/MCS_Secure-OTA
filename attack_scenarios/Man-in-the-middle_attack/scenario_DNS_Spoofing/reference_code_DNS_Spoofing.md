reference_code_DNS_Spoofing/
├── ota_client/ #OTA target vehicle
|   ├── certs/
|   |   ├── ota.crt
|   |   └── client.key
|   └── client_simulator.py
├── attacker/   #OTA attacker
|   ├── certs/
|   |   ├── ota.crt
|   |   └── attacker.key
|   ├── fake_app.py
|   ├── attacker.pub
|   ├── firmware.bin
|   ├── firmware.hash
|   ├── firmware.sig
|   └── client_simulator.py
├── server/     #OTA normal update server
|   ├── certs/
|   |   ├── ota.crt
|   |   └── server.key
|   ├── firmware.bin 
|   └── app.py
└── README.md
