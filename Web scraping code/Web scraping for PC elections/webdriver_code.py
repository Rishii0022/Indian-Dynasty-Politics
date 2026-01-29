#selenium.py
def get_lok_sabha_page(state_name, year_value, chromedriver_path=r"C:\Program Files (x86)\chromedriver.exe"):
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import time
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()

    driver.get("https://www.indiavotes.com/")

    form = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "form[onsubmit*='lok-sabha']"))
    )

    state_field = form.find_element(By.ID, "state")
    state_field.send_keys(state_name)
    state_field.send_keys(Keys.RETURN)

    time.sleep(5)

    year_field = form.find_element(By.ID, "year")
    year_field.click()
    year_field.send_keys(year_value)
    year_field.send_keys(Keys.RETURN)

    time.sleep(5)

    search_button = form.find_element(By.CSS_SELECTOR, "input.searchIcon.fr")
    search_button.click()

    time.sleep(5)  # wait for results

    print(driver.current_url)  # confirm page opened
    page_source = driver.page_source

    driver.quit()
    return page_source