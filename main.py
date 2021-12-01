from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import datetime
import csv
import re
import codecs

yesterday = str(datetime.date.today() + datetime.timedelta(-1))
today = str(datetime.date.today())
print(f"早安,今天是{today}\n爬取的日期为", yesterday, "and", today)
url = "http://my.bupt.edu.cn"
page = webdriver.Chrome()
page.get(url)
page.maximize_window()
# 登陆
page.find_element(By.XPATH, "//*[@id='username']").send_keys("2020212265")
page.find_element(By.XPATH, "//*[@id='password']").send_keys("03053913")
page.find_element(By.XPATH, "//*[@id='casLoginForm']/input[4]").click()

page.find_element(By.XPATH, "/html/body/div[1]/div/ul/li[5]/a").click()
page.find_element(By.XPATH, "/html/body/div[3]/div/div[1]/div[2]/ul/li[18]/a").click()

url = "http://my.bupt.edu.cn/list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1162"
res = []
for i in range(1, 21):
    target = page.find_element(By.XPATH, f"/html/body/div[3]/div/div[2]/ul/li[{i}]/a")
    target_date = page.find_element(By.XPATH, f"/html/body/div[3]/div/div[2]/ul/li[{i}]/span[2]")
    text = target_date.text
    if re.search("讲座", target.text, flags=0) is not None and (text == today or text == yesterday):
        n_url = target.get_attribute("href")
        temp_str = ""
        temp = ""
        page.get(n_url)
        content = page.find_elements(By.XPATH, "//*[@id='vsb_content']/div//*")
        for i1 in content:
            if i1.text != "":
                if temp != i1.text:
                    temp_str += i1.text + "\n"
                temp = i1.text
        if re.search("盖", temp_str, flags=0) is not None:
            title = page.find_element(By.XPATH, "/html/body/div[3]/div[2]/div[1]/form/div[1]/h1[1]")
            res.append((text, title.text + "\n" + n_url))
            print(f"可以盖章哦!快去看看吧{n_url}")
        page.get(url)
# /html/body/div[3]/div/div[2]/ul/li[7]/a /html/body/div[3]/div/div[2]/ul/li[20]/a
page.close()
if not res:
    print("今天还没有可以盖章的呢!过会再来吧!")
else:
    f = codecs.open(f'speech{today}.csv', 'w', 'gbk')
    writer = csv.writer(f)
    for i in res:
        writer.writerow(i)
    f.close()
# //*[@id="vsb_content"]/div/p[9]/span[1]/span
# //*[@id="vsb_content"]/div/p[13]/span
