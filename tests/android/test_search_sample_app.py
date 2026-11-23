import allure
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

SEARCH_RESULT_TITLE = (AppiumBy.ID, "org.wikipedia.alpha:id/page_list_item_title")


@allure.title("Поиск статьи в Wikipedia sample app")
def test_successful_search(driver):
    wait = WebDriverWait(driver, 30)

    with allure.step("Открыть поиск"):
        search_element = wait.until(
            EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia"))
        )
        search_element.click()

    with allure.step("Ввести запрос 'Appium'"):
        insert_text_element = wait.until(
            EC.element_to_be_clickable(
                (AppiumBy.ID, "org.wikipedia.alpha:id/search_src_text")
            )
        )
        insert_text_element.send_keys("Appium")

    with allure.step("Проверить, что среди заголовков результатов есть ожидаемый"):
        wait.until(EC.presence_of_element_located(SEARCH_RESULT_TITLE))
        result_titles = [
            element.text for element in driver.find_elements(*SEARCH_RESULT_TITLE)
        ]
        allure.attach(
            "\n".join(result_titles),
            name="Заголовки результатов поиска",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert any("Appium" in title for title in result_titles), (
            f"Среди результатов поиска не нашли 'Appium': {result_titles}"
        )