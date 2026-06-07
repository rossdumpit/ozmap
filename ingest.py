import requests


url = "https://myhospitalsapi.aihw.gov.au/api/v1/measure-downloads/myh-ed"

headers = {
    "accept": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "X-SWAGGER-UI": "true",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
    "Referer": "https://myhospitalsapi.aihw.gov.au/"
}



def extract():
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code}")


    content_type = response.headers.get("Content-Type", "")

    if "spreadsheet" not in content_type and "octet-stream" not in content_type:
        raise Exception(f"Not Excel: {content_type}")

    data = response.content

    with open("raw.xlsx", "wb") as f:
        f.write(data)

    return data, content_type

