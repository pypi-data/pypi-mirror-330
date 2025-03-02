from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import TimeoutException

from selenium.webdriver import Chrome as OriginalChrome
from undetected_chromedriver import Chrome as UndetectedChrome
from seleniumwire.webdriver import Chrome as WireChrome
from seleniumwire.undetected_chromedriver import Chrome as WireUndetectedChrome

from .selector import Selector

import warnings

class Chrome(WireChrome, WireUndetectedChrome, UndetectedChrome, OriginalChrome):
    def __init__(self, *args, headless:bool=False, wire:bool=False, undetected:bool=False, options=None, service=None, user_data_dir:str=None, profile_directory:str=None, **kwargs):
        '''
        Create a new Chrome driver instance.

        :param args: Chrome driver arguments.
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
        options.add_argument("--no-sandbox") # Avoid error on Linux
        options.add_argument("--ignore-certificate-errors") # Avoid SSL error

        # Choose Chrome driver
        if wire and undetected:
            WireUndetectedChrome.__init__(self, *args, **kwargs, options=options, service=service)
        elif wire:
            WireChrome.__init__(self, *args, **kwargs, options=options, service=service)
        elif undetected:
            UndetectedChrome.__init__(self, *args, **kwargs, options=options, service=service)
        else:
            options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Remove "Chrome is being controlled by automated test software."
            OriginalChrome.__init__(self, *args, **kwargs, options=options, service=service)


        self.actions = ActionChains(self)
        self.select = Select


    def __dir__(self):
        return dir(self.__dir__())


    def wait_element(self, value, by:str=By.CSS_SELECTOR, timeout:int=10, visibility:bool=False, clickable:bool=False):
        '''
        Waits for the element to appear in the DOM or become visible.

        :param value: string or Selector object.
        :param by: string.
        :param timeout: wait time in seconds.
        :param visibility: boolean.
        :return: WebElement object.
        '''
        if isinstance(value, Selector):
            if value.contains:
                value = value.xpath
                by = By.XPATH
            else:
                value = value.css if by==By.CSS_SELECTOR else value.xpath

        if clickable:
            condition = EC.element_to_be_clickable
        elif visibility:
            condition = EC.visibility_of_element_located
        else:
            condition = EC.presence_of_element_located

        try:
            return WebDriverWait(self, timeout).until(condition((by, value)))
        except TimeoutException:
            warnings.warn(message=f'Timeout and element not found. {value}')
            return None


    def click(self, selector, by:str=By.CSS_SELECTOR, timeout:int=10, visibility:bool=False):
        '''
        Wait and click on the element if present.

        :param selector: string or Selector object.
        :param by: string.
        :param timeout: wait time in seconds.
        :param visibility: boolean.
        '''
        if element := self.wait_element(selector, by, timeout, visibility):
            element.click()


    def send_keys(self, selector, value:str, by:str=By.CSS_SELECTOR, timeout:int=10, visibility:bool=False):
        '''
        Wait and send the keys to the element if available.

        :param selector: string or Selector object.
        :param value: string.
        :param by: string.
        :param timeout: wait time in seconds.
        :param visibility: boolean.
        '''
        if element := self.wait_element(selector, by, timeout, visibility):
            element.send_keys(value)


    def select_option(self, selector, option, by:str=By.CSS_SELECTOR, timeout:int=10, visibility:bool=False, method:str='text'):
        '''
        Select an option from the drop-down list by text, value, or index.

        :param selector: string or Selector object.
        :param option: string for text and value, int for index.
        :param by: string.
        :param timeout: wait time in seconds.
        :param visibility: boolean.
        :param method: text, value, index.
        '''
        if element := self.wait_element(selector, by, timeout, visibility):
            select = Select(element)
            match method.strip().lower():
                case "text": select.select_by_visible_text(option)
                case "value": select.select_by_value(option)
                case "index": select.select_by_index(option)


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