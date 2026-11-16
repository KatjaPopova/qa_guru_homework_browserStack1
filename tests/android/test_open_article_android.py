from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_open_article(driver):

    wait = WebDriverWait(driver, 30)

    search_icon = wait.until(
        EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia"))
    )
    search_icon.click()

    search_input = wait.until(
        EC.element_to_be_clickable(
            (AppiumBy.ID, "org.wikipedia.alpha:id/search_src_text")
        )
    )
    search_input.send_keys("Appium")

    first_result = wait.until(
        EC.element_to_be_clickable(
            (AppiumBy.ID, "org.wikipedia.alpha:id/page_list_item_title")
        )
    )
    article_title = first_result.text
    assert article_title, "Не нашли заголовок статьи в результатах поиска"

    first_result.click()