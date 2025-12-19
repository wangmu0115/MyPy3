import httpx

api_url = "https://bible-api.com/data/web/random"


def main():
    resp = httpx.get(api_url)
    print(resp)
    print(resp.status_code)
    print(resp.headers["content-type"])
    print(resp.text)


if __name__ == "__main__":
    main()
