import requests

foto = [
    "AC.0010-OBJECT_0058-R.jpeg",
    "AC.0010-OBJECT_0056-R.jpeg",
    "AC.0010-OBJECT_0055-R.jpeg",
    "AC.0010-OBJECT_0040-R.jpeg",
    "AC.0010-OBJECT_0039-R.jpeg",
    "AC.0010-OBJECT_0024-R.jpeg",
    "AC.0010-OBJECT_0010-R.jpeg",
]

for f in foto:
    url = f"https://hobnm0201.sat.co.id/api/v1/checklist/img/AC.0010/{f}"

    payload = {}
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInNlcnZpY2VfaWQiOiJrYW5nZ28iLCJ0eXAiOiJKV1QifQ.eyJleHAiOjE3MTg3MTkxMjcuOTg4NjksInRva2VuX2VudiI6InByb2QifQ.VuroflRbxIOFv1fGDq7_IM7chXl7hPwIPM94tWmjkkc"
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.status_code)
