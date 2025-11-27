from pygments.formatters.html import webify
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd 
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 1. Tai noi chua links va tao dataframe rong
all_links = []
d = pd.DataFrame({'name': [], 'birth': [], 'death': [], 'nationality': []})

# 2. Lay ra tat ca duong dan de truy cap den painters
# Khoi tao webdriver
for i in range (70,71):
    driver = webdriver.Chrome()
    # # Mo trang 
    # url = "https://en.wikipedia.org/wiki/List_of_painters_by_name_beginning_with_%22"+chr(i)+"%22"
    # try:
    #     driver.get(url)
    #     # Doi 2 giay
    #     time.sleep(3)
    #     # Lay ra tat cac ca the url
    #     ul_tags = driver.find_elements(By.TAG_NAME, "ul")
    #     print(len(ul_tags))
    #     # Chon the ul thu 21
    #     ul_painters = ul_tags[20] 
    #     # Lay ra tat ca the <li> thuoc ul_painters
    #     li_tags = ul_painters.find_elements(By.TAG_NAME, "li")
    #     # Tao danh sach cac url
    #     links = [tag.find_element(By.TAG_NAME, "a").get_attribute("href") for tag in li_tags]
    #     for x in links:
    #         all_links.append(x)
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
        all_links = [a.get_attribute("href") for a in anchors if a.get_attribute("href")]

        # # 3. Rut trich du lieu (List comprehension)
        # links = [a.get_attribute("href") for a in anchors]
        # # Chi lay title neu thuoc tinh do ton tai
        # titles = [a.get_attribute("title") for a in anchors if a.get_attribute("title")]

        print(f"--- Tim thay {len(all_links)} link hoa si ---")

        # # In ra URL
        # print("\n--- DANH SACH LINK ---")
        # for link in links:
        #     print(link)
    except:
        print("Error!")     
    # Dong webdriver
    driver.quit()   
    
# 3. Lay thong tin cua tung hoa si
count = 0;
for link in all_links:
    if (count > 3):
        break
    count = count + 1;
    print(link)
    try:
        # Khoi tao webdriver
        driver = webdriver.Chrome()
        # Mo trang 
        url = link
        driver.get(url)
        # Doi 2 giay
        time.sleep(2)
        # Lay ten hoa si
        try: 
            name = driver.find_element(By.TAG_NAME, "h1").text
        except:
            name = ""
        # Lay ngay sinh
        try:
            birth_element = driver.find_element(By.XPATH, "//th[text()='Born']/following-sibling::td")
            birth = birth_element.text
            birth = re.findall(r'[0-9]{1,2}+\s+[A-Za-z]+\s+[0-9]{4}', birth)[0]
        except:
            birth = ""
        # Lay ngay mat
        try:
            death_element = driver.find_element(By.XPATH, "//th[text()='Died']/following-sibling::td")
            death = death_element.text
            death = re.findall(r'[0-9]{1,2}+\s+[A-Za-z]+\s+[0-9]{4}', death)[0]
        except:
            death = ""
        # Lay ngay mat
        try:
            nationality_element = driver.find_element(By.XPATH, "//th[text()='Nationality']/following-sibling::td/")
            nationality = nationality_element.text
        except:
            nationality = ""
        # Tao dictionnary thong tin cua hoa si
        painter = {'name': name, 'birth': birth, 'death': death, 'nationality': nationality}
        # Chuyen doi dictionnary thanh DataFrame
        painter_df = pd.DataFrame([painter])
        # Them thing tin vao DF chinh
        d = pd.concat([d, painter_df], ignore_index = True)
        # Dong webdriver
        driver.quit()
    except:
        pass
# 4. In thong tin
print(d)
# Determining the name of the file
file_name = 'Painters.xlsx'
# Saving the excel
d.to_excel(file_name)
print('DataFrame is written to Excel File successfully.')