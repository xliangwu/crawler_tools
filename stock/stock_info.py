import json
import requests


def download_stock_infos():
    url = r"http://www.cninfo.com.cn/new/data/szse_stock.json"
    response = requests.get(url=url)
    if response.status_code == 200:
        stock_content = response.content
        stock_list = json.loads(stock_content)["stockList"]
        print("download stock size:{}".format(len(stock_list)))

        with open("stock.json", "w", encoding='utf-8') as f:
            json.dump(response.json(),f, ensure_ascii=False)
            print("write stock content to file")


if __name__ == '__main__':
    download_stock_infos()
