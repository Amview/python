import json
import re
import requests

def main(page):
    url = 'https://www.km.com/piandan/1912.html?page='+str(page)
    html = request_dandan(url)
    items = parse_result(html)
    for item in items:
        write_item_to_file(item)

def request_dandan(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None

def parse_result(html):
    pattern = re.compile('div\sclass="m-t-n">.*?(\d+).*?</div>.*?div\s.*?class="m-t-t">.*?<a\shref="(.*?)"\starget="_blank">(.*?)</a>',re.S)
    # 符号 . 就 是匹配除 \n (换行符)以外的任意一个字符
    # 符号 * 前面的字符出现0次或以上
    # 符号. * 贪婪，匹配从. * 前面为开始到后面为结束的所有内容
    # 符号. *? 非贪婪，遇到开始和结束就进行截取，因此截取多次符合的结果，中间没有字符也会被截取
    # 符号(. *?) 非贪婪，与上面一样，只是与上面的相比多了一个括号，只保留括号的内容
    # 参数有re.S，不会对\n进行中断
    items = re.findall(pattern, html)
    for item in items:
        yield {
            '排序':item[0],
            '链接': item[1],
            'name': item[2]
        }

def write_item_to_file(item):
    print('开始写入' + str(item))
    with open('D:\\Desktop\\b.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')
        f.close()

if __name__ == "__main__":
    for i in range(1,20):
        main(i)
