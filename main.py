from bs4 import BeautifulSoup as bs
from datetime import datetime, timedelta
import requests


def parse_naver_weather(elements):  # 네이버날씨를 파싱하여 오전/오후의 기온을 반환하는 함수
    data = []
    for e in elements:
        inners = e.findAll("span", {"class": "weather_inner"})
        rainAM = inners[0].find("span", {"class": "rainfall"}).text
        rainPM = inners[1].find("span", {"class": "rainfall"}).text
        tempAM = e.find("span", {"class": "lowest"}).find(text=True, recursive=False)
        tempPM = e.find("span", {"class": "highest"}).find(text=True, recursive=False)
        foo = "%9s" % tempAM + "%9s" % rainAM + "%9s" % tempPM + "%9s" % rainPM
        data.append(foo)
    return data


def main():
    # 네이버 날씨를 크롤링합니다.
    html = requests.get(
        "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EC%A7%84%EC%A3%BC%EC%8B%9C+%EA%B8%88%EC%82%B0%EB%A9%B4+%EB%82%A0%EC%94%A8&oquery=%EC%A7%84%EC%A3%BC+%EB%82%A0%EC%94%A8&tqi=h9vXClprvOsssS4lLrZssssssjs-396297"
    )
    base_url = "https://m.search.naver.com/p/csearch/content/nqapirender.nhn?where=nexearch&pkid=227&u1=03170410&key=weather"

    url = base_url
    # urls = base_url

    r = requests.get(url)
    html = str(r.json()["weekly"])
    soup = bs(html, "html5lib")
    lis = soup.findAll("li")
    result = parse_naver_weather(lis)

    # 사용할 날짜를 구합니다(오늘 포함 총 7일).
    weeks = ["일", "월", "화", "수", "목", "금", "토"]
    dt = datetime.now().date()
    dates7 = [
        (dt + timedelta(days=i)).strftime("%m/%d")
        + "("
        + weeks[int((dt + timedelta(days=i)).strftime("%w"))]
        + ")"
        for i in range(7)
    ]

    print("%20s" % "오전" + "%16s" % "오후")
    print('%16s'%'기온'+'%7s'%'강수'+'%7s'%'기온'+'%7s'%'강수')
    for i in range(7):
        print(dates7[i] + result[i])


if __name__ == "__main__":
    main()
