from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


nips = ['PL6711688324', 'PL6711688324', 'PL6711688324']


def get_data_for_nip(nip_list):
    """Validates NIP number in VIES Europa."""

    for nip in nip_list:
        # Loops over nip numbers in specified list.
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
        vies = 'https://ec.europa.eu/taxation_customs/vies/vatRequest.html'
        driver.get(vies)


        # Pick a country.
        select_element = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.ID, "countryCombobox"))
                )
        # select_element = driver.find_element(By.ID,'countryCombobox')
        select_object = Select(select_element)
        select_object.select_by_value(nip[:2])


        # Type a NIP number.
        inputElement = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.XPATH,'//*[@id="number"]'))
                )
        inputElement = driver.find_element(By.XPATH,'//*[@id="number"]')
        inputElement.click()
        inputElement.clear()
        inputElement.send_keys(nip[2:])
        inputElement.send_keys(Keys.ENTER)


        # Return final page for NIP number
        final = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.CLASS_NAME ,'validStyle'))
                )

        with open("Raport-NIP.txt", "a") as myfile:
            myfile.write(f'{nip} {final.text} \n')
        driver.quit()
        

print(get_data_for_nip(nips))