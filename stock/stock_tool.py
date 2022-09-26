import requests


def query_more_pages(startPages, totalPages, stockCode, orgId, searchkey='', startDate=None, endDate=None):
    for pageIndex in range(startPages, totalPages + 1):
        query_stock_announcements(pageIndex, stockCode, orgId, searchkey, startDate, endDate)


def query_stock_announcements(pageNum, stockCode, orgId, searchkey='', startDate=None, endDate=None, skipMorePage=True):
    url = r'http://www.cninfo.com.cn/new/hisAnnouncement/query'
    seDate = None
    if startDate and endDate:
        seDate = startDate + "~" + endDate
    # 定义表单数据
    data = {'pageNum': pageNum,
            'pageSize': 30,
            'column': 'sse',
            'tabName': 'fulltext',
            'plate': '',
            'stock': stockCode + ',' + orgId,
            'searchkey': searchkey + ';',
            'secid': '',
            'category': None,
            'trade': '',
            'seDate': seDate,
            'sortName': '',
            'sortType': '',
            'isHLtitle': 'true'}

    #   定义请求头
    headers = {'Accept': '*/*',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9',
               'Connection': 'keep-alive',
               'Content-Length': '181',
               'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
               'Host': 'www.cninfo.com.cn',
               'Origin': 'http://www.cninfo.com.cn',
               'Referer': 'http://www.cninfo.com.cn/new/commonUrl/pageOfSearch?url=disclosure/list/search',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
               'X-Requested-With': 'XMLHttpRequest'}

    response = requests.post(url, data=data, headers=headers)
    if response.status_code != 200:
        print("query data failed")
        return

    # 2.获取单页年报的数据，数据格式为json，解析并获取json中的年报信息
    response_obj = response.json();
    announcements = response_obj['announcements']
    totalPages = response_obj['totalpages']

    # totalPage 从0开始计数
    if totalPages >= 0:
        # 3.对数据信息进行提取
        recordIndex = 0
        for item in announcements:
            secCode = item['secCode']
            secName = item['secName']
            orgId = item['orgId']
            announcementTitle = item['announcementTitle']
            announcementId = item['announcementId']
            viewUrl = "http://www.cninfo.com.cn/new/disclosure/detail?plate=sse&orgId={}&stockCode={}&announcementId={}".format(
                orgId, stockCode, announcementId)
            print("{}/{}:{}\t{}\t{}\t{}\t{}".format(pageNum, recordIndex, secName, secCode, orgId, announcementTitle,
                                                    viewUrl))
            recordIndex = recordIndex + 1

        # 4 采集其他页数的数据
        if not skipMorePage and totalPages > 0:
            query_more_pages(2, totalPages + 1, stockCode, orgId, searchkey, startDate, endDate)
    else:
        print("No data for stock:{},keyWord:{}".format(stockCode, searchkey))


if __name__ == '__main__':
    # query_stock_announcements(1, '600499', 'gssh0600499', '薪酬', '2021-09-26', '2022-09-27', False)
    query_stock_announcements(1, '002340', '9900010252', '', '2022-06-27', '2022-09-27', False)
