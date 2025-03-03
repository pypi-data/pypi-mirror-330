from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

from selenium.webdriver import Chrome as OriginalChrome
from undetected_chromedriver import Chrome as UndetectedChrome
from seleniumwire.webdriver import Chrome as WireChrome
from seleniumwire.undetected_chromedriver import Chrome as WireUndetectedChrome

from .selector import Selector


def Driver(headless:bool=False, wire:bool=False, undetected:bool=False, options=None, service=None, user_data_dir:str=None, profile_directory:str=None, **kwargs):
    '''
    Create a new Chrome driver instance.

    :param headless: Use headless browser.
    :param wire: Use selenium-wire to work with requests.
    :param undetected: Use undetected-chromedriver to avoid anti bot.
    :param options: Options object.
    :param service: Service object.
    :param user_data_dir: User data directory.
    :param profile_directory: Profile directory.
    :param kwargs: Chrome driver keyword arguments.
    :return: Chrome driver instance.
    '''

    options = options if options else Options()

    # User options
    if headless:
        options.add_argument("--headless=new")
    if user_data_dir:
        options.add_argument(f'--user-data-dir={user_data_dir}')
    if profile_directory:
        options.add_argument(f'--profile-directory={profile_directory}')

    # Helpful options
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")  # Avoid error on Linux
    options.add_argument("--ignore-certificate-errors")  # Avoid SSL error
    if not undetected:
        options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Remove "Chrome is being controlled by automated test software."

    if wire and undetected:
        ChromeCls = WireUndetectedChrome
    elif wire:
        ChromeCls = WireChrome
    elif undetected:
        ChromeCls = UndetectedChrome
    else:
        ChromeCls = OriginalChrome

    class CustomChrome(ChromeCls):
        def __init__(self, **kwargs):
            super().__init__(options=options, service=service, **kwargs)

            self.implicitly_wait(20)  # https://selenium-python.readthedocs.io/waits.html#implicit-waits, help avoid selenium.common.exceptions.ElementNotInteractableException: Message: element not interactable
            self.actions = ActionChains(self)
            self.select = Select

        def wait_element(self, value, by: str = By.CSS_SELECTOR, timeout: int = 20, visibility: bool = False, clickable: bool = False):
            '''
            Waits for the element to appear in the DOM or become visible.

            :param value: string or Selector object.
            :param by: string.
            :param timeout: wait time in seconds.
            :param visibility: boolean.
            :param clickable: boolean.
            :return: WebElement object.
            '''
            if isinstance(value, Selector):
                if value.contains:
                    value = value.xpath
                    by = By.XPATH
                else:
                    value = value.css if by == By.CSS_SELECTOR else value.xpath

            if clickable:
                condition = EC.element_to_be_clickable
            elif visibility:
                condition = EC.visibility_of_element_located
            else:
                condition = EC.presence_of_element_located

            return WebDriverWait(self, timeout).until(condition((by, value)))


        def click(self, selector, by: str = By.CSS_SELECTOR, timeout: int = 20, visibility: bool = False, clickable: bool = True):
            '''
            Wait and click on the element if present.

            :param selector: string or Selector object.
            :param by: string.
            :param timeout: wait time in seconds.
            :param visibility: boolean.
            :param clickable: boolean.
            '''
            if element := self.wait_element(selector, by, timeout, visibility, clickable):
                element.click()

        def send_keys(self, selector, value: str, by: str = By.CSS_SELECTOR, timeout: int = 20, visibility: bool = False, clickable: bool = False):
            '''
            Wait and send the keys to the element if available.

            :param selector: string or Selector object.
            :param value: string.
            :param by: string.
            :param timeout: wait time in seconds.
            :param visibility: boolean.
            :param clickable: boolean.
            '''
            if element := self.wait_element(selector, by, timeout, visibility, clickable):
                element.send_keys(value)

        def select_option(self, selector, option, method: str = 'text', by: str = By.CSS_SELECTOR, timeout: int = 20, visibility: bool = False, clickable: bool = False):
            '''
            Select an option from the drop-down list by text, value, or index.

            :param selector: string or Selector object.
            :param option: string for text and value, int for index.
            :param by: string.
            :param timeout: wait time in seconds.
            :param visibility: boolean.
            :param method: text, value, index.
            '''
            if element := self.wait_element(selector, by, timeout, visibility, clickable):
                select = Select(element)
                match method.strip().lower():
                    case "text":
                        select.select_by_visible_text(option)
                    case "value":
                        select.select_by_value(option)
                    case "index":
                        select.select_by_index(option)

        def keystroke(self, *args):
            '''
            Press any key combination.

            :param args: Keys object or any letter.
            '''

            for key in args:
                self.actions.key_down(key)

            for key in reversed(args):
                self.actions.key_up(key)

            self.actions.perform()

        def switch_to_window_title_contains(self, title):
            for window in self.window_handles:
                self.switch_to.window(window)
                if title in self.title:
                    break


    return CustomChrome(**kwargs)
