from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
import random
# options = webdriver.ChromeOptions()
# browser = webdriver.Chrome(options=options)
browser = webdriver.Chrome()
# browser.set_window_size(800,640)
# 打开数字石大并登录
browser.get("https://i.upc.edu.cn")
WebDriverWait(browser,30).until(EC.visibility_of_all_elements_located((By.ID,"index_login_btn")))
print("数字石大登录页面加载完成")
browser.find_element_by_id('un').send_keys("学号")
browser.find_element_by_id('pd').send_keys("数字石大密码")
browser.find_element_by_class_name("login_box_landing_btn").click()
# 等待加载
WebDriverWait(browser,30).until(EC.visibility_of_all_elements_located((By.CLASS_NAME,"profile_home_r_font01")))
print("数字石大登录完成，即将进入教务系统")
time.sleep(5)
# 进入教务系统
browser.get("https://i.upc.edu.cn/dcp/forward.action?path=dcp/core/appstore/menu/jsp/redirect&appid=1180&ac=0")
time.sleep(2)
print("教务系统加载完成")
# 进入学生评价
browser.get("http://jwxt.upc.edu.cn/jsxsd/xspj/xspj_find.do?Ves632DSdyV=NEW_XSD_JXPJ")
time.sleep(2)
print("学生评价页面加载完成")

# 找到所有评价项目
evaluations = browser.find_elements_by_xpath("//table[@class='Nsb_r_list Nsb_table']//a")
# 点击进入评价,注意此处分为实验课评教       理论课评教     体育课评教  请根据需要选择 0-2
evaluations[1].click()
time.sleep(2)
print("进入理论课评教，即将开始自动评教")
time.sleep(2)
# 记录所有课程
courses = browser.find_elements_by_xpath("//table[@class='Nsb_r_list Nsb_table']//a")
course_length = len(courses)
# 记录原页面handle
raw_handle = browser.current_window_handle
for i in range(course_length):

    if browser.current_window_handle != raw_handle:
        browser.switch_to.window(raw_handle)
    # 重新取一下试试
    courses = browser.find_elements_by_xpath("//table[@class='Nsb_r_list Nsb_table']//a")
    # 如果这个链接不是评价说明已经评价完成或者无法评价
    if courses[i].get_attribute("innerText") != "评价":
        continue
    courses[i].click()
    all_handles = browser.window_handles
    time.sleep(2)
    # 切换到弹出的页面
    if all_handles[0]==raw_handle:
        browser.switch_to.window(all_handles[1])
    else:
        browser.switch_to.window(all_handles[0])
    # 等待保存按钮出现
    WebDriverWait(browser, 30).until(EC.visibility_of_all_elements_located((By.ID, "bc")))
    time.sleep(2)
    # 随机取一项选择为满意，其它为非常满意  否则无法提交
    randomV = random.randint(0, 7)
    # 开始选择
    print("开始选择")
    for j in range(8):
        print("正在选择第" + str(i+1)+"项")
        if randomV == j:
            browser.find_element_by_id("pj0601id_" + str(j + 1) + "_2").click()
        else:
            browser.find_element_by_id("pj0601id_" + str(j + 1) + "_1").click()
    # 打分  需要先清除0，否则会变成 0xx
    print("开始打分")
    browser.find_element_by_id("pjbfb").clear()
    score = random.randint(90, 100)
    browser.find_element_by_id("pjbfb").send_keys(str(score))
    print("打分完成")
    browser.find_element_by_id("tj").click()
    dig_confirm = browser.switch_to.alert
    time.sleep(1)
    dig_confirm.accept()
    time.sleep(1)
    dig_alert = browser.switch_to.alert
    time.sleep(1)
    dig_alert.accept()
    print("课程"+str(i+1)+"提交完成,3秒后开始下一个")
    time.sleep(2)
    browser.switch_to.window(raw_handle)

print("理论课评价结束")



##------------以下为测试时使用 请忽略------------
# 控制一个已经打开的页面,或者说selenium控制和手动控制结合，开发阶段使用
# https://www.cnblogs.com/pythonywy/p/13805061.html
# C:\Program Files\Google\Chrome\Application
# chrome.exe --remote-debugging-port=5555 --user-data-dir="C:\selenum\setting"


# options = webdriver.ChromeOptions()
# options.debugger_address = "127.0.0.1:5555"
# driver = webdriver.Chrome(options=options)
# 进入教务系统
# driver.get("https://i.upc.edu.cn/dcp/forward.action?path=dcp/core/appstore/menu/jsp/redirect&appid=1180&ac=0")
# 进入学生评价
# driver.get("http://jwxt.upc.edu.cn/jsxsd/xspj/xspj_find.do?Ves632DSdyV=NEW_XSD_JXPJ")

# 找到所有评价项目
# evaluations = driver.find_elements_by_xpath("//table[@class='Nsb_r_list Nsb_table']//a")
# 点击进入评价n
# evaluations[1].click()
# 记录当前评价的URL
# v = driver.current_url
# print(v)



# time.sleep(2)
# courses = driver.find_elements_by_xpath("//table[@class='Nsb_r_list Nsb_table']//a")
# raw_handle = driver.current_window_handle
# courses[3].click()
# all_handles = driver.window_handles
# if all_handles[0]==raw_handle:
#     driver.switch_to.window(all_handles[1])
# else:
#     driver.switch_to.window(all_handles[0])
# # 等待保存按钮出现
# WebDriverWait(driver,30).until(EC.visibility_of_all_elements_located((By.ID,"bc")))
# time.sleep(2)
        # 决定不使用这种方式了
        # trs = driver.find_elements_by_xpath("//table[@id='table1']//tr")
        #  trs[0].get_attribute()

# id规律
# pj0601id_1_1 ~  pj0601id_8_4
# 对于pj0601id_x_y  x的取值范围是1~8,代表每一项评分， y的取值为[1,4]，代表是否满意,注意 x 的值并不和实际顺序一致

# 随机取一项选择为满意，否则无法保存
# randomV = random.randint(0,7)
# # 开始选择
# for i in range(8):
#     if randomV == i:
#         driver.find_element_by_id("pj0601id_" + str(i+1)+"_2").click()
#     else:
#         driver.find_element_by_id("pj0601id_" + str(i + 1) + "_1").click()

# 打分  需要先清除0，否则会变成 0xx
# driver.find_element_by_id("pjbfb").clear()
# score = random.randint(90,100)
# driver.find_element_by_id("pjbfb").send_keys(str(score))
# driver.find_element_by_id("tj").click()
# dig_confirm = driver.switch_to.alert
# time.sleep(1)
# dig_confirm.accept()
# time.sleep(1)
# dig_alert = driver.switch_to.alert
# time.sleep(1)
# dig_alert.accept()

