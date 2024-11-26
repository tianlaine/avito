from selenium import webdriver

driver = webdriver.Chrome(executable_path='path_to_chromedriver')
driver.get('https://www.avito.ru')

ads_elements = driver.find_elements(by=By.XPATH, value='//a[@data-marker="item-title"]')
ads_count = driver.find_element(by=By.XPATH, value="//span[@data-marker='page-title/count']").text.replace(' ','')

if ads_count % 50 > 0:
    page_count = (ads_count // 50) + 1
else:
    page_count = ads_count // 50

for page in range(1, page_count + 1):
    driver.get(f"{url}&p={page}")
    driver.implicitly_wait(3)
    ads_elements = driver.find_elements(by=By.XPATH, value='//a[@data-marker="item-title"]')

    for ad in ads_elements:
        link = ad.get_attribute("href")
        # Записываем ссылку на страницу с объявлениями в csv
        with open("info.csv", mode='a', encoding='utf-8-sig') as csv_file:
            writer = csv.writer(csv_file)
            # Записываем данные
            writer.writerow((url))

data = []
def open_info_csv():
    # Инициализация драйвера
    with open("info.csv", mode='r', encoding='utf-8-sig') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            data.append(row)
# Вызываем функцию
open_info_csv()

list_of_url = open_info_csv()
for row in list_of_url:
    driver.get(row)
    # ищу название объявления
    title = driver.find_element(By.XPATH, "//h1[@data-marker='item-view/title-info']").text.split(',')[0].strip('"')
    # Цену
    price = driver.find_element(By.XPATH, '//span[@data-marker="item-view/item-price"]').get_attribute('content')
    # Тип продавца
    seller_type = driver.find_element(by=By.XPATH, value='//div[@data-marker="seller-info/label"]').text
    # Адрес
    address = driver.find_element(by=By.XPATH, value="//div[@itemprop='address']/span").text

    # cохраняю в файл
    with open("car_info.csv", mode='a', encoding='utf-8-sig') as csv_file:
        writer = csv.writer(csv_file)
        # Записываем данные
        writer.writerow((title, price, seller_type, address))
    driver.close()
    driver.quit()