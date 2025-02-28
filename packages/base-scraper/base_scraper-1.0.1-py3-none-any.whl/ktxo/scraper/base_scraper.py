"""
Scraper base class
"""
import warnings

import copy
import json
import logging
import os
import random
import shutil
import sys
import time

from datetime import datetime
from typing import Dict, Union, Any, Optional
import uuid


import bs4.element # jsut for typping
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.support.ui import Select

try:
    import undetected_chromedriver as uc
except ModuleNotFoundError as me:
    warnings.warn(f"Module 'undetected_chromedriver' not found, ignoring.")

logger=logging.getLogger("ktxo.scraper")

class SeleniumWrapper():
    DEFAULT = {
        "browser": "chrome",
        "wait": [1, 5],
        "wait_ec": {"timeout": 10, "poll_frequency": 0.2},
        "fake_useragent": {"browser": "random"},
        "chrome": {
            "executable_path": "./chromedriver",
            "config": {},
            "chrome_options": ["--headless",
                               "--incognito",
                               "--disable-blink-features=AutomationControlled",
                               "--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"],
            "experimental_option": {
                "prefs": {
                    "download.default_directory": "./tmp",
                    "download.prompt_for_download": False,
                    "download.directory_upgrade": True
                }
            }

        },
        "uc": {
            "config": {
                "headless": False,
                "use_subprocess": False,
                "driver_executable_path": "./undetected_chromedriver"
            },
            "chrome_options": ["--headless",
                               "--incognito",
                               "--disable-blink-features=AutomationControlled",
                               "--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"]
        }

    }

    def __init__(self, config:Dict|str=None, wait=[1,5], exe_path=None, delete_before:bool = True):
        self.driver=None
        self.options:webdriver.ChromeOptions = None
        if isinstance(config, str):
            with open(config, "r") as fd:
                config = json.load(fd)

        self.browser = config.get("browser")
        if not self.browser:
            raise("Wrong config, missing")

        if not self.browser in ["uc", "chrome"]:
            raise Exception(f"Unknown browser configuration '{self.browser}'")

        self.config = copy.deepcopy(config.get(self.browser))
        # Delete before
        if delete_before:
            if config["browser"] == "uc":
                user_dir = config.get("uc").get("config").get("user_data_dir")
                shutil.rmtree(user_dir, ignore_errors=True)
                # --user-data-dir
                user_dir = [o[16:] for o in config.get("chrome").get("chrome_options", []) if o.startswith("--user-data-dir")]
            else:
                user_dir = [o[16:] for o in config.get("chrome").get("chrome_options", []) if o.startswith("--user-data-dir")]
            if user_dir:
                shutil.rmtree(user_dir[0], ignore_errors=True)

        if isinstance(wait, int):
            self.config["wait"] = [0,wait]
        elif isinstance(wait, list):
            self.config["wait"] = [int(wait[0]), int(wait[1])]

        logger.debug(f"Using options {self.config}")

        self.wait = self.config["wait"]
        self.windows = [] # [ [window_handler, url], [window_handler, url], ...]
        self.wait_ec = None
        self.wait_ec_params = config["wait_ec"]
        self.ua = None
        fake_ua_config = config.get("fake_useragent", {})
        if fake_ua_config:
            fake_ua_browser = "random"
            if "browser" in fake_ua_config:
                fake_ua_browser = fake_ua_config["browser"]
                del fake_ua_config["browser"]
                self.ua = getattr(UserAgent(**fake_ua_config), fake_ua_browser)

        #logger.info(f"{self.__class__.__name__}: driver={self.browser}")

    def __build_chrome_options(self) -> webdriver.ChromeOptions:
        # user-agent
        self.options = webdriver.ChromeOptions()
        if self.config.get("chrome_options", []):
            for o in self.config.get("chrome_options", []):
                if o.lower() == "--user-agent=fake":
                    self.options.add_argument(f"--user-agent={self.ua}")
                    continue
                #
                # if o.startswith("--user-agent") and self.ua:
                #     self.options.add_argument(f"--user-agent={self.ua}")
                #     continue
                self.options.add_argument(o)
        for o, v in self.config.get("experimental_option", {}).items():
            self.options.add_experimental_option(o, v)
        return self.options

    def __build_uc_chrome_options(self) -> uc.ChromeOptions:
        # user-agent
        self.options = uc.ChromeOptions()
        if self.config.get("chrome_options", []):
            for o in self.config.get("chrome_options", []):
                if o.lower() == "--user-agent=fake":
                    self.options.add_argument(f"--user-agent={self.ua}")
                    continue
                self.options.add_argument(o)
                if o.startswith("--user-data="):
                    continue
                    #self.options.user_data_dir = o[len("--user-data="):]
        for o, v in self.config.get("experimental_option", {}).items():
            self.options.add_experimental_option(o, v)
        return self.options

    def __init_wait_ec(self):
        self.wait_ec = WebDriverWait(self.driver,
                                     timeout=self.wait_ec_params["timeout"],
                                     poll_frequency=self.wait_ec_params["poll_frequency"]
                                     )

    def __init_chrome(self):
        try:
            self.options = self.__build_chrome_options()
            self.driver = webdriver.Chrome(service=Service(executable_path=self.config["executable_path"]),
                                           options=self.options)
        except WebDriverException as we:
            logger.error(f"Cannot connect to process")
            raise Exception(we)
        self.__init_wait_ec()
        return self.driver

    def __init_uc(self):
        try:
            self.options = self.__build_uc_chrome_options()
            self.driver = uc.Chrome(options=self.options, **self.config["config"])
        except WebDriverException as we:
            logger.error(f"Cannot connect to process")
            raise Exception(we)
        self.__init_wait_ec()
        return self.driver

    def build_wait(self, timeout:float=5, poll_frequency:float=0.5, ignored_exceptions:Optional[Exception] = None):
        return WebDriverWait(self.driver,
                             timeout=timeout,
                             poll_frequency=poll_frequency,
                             ignored_exceptions=ignored_exceptions
                             )

    def start(self, url: str = None):
        if self.browser == "chrome":
            self.driver = self.__init_chrome()
        elif self.browser == "uc":
            self.driver = self.__init_uc()
        if url:
            self.go2url(url)
        return self

    def exit(self):
        try:
            self.driver.close()
        except:
            pass

    def refresh(self):
        self.driver.refresh()

    def maximize(self):
        self.driver.maximize_window()
        return self

    def minimize(self):
        s.driver.minimize_window()
        return self

    def sleep(self, t: float|int|list[int] = None):
        if not t:
            time.sleep(random.randint(*self.wait))
        elif isinstance(t, (int,float)):
            time.sleep(t)
        elif isinstance(t, list):
            time.sleep(random.randint(*self.wait))
        else:
            time.sleep(random.randint(*self.wait))

    def go2urls(self, urls:list[str], use_tab=True):
        for url in urls:
            if use_tab:
                self.go2url(url, True, False)
            else:
                self.go2url(url, False, True)

    def go2url(self, url: str, new_tab: bool = False, new_window:bool = False):
        if new_tab:
            self.driver.switch_to.new_window('tab')
        elif new_window:
            self.driver.switch_to.new_window('window')
        self.driver.get(url)
        self.windows.append([self.driver.current_window_handle, self.driver.current_url])

    def go_2_top_of_page(self):
        ActionChains(self.driver).send_keys(Keys.CONTROL).send_keys(Keys.HOME).perform()

    def go_2_end_of_page(self):
        ActionChains(self.driver).send_keys(Keys.CONTROL).send_keys(Keys.END).perform()

    def key_down(self, key):
        ActionChains(self.driver).key_down(key).perform()

    def close_tab(self, tab: int | str):
        hnd = None
        if isinstance(tab, int):
            if 0 <= tab < len(self.windows):
                hnd = self.windows[tab][0]
        elif isinstance(tab, str):
            hnd = next((w[0] for w in self.windows if w[1] == tab), None)
        if hnd:
            self.driver.switch_to(hnd)
            self.driver.close()
            self.windows.pop(hnd)
            if self.windows:
                self.driver.switch_to(self.windows[0][0])

    def screenshot(self, message: str = None) -> str:
        os.makedirs("dump", exist_ok=True)
        filename = os.path.join("dump",
                                f"{datetime.now().strftime('%Y%M%d_%H%M%S')}_{str(uuid.uuid4())}.png")
        self.driver.save_screenshot(filename)
        logger.debug(f"ScreenShot {filename}")
        if message:
            logger.warning(message)
        return filename

    def find_element(self,
                     selector: str,
                     selector_value,
                     element: WebElement = None,
                     default: Any = None,
                     return_text: bool = False,
                     trim_text: bool = True,
                     log_missing: bool = False) -> Union[WebElement, None]:
        if not element:
            element = self.driver
        try:
            elem = element.find_element(selector, selector_value)
            if return_text:
                return elem.text.strip() if trim_text else elem.text
            else:
                return elem
        except Exception as e:
            if log_missing:
                #logger.warning(f"selector='{selector}' selector_value='{selector_value}' not found. {e}")
                self.screenshot(f"selector='{selector}' selector_value='{selector_value}' not found. {e}")
            if not default is None:
                return default
            return None

    def find_elements(self,
                      selector: str,
                      selector_value: str,
                      element: WebElement = None,
                      default: Any = None,
                      return_text: bool = False,
                      trim_text: bool = True,
                      log_missing: bool = False) -> Union[list[WebElement],None]:
        if not element:
            element = self.driver
        elems = element.find_elements(selector, selector_value)
        if len(elems) == 0:
            if log_missing:
                #logger.warning(f"selector='{selector}' selector_value='{selector_value}' not found")
                self.screenshot(f"selector='{selector}' selector_value='{selector_value}' not found")
            if not default is None:
                return default
            return None
        else:
            if return_text:
                elems_ = []
                for e in elems:
                    if e:
                        elems_.append(e.text.strip() if trim_text else e.text)
                return elems_
            else:
                return elems

    def find_element_bs4(self,
                         name: str,
                         attrs: dict = {},
                         element: str = None,
                         default: Any = None,
                         return_text: bool = False,
                         trim_text: bool = True,
                      log_missing=False) -> Union[bs4.element.Tag, bs4.element.NavigableString, None]:

        if not element:
            elem = BeautifulSoup(self.driver.page_source, 'html.parser').find(name, attrs)
        else:
            elem = element.find(name, attrs)
        if not elem:
            if log_missing:
                logger.warning(f"name={name} attrs={attrs} not found")
                self.screenshot(f"name={name} attrs={attrs} not found")
            if not default is None:
                return default
            return None
        else:
            if return_text:
                return elem.get_text(strip=trim_text)
            else:
                return elem

    def find_elements_bs4(self,
                      name:str,
                      attrs: dict = {},
                      element: str = None,
                      default: Any = None,
                      log_missing: bool = False) -> Union[bs4.element.ResultSet,None]:

        if not element:
            elems = BeautifulSoup(self.driver.page_source, 'html.parser').find_all(name, attrs)
        else:
            elems = element.find_all(name, attrs)

        if len(elems) == 0:
            if log_missing:
                #logger.warning(f"name={name} attrs={attrs} not found")
                self.screenshot(f"name={name} attrs={attrs} not found")
            if not default is None:
                return default
            return None
        else:
            return elems

    def get_href(self,
                 selector: str = None,
                 selector_value: str = None,
                 element: WebElement = None,
                 default="",
                 log_missing: bool = False,
                 ):

        if selector and selector_value:
            element = self.find_element(selector, selector_value, element=element, default=None, log_missing=log_missing)

        if element is None:
            return default
        else:
            try:
                return self.find_element(By.TAG_NAME, "a", element=element).get_attribute("href")
            except:
                return default
    def get_href_bs4(self, element: str = None):
        if not element:
            elems = BeautifulSoup(self.driver.page_source, 'html.parser').find_all("a")
        else:
            elems = element.find_all("a")
        hrefs = []
        for e in elems:
            hrefs.append(e.get("href"))
        return hrefs


    def _wait_4(self,
                type_: str,
                selector: str,
                selector_value: str,
                wait: WebDriverWait = None,
                log_missing: bool = False ):
        """
        wait_type:  visibility_of_element_located
                    presence_of_element_located
                    frame_to_be_available_and_switch_to_it
                    element_to_be_clickable
        """
        try:
            wait_func = getattr(EC, type_)
            if wait:
                return wait.until(wait_func((selector, selector_value)))
            else:
                # EC.text_to_be_present_in_element()
                return self.wait_ec.until(wait_func((selector, selector_value)))
        except TimeoutException as te:
            if log_missing:
                logger.warning(f"wait_func={type_} selector='{selector}' selector_value='{selector_value}' not found")
                self.screenshot(f"wait_func={type_} selector='{selector}' selector_value='{selector_value}' not found")
            return None

    def wait_4_visibility_of_element_located(self,
                                             selector: str,
                                             selector_value: str,
                                             wait: WebDriverWait = None,
                                             log_missing: bool = False ):
        return self._wait_4("visibility_of_element_located", selector, selector_value, wait, log_missing)

    def wait_4_presence_of_element_located(self,
                                           selector: str,
                                           selector_value: str,
                                           wait: WebDriverWait = None,
                                           log_missing: bool = False):
        return self._wait_4("presence_of_element_located", selector, selector_value, wait, log_missing)

    def wait_4_visibility_of_all_elements_located(self,
                                           selector: str,
                                           selector_value: str,
                                           wait: WebDriverWait = None,
                                           log_missing: bool = False):
        return self._wait_4("visibility_of_all_elements_located", selector, selector_value, wait, log_missing)

    def wait_4_visibility_of_any_elements_located(self,
                                           selector: str,
                                           selector_value: str,
                                           wait: WebDriverWait = None,
                                           log_missing: bool = False):
        return self._wait_4("visibility_of_any_elements_located", selector, selector_value, wait, log_missing)

    def wait_4_element_to_be_clickable(self,
                                       selector: str,
                                       selector_value: str,
                                       wait: WebDriverWait = None,
                                       log_missing: bool = False):
        return self._wait_4("element_to_be_clickable", selector, selector_value, wait, log_missing)

    def wait_4_frame_to_be_available_and_switch_to_it(self,
                                                      selector: str,
                                                      selector_value: str,
                                                      wait: WebDriverWait = None,
                                                      log_missing: bool = False):
        return self._wait_4("frame_to_be_available_and_switch_to_it", selector, selector_value, wait, log_missing)

    def wait_4_title_is(self, text: str, wait: WebDriverWait = None, log_missing: bool = False):
        # EC.title_is(), EC.title_contains()
        try:
            if wait:
                return wait.until(EC.title_is(text))
            else:
                # EC.text_to_be_present_in_element()
                return self.wait_ec.until(EC.title_is(text))
        except TimeoutException as te:
            if log_missing:
                logger.warning(f"wait_func=title_is text='{text}' not found")
                self.screenshot(f"wait_func=title_is text='{text}' not found")
            return None

    def switch_to_tab(self, w):
        window = []
        for w_ in self.windows:
            if w in w_:
                window = w_
                break
        if window == []:
            return
        self.driver.switch_to(window[0])

    def switch_to_frame(self, frame=None):
        if frame:
            self.driver.switch_to.frame(frame)
        else:
            self.driver.switch_to.default_content()

    def scroll_to(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def click(self,
              selector: str,
              selector_value: str,
              element: WebElement = None,
              wait: WebDriverWait = None,
              log_missing: bool = False):
        if wait:
            e = self.wait_4_element_to_be_clickable(selector, selector_value, wait, log_missing)
        else:
            e = self.find_element(selector, selector_value, element=element, default=None, log_missing=log_missing)
        if e:
            e.click()
            return True
        else:
            return False

    def click_js(self,
                 selector: str,
                 selector_value: str,
                 element: WebElement = None,
                 wait: WebDriverWait = None,
                 log_missing: bool = False):

        if wait:
            e = self.wait_4_element_to_be_clickable(selector, selector_value, wait, log_missing)
        else:
            e = self.find_element(selector, selector_value, element=element, default=None, log_missing=log_missing)
        if e:
            ActionChains(self.driver).move_to_element(e).click().perform()
            return True
        else:
            return False

    def execute_script(self, script:str, *args):
        self.driver.execute_script(script, *args)

    def _select_func(self,
                     element: WebElement|Select,
                     func: str,
                     log_missing: bool = False,
                     *args):
        try:
            s = element if isinstance(element, Select) else Select(element)
            func = getattr(s, func)
            if func:
                func(*args)
                return True
            return None
        except NoSuchElementException as te:
            if log_missing:
                logger.warning(f"func={func} ' not found")
            return None

    def select_by_visible_text(self, element: WebElement|Select, text:str, log_missing: bool = False):
        return self._select_func(element, "select_by_visible_text", log_missing, text)

    def select_by_index(self, element: WebElement | Select, index: int, log_missing: bool = False):
        return self._select_func(element, "select_by_index", log_missing, index)

    def select_by_value(self, element: WebElement | Select, value: str, log_missing: bool = False):
        return self._select_func(element, "select_by_value", log_missing, value)

    def deselect_all(self, element: WebElement | Select, log_missing: bool = False):
        return self._select_func(element, "deselect_all", log_missing)

    def deselect_by_index(self, element: WebElement | Select, index: int, log_missing: bool = False):
        return self._select_func(element, "deselect_by_index", log_missing, index)

    def deselect_by_value(self, element: WebElement | Select, value: str, log_missing: bool = False):
        return self._select_func(element, "deselect_by_value", log_missing, value)

    def deselect_by_visible_text(self, element: WebElement | Select, text: str, log_missing: bool = False):
        return self._select_func(element, "deselect_by_visible_text", log_missing, text)

    def send_text(self,
                  selector: str,
                  selector_value: str,
                  text: str = "",
                  clear_before: bool = False,
                  element: WebElement = None,
                  wait: WebDriverWait = None,
                  log_missing: bool = False):
        if wait:
            e = self.wait_4_element_to_be_clickable(selector, selector_value, wait, log_missing)
        else:
            e = self.find_element(selector, selector_value, element=element, default=None, log_missing=log_missing)
        if e:
            if clear_before:
                e.clear()
            e.send_keys(text)
            return True
        else:
            return False
