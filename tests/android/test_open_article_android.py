import allure
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

SEARCH_RESULT_TITLE = (AppiumBy.ID, "org.wikipedia.alpha:id/page_list_item_title")
ARTICLE_TITLE = (AppiumBy.ID, "org.wikipedia.alpha:id/view_page_title_text")


@allure.title("Открытие статьи через поиск (Android)")
def test_open_article(driver):
    wait = WebDriverWait(driver, 30)

    with allure.step("Открыть поиск по Википедии"):
        search_icon = wait.until(
            EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia"))
        )
        search_icon.click()

    with allure.step("Ввести поисковый запрос 'Appium'"):
        search_input = wait.until(
            EC.element_to_be_clickable(
                (AppiumBy.ID, "org.wikipedia.alpha:id/search_src_text")
            )
        )
        search_input.send_keys("Appium")

    with allure.step("Дождаться результатов поиска и найти первую статью"):
        first_result = wait.until(EC.element_to_be_clickable(SEARCH_RESULT_TITLE))
        article_title = first_result.text
        allure.attach(
            article_title,
            name="Заголовок в результатах поиска",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert article_title, "Не нашли заголовок статьи в результатах поиска"

    with allure.step("Кликнуть на найденную статью"):
        first_result.click()

    with allure.step("Дождаться открытия статьи и сравнить заголовок с сохранённым"):
        opened_title_element = wait.until(EC.presence_of_element_located(ARTICLE_TITLE))
        opened_title = opened_title_element.text
        allure.attach(
            opened_title,
            name="Заголовок открывшейся статьи",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert opened_title == article_title, (
            f"Открылась статья '{opened_title}', а не ожидаемая '{article_title}'"
        )