# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time
# # Khoi tao Webdriver
# driver = webdriver.Chrome()
# # mo trang
# url = "https://en.wikipedia.org/wiki/List_of_painters_by_name_beginning_with_%22P%22"
# driver.get(url)
# # Doi 1 chut de tai trang
# time.sleep(3)
# # Lay ra tat cac ca the url
# ul_tags = driver.find_elements(By.TAG_NAME, "ul")
# print(len(ul_tags))
# # Chon the ul thu 21
# ul_painters = ul_tags[20] 
# # Lay ra tat ca the <li> thuoc ul_painters
# li_tags = ul_painters.find_elements(By.TAG_NAME, "li" )
# # Tao danh sach cac url
# links = [tag.find_element(By.TAG_NAME, "a").get_attribute("href") for tag in li_tags]
# # Tao danh sach cac url
# titles = [tag.find_element(By.TAG_NAME, "a").get_attribute("title") for tag in li_tags]
# # In ra url
# for link in links:
#     print(link)
# # In ra title
# for title in titles:
#     print(title)
# # Dong webdriver
# driver.quit()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 1. Thay doi tu Safari sang Chrome (Trinh duyet pho bien tren Windows)
driver = webdriver.Chrome()

# Mo trang web
driver.get("https://en.wikipedia.org/wiki/List_of_painters_by_name_beginning_with_%22P%22")

try:
    # 2. Su dung WebDriverWait nhu code mau ban gui
    # Doi toi da 10 giay de cac the <a> trong class .div-col xuat hien
    anchors = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "#mw-content-text .div-col li > a") 
        )
    )

    # 3. Rut trich du lieu (List comprehension)
    links = [a.get_attribute("href") for a in anchors]
    # Chi lay title neu thuoc tinh do ton tai
    titles = [a.get_attribute("title") for a in anchors if a.get_attribute("title")]

    print(f"--- Tim thay {len(links)} hoa si ---")

    # In ra URL
    print("\n--- DANH SACH LINK ---")
    for link in links:
        print(link)

    # In ra Ten (Title)
    print("\n--- DANH SACH TEN ---")
    for title in titles:
        print(title)

except Exception as e:
    print(f"Co loi xay ra: {e}")

finally:
    # Luon dong trinh duyet du co loi hay khong
    driver.quit()