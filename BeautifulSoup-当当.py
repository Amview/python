import requests
from bs4 import BeautifulSoup
import xlwt
def main(page):
    url = 'https://movie.douban.com/top250?start=' + str(page * 25) + '&filter='
    html = request_douban(url)
    soup = BeautifulSoup(html, 'html.parser')
    save_to_excel(soup)
book=xlwt.Workbook(encoding='UTF-8',style_compression=0)
sheet=book.add_sheet('豆瓣电影top250',cell_overwrite_ok=True)
sheet.write(0, 0, '名称')
sheet.write(0, 1, '图片')
sheet.write(0, 2, '排名')
sheet.write(0, 3, '评分')
sheet.write(0, 4, '作者')
sheet.write(0, 5, '简介')

n=1
def save_to_excel(soup):
    list = soup.find(class_='grid_view').find_all('li')
    for item in list:
        item_name = item.find(class_='title').string
        item_img = item.find('a').find('img').get('src')
        item_index = item.find(class_='').string
        item_score = item.find(class_='rating_num').string
        item_author = item.find('p').text
        # item.intr = item.find(class_='inq').string
        print('电影：' + item_index + ' | ' + item_name + ' | ' + item_score + ' | '  + item_author)

        global  n
        sheet.write(n, 0, item_name)
        sheet.write(n, 1, item_img)
        sheet.write(n, 2, item_index)
        sheet.write(n, 3, item_score)
        sheet.write(n, 4, item_author)
        n=n+1

def request_douban(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None


if __name__ == "__main__":
    for i in range(1, 10):
        main(i)

book.save(u'豆瓣最受欢迎的250部电影.csv')
