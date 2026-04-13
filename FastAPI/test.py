import requests

headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1IiwidXNlcm5hbWUiOiJWaW5ueTMiLCJleHAiOjE3NzU0MjQ4MDh9.x1dd_BW7qIuk47cuONo-YFySvzfDPcATMbzq7AOiclw"}

response = requests.get("http://127.0.0.1:8000/auth/refresh", headers=headers)
print(response.status_code)
print(response.json())
