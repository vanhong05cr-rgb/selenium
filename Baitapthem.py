from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# ======================================================
# BƯỚC 1: KHỞI TẠO VÀ CHUẨN BỊ
# ======================================================
data_list = [] # List chứa kết quả cuối cùng
driver = webdriver.Chrome()

# Trang danh sách các trường ĐH tại Việt Nam
url_goc = "https://vi.wikipedia.org/wiki/Danh_s%C3%A1ch_tr%C6%B0%E1%BB%9Dng_%C4%91%E1%BA%A1i_h%E1%BB%8Dc_t%E1%BA%A1i_Vi%E1%BB%87t_Nam"

print("--- ĐANG THU THẬP LINK CÁC TRƯỜNG ---")
driver.get(url_goc)

# ======================================================
# BƯỚC 2: LẤY LINK TỪNG TRƯỜNG (GIAI ĐOẠN 1)
# ======================================================
# Các trường ĐH thường nằm trong bảng có class là 'wikitable'
# Chúng ta lấy tất cả thẻ 'a' (link) nằm trong bảng đó
try:
    # Chờ bảng hiện ra
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "wikitable")))
    
    # Lấy các thẻ <a> nằm trong cột tên trường (thường là td)
    elements = driver.find_elements(By.CSS_SELECTOR, "table.wikitable td a")
    
    uni_links = []
    for e in elements:
        link = e.get_attribute("href")
        title = e.get_attribute("title")
        
        # LỌC LINK RÁC:
        # 1. Phải có link
        # 2. Link phải chứa "/wiki/"
        # 3. Loại bỏ các link đỏ (trang chưa viết) thường chứa "redlink=1"
        if link and "/wiki/" in link and "redlink=1" not in link:
            uni_links.append(link)
    
    # Khử trùng lặp
    uni_links = list(set(uni_links))
    print(f"-> Tìm thấy {len(uni_links)} trường đại học.")

except Exception as e:
    print("Lỗi khi lấy danh sách:", e)
    uni_links = []

# ======================================================
# BƯỚC 3: TRUY CẬP TỪNG TRƯỜNG & LẤY DỮ LIỆU (GIAI ĐOẠN 2)
# ======================================================
count = 0
# --- CHẠY THỬ NGHIỆM 5 TRƯỜNG (Xóa dòng if break để chạy hết) ---
for link in uni_links:
    if count >= 5: 
        break
    count += 1
    
    print(f"[{count}] Đang cào: {link}")
    
    try:
        driver.get(link)
        # Không cần sleep lâu nếu mạng nhanh
        time.sleep(1) 
        
        # --- A. LẤY TÊN TRƯỜNG ---
        try:
            name = driver.find_element(By.TAG_NAME, "h1").text
        except:
            name = "Null"

        # --- B. XỬ LÝ INFOBOX (KHUNG THÔNG TIN BÊN PHẢI) ---
        # Đây là kỹ thuật quan trọng: Tìm theo từ khóa trong bảng
        
        # Mặc định là Null (Trống)
        hieu_truong = "Null"
        dia_chi = "Null"
        so_dien_thoai = "Null"

        try:
            # Tìm tất cả các dòng (tr) trong bảng thông tin (infobox)
            rows = driver.find_elements(By.CSS_SELECTOR, "table.infobox tr")
            
            for row in rows:
                text_row = row.text # Lấy toàn bộ chữ trong dòng đó
                
                # 1. Tìm Hiệu trưởng (Có thể ghi là Hiệu trưởng, Giám đốc, Viện trưởng...)
                # Logic: Nếu dòng đó có chữ "Hiệu trưởng" -> Lấy phần bên phải
                if "Hiệu trưởng" in text_row or "Giám đốc" in text_row:
                    # Cố gắng lấy thẻ td (cột giá trị)
                    try:
                        hieu_truong = row.find_element(By.TAG_NAME, "td").text
                    except:
                        pass
                
                # 2. Tìm Địa chỉ (Wiki thường ghi là "Địa chỉ" hoặc "Trụ sở")
                if "Địa chỉ" in text_row or "Trụ sở" in text_row:
                    try:
                        dia_chi = row.find_element(By.TAG_NAME, "td").text
                    except:
                        pass

                # 3. Tìm Số điện thoại (Thường ít trường ghi cái này trên Wiki)
                if "Điện thoại" in text_row:
                    try:
                        so_dien_thoai = row.find_element(By.TAG_NAME, "td").text
                    except:
                        pass

        except:
            # Nếu không có bảng infobox thì chịu, giữ nguyên Null
            pass

        # --- C. LƯU VÀO LIST ---
        uni_info = {
            'Tên Trường': name,
            'Hiệu Trưởng': hieu_truong,
            'Địa Chỉ': dia_chi,
            'Điện Thoại': so_dien_thoai,
            #'Link Wiki': link
        }
        data_list.append(uni_info)

    except Exception as e:
        print(f"Lỗi link {link}: {e}")

# ======================================================
# BƯỚC 4: XUẤT EXCEL
# ======================================================
driver.quit()

if data_list:
    df = pd.DataFrame(data_list)
    # Thay thế chữ "Null" bằng giá trị rỗng thật của Excel (nếu muốn)
    # df.replace("Null", "", inplace=True)
    
    file_name = 'DanhSachTruongDH.xlsx'
    df.to_excel(file_name, index=False)
    print("\n------------------------------------------------")
    print(f"XONG! Đã lưu dữ liệu vào file '{file_name}'")
    print(df.head())
else:
    print("Không lấy được dữ liệu nào.")