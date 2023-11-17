from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
import time


# Đoạn code giúp browser ko bị tắt ngay khi mở
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))

# Truy cập trang web
driver.get("https://www.foody.vn/ho-chi-minh")

# --- Đăng nhập Foody ---
# Tìm phần tử "Đăng nhập" bằng class name
time.sleep
login_button = driver.find_element(By.CLASS_NAME, 'fd-btn-login-new')

# Click vào nút "Đăng nhập"
login_button.click()

# --- Nhập thông tin ---
# Email
time.sleep(2)
email_input = driver.find_element(By.ID, 'Email')
email_input.send_keys('quochuybh0404@gmail.com')

# Password
time.sleep(2)
password_input = driver.find_element(By.ID, 'Password')
password_input.send_keys('quochuy441996')


time.sleep(2)
login_button = driver.find_element(By.ID,'bt_submit')
login_button.click()

# Tạo danh sách link rỗng để cập nhật link vào trang web
list_links =[]

# --- Scroll để hiển thị các sản phẩm, hiển thị nút xem thêm và cập nhật link vào list_links ---
for _ in range(9):
    # Cuộn trang xuống
    driver.execute_script("window.scrollBy(0, 800);")  # Điều chỉnh giá trị 1000 tùy theo trang web
    
    # Chờ một khoảng thời gian trước khi cuộn tiếp (tùy chỉnh thời gian)
    time.sleep(3)

# --- Lấy link quán để chuyển tới trang quán đó trên foody ---
a_elements = driver.find_elements(By.XPATH, '//a[@class="ng-binding"]')
for i in range(0,len(a_elements),2):
    link = a_elements[i].get_attribute("href")
    list_links.append(link)


    
product_elements = driver.find_elements(By.CLASS_NAME,'title.fd-text-ellip')
number_product_elements = len(product_elements)
while True:
    try:
        load_more_button = driver.find_element(By.CLASS_NAME, 'fd-btn-more')
        load_more_button.click()
        time.sleep(2)    
        product_elements = driver.find_elements(By.CLASS_NAME,'title.fd-text-ellip')
        a_elements = driver.find_elements(By.XPATH, '//a[@class="ng-binding"]')
        for i in range(number_product_elements*2, len(a_elements),2):
            link = a_elements[i].get_attribute("href")
            list_links.append(link)

        number_product_elements = len(product_elements)
    except NoSuchElementException:
        # Nếu không tìm thấy nút "Xem thêm" thì thoát khỏi vòng lặp
        break    
    


# --- Tạo danh sách rỗng để lấy số phần tử đưa vào danh sách ---
list_comments = []
list_ratings = []

# --- Lấy link quán để chuyển tới trang quán đó trên foody ---
for link in list_links:
    if (type(link) == str):
        time.sleep(2)
        driver.get(link)

        # Thực hiện việc đếm số phần tử, scroll để load thêm sản phẩm và click nút "xem thêm"
        time.sleep(2)
        description_elements = driver.find_elements(By.XPATH, '//*[@ng-bind-html="Model.Description"]')
        # Lấy tổng số comment
        list_tool_element = driver.find_element(By.CLASS_NAME, 'list-tool')
        total_comment_elements = list_tool_element.find_element(By.XPATH, './/li[@data-item-name="review"]//span[@class="fa fa-angle-right"]/preceding-sibling::span').text
        if len(total_comment_elements) >= 4:
            number_description_elements = 0
            while True:
                try:
                    # Lấy phần tử tại vị trí thứ len(description_elements)-1
                    target_description_elements = description_elements[len(description_elements)-1]

                    # Sử dụng JavaScript để cuộn đến vị trí của phần tử đó
                    driver.execute_script("arguments[0].scrollIntoView();", target_description_elements)

                    time.sleep(3)    
                    description_elements = driver.find_elements(By.XPATH, '//*[@ng-bind-html="Model.Description"]')
                    if number_description_elements != len(description_elements):
                        number_description_elements = len(description_elements)
                    else:
                        time.sleep(3)
                        load_more_button = driver.find_elements(By.XPATH, '//a[@class="fd-btn-more"]')[1]
                        load_more_button.click()
                except:
                    break

        else:
            if len(description_elements) <= 10 and int(total_comment_elements) <= 10:
                description_elements
            else: 
                number_description_elements = 0
                while True:
                    try:
                        # Lấy phần tử tại vị trí thứ len(description_elements)-1
                        target_description_elements = description_elements[len(description_elements)-1]

                        # Sử dụng JavaScript để cuộn đến vị trí của phần tử đó
                        driver.execute_script("arguments[0].scrollIntoView();", target_description_elements)

                        time.sleep(3)    
                        description_elements = driver.find_elements(By.XPATH, '//*[@ng-bind-html="Model.Description"]')
                        if number_description_elements != len(description_elements):
                            number_description_elements = len(description_elements)
                        else:
                            time.sleep(3)
                            load_more_button = driver.find_elements(By.XPATH, '//a[@class="fd-btn-more"]')[1]
                            load_more_button.click()
                    except:
                        break


        # Thực hiện lấy phần tử 
        time.sleep(2)
        description_elements = driver.find_elements(By.XPATH, '//*[@ng-bind-html="Model.Description"]')
        time.sleep(2)
        point_elements = driver.find_elements(By.CLASS_NAME, 'review-points')

        for description_element in description_elements:
            list_comments.append(description_element.text)

        for point_element  in point_elements:
            rating = point_element.find_element(By.TAG_NAME, 'span').text
            if rating != '':
                list_ratings.append(rating)

        # Thực hiện xong thì quay trang trước
        time.sleep(2)
        driver.back()

print(len(list_comments))
print(len(list_ratings))
dict_product = {
    'comments': list_comments,
    'ratings': list_ratings
    }

import csv
with open('crawl_data/Foody.csv', 'w', encoding = 'utf-8') as f:
    write = csv.writer(f)
    write.writerow(dict_product.keys())
    write.writerows(zip(*dict_product.values()))

