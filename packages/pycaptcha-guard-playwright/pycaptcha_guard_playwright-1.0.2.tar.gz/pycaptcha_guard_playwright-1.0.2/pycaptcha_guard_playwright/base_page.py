# Standard library imports
import logging
import random
import time
import pyautogui
from typing import List, Tuple, Optional
from pycaptcha_guard_playwright.common_components import constants
from oxymouse import OxyMouse

class BasePage:
    """Base class to initialize the base page that will be called from all pages"""

    def __init__(self, driver, browser_context) -> None:
        """ This function is called every time a new object of the base class is created"""
        self.driver = driver
        self.browser_context = browser_context
        
    def wait_for_element(self, locator: str, timeout: int = constants.WAIT_TIMEOUT, silent=False):
        try:
            # Wait for the element to be present using Playwright's locator method
            element = self.driver.locator(locator).nth(0) # Assuming 'locator' is a CSS selector or XPath
            element.wait_for(timeout=timeout) # Wait for the element to be present
            return element
        except Exception:
            if not silent:
                logging.exception(f"Element with locator {locator} on url {self.driver.url} not found within {timeout} seconds")
            return None
    
    def wait_for_element_to_be_visible(self, locator: str, timeout: int=constants.WAIT_TIMEOUT, silent=False):
        try:
            element = self.driver.locator(locator)
            element.wait_for(state="visible", timeout=timeout)
            return element
        except TimeoutError:
            if not silent:
                logging.exception(f"Element with locator {locator} on url {self.driver.url} not found within {timeout} seconds")
            return None
                        
    def switch_to_default_content(self) -> None:
        """
        Switch to the default content (main page context).
        """
        iframe = self.driver.main_frame
        return iframe
        
    def wait_for_elements(self, locator: str, timeout: int=constants.WAIT_TIMEOUT, silent=False):
        try:
            elements = self.driver.query_selector_all(locator)
            return elements
        except TimeoutError:
            if not silent:
                logging.exception(f"Elements with locator {locator} on url {self.driver.url} not found within {timeout} milliseconds")
            return None
    
    def enter_text(self, by_locator: str, text: str) -> None:
        """ Performs text entry of the passed in text, in a web element whose locator is passed to it"""
        
        self.driver.evaluate("window.onfocus")
        element = self.wait_for_element(by_locator)

        if element:
            for one in text:
                element.type(one)
            try:
                self.press_enter_on_element(by_locator)
            except Exception as e:
                logging.exception(f"Failed to press enter on element {by_locator}: {e}")
                element.click()
        time.sleep(2) 

    def enter_text_and_click_submit(self, text_locator: str, text: str, target_btn: str) -> None:
        """ Performs text entry of the passed in text, whose locator is passed to it"""
        
        self.driver.evaluate("window.onfocus")
        element = self.wait_for_element(text_locator)

        if element:
            for one in text:
                element.type(one)
            try:
                self.move_mouse_to_element(target_btn)
                target_btn.click()
            except Exception as e:
                logging.exception(f"Failed to submit button {target_btn}: {e}")
                target_btn.click()
        time.sleep(2) 
        
    def press_enter_on_element(self, locator: str):
        """
            Take the element and press enter in that element

        Args:
            locator (Tuple[str, str]): Element locator to perform actions
        """
        try:
            element = self.wait_for_element(locator, constants.WAIT_TIMEOUT, silent=True)
            if element:
                element.press("Enter")
            else:
                self.driver.keyboard.press("Enter")
        except Exception as e:
            logging.exception(f"Error occurred while pressing Enter on element with locator {locator}: {str(e)}")
        
            
    def click_captcha(self, element, iframe_measures, click_on_images=True) -> None:
        """ 
            Performs click on captcha web element whose locator is passed to it
        """
        
        try: 
            self.move_mouse_to_captcha_element(element, iframe_measures, click_on_images)
        except:
            pass
        try:
            element.click()
        except:
            try:
                self.driver.evaluate("arguments[0].scrollIntoView();", element)
                element.click()
            except:
                try:
                    self.driver.evaluate("arguments[0].scrollIntoView();", element)
                    self.driver.evaluate("arguments[0].click();", element)
                except:
                    pass
                
                
    def move_mouse_to_captcha_element(self, element, iframe_measures, click_on_images=True):
        """
        Move the mouse to a random location within a WebElement.

        Parameters:
        - `element`: a Selenium WebElement
        - `iframe measure`: iframe axis location for exact mouse movement
        """
        x_iframe, y_iframe, top_height = iframe_measures
                
        try:
            # Get the bounding box of the element
            bounding_box = element.bounding_box()
            loc_x = bounding_box['x']
            loc_y = bounding_box['y']
            size_height = bounding_box["height"]
            size_width = bounding_box["width"]

            # Obtain the window position
            window_position = self.driver.evaluate("""
                () => ({
                    x: window.screenX,
                    y: window.screenY
                })
            """)

            # Adjust the location of the WebElement by the position of the WebDriver's browser window
            loc_x += window_position['x'] + x_iframe
            loc_y += window_position['y'] + top_height + y_iframe

            # Get the position of each side of the element
            top, bottom = loc_y, loc_y + size_height
            left, right = loc_x, loc_x + size_width

            # Generate a random location within these bounds
            end_x = int(random.uniform(left, right))
            end_y = int(random.uniform(top, bottom))

            if click_on_images == True:
                pyautogui.moveTo(end_x, end_y, duration=0.5)
            else:
                start_x, start_y = pyautogui.position()
                self.move_mouse_to_coordinates(end_x, end_y, start_x, start_y)
        except:
            pass
        try:
            center_x = bounding_box["x"] + bounding_box["width"] / 2
            center_y = bounding_box["y"] + bounding_box["height"] / 2
            # Move the mouse to the center of the element
            self.driver.mouse.move(center_x, center_y)
        except:
            pass


    def move_mouse_to_element(self, element):
        """
        Move the mouse to a random location within an element in Playwright.

        Parameters:
        - `page`: Playwright page object
        - `selector`: CSS selector for the target element
        """
        try:
            # Get the bounding box of the element
            bounding_box = element.bounding_box()
            loc_x = bounding_box['x']
            loc_y = bounding_box['y']
            size_height = bounding_box["height"]
            size_width = bounding_box["width"]

            if not bounding_box:
                raise ValueError("Could not retrieve the bounding box of the element.")

            # window_position = self.page.evaluate("({ x: window.screenX, y: window.screenY })")
            window_position = self.driver.evaluate("({ x: 0, y: 0 })")

            # Calculate the height of the title and URL bar
            bars_height = self.driver.evaluate("window.outerHeight - window.innerHeight")

            # Adjust the location of the WebElement by the position of the WebDriver's browser window
            loc_x += window_position['x']
            loc_y += window_position['y'] + bars_height

            # Get the position of each side of the element
            top, bottom = loc_y, loc_y + size_height
            left, right = loc_x, loc_x + size_width

            # Generate a random location within these bounds
            end_x = int(random.uniform(left, right))
            end_y = int(random.uniform(top, bottom))

            # # Move the mouse to the random location
            # self.page.mouse.move(end_x, end_y)

            # # Move the mouse
            # pyautogui.moveTo(end_x, end_y, duration=random.uniform(0.1, 0.5))

            start_x, start_y = pyautogui.position()
            self.move_mouse_to_coordinates(end_x, end_y, start_x, start_y)

        except Exception as e:
            print(f"Error: {e}")
        try:
            # Calculate the center of the element
            center_x = bounding_box["x"] + bounding_box["width"] / 2
            center_y = bounding_box["y"] + bounding_box["height"] / 2
            # Move the mouse to the center of the element
            self.page.mouse.move(center_x, center_y)
        except:
            pass


    def move_mouse_to_coordinates(self, end_x: int, end_y: int, start_x, start_y):
        """
        # Move the mouse from the start coordinates to the end coordinates in a human-like way.
        The mouse movement is determined by a cubic curve.

        ## Parameters:
        - `end_x`: end x-coordinate
        - `end_y`: end y-coordinate
        - `duration`: duration of the movement
        """

        distance = ((end_x - start_x) ** 2 + (end_y - start_y) ** 2) ** 0.5
        if distance < 100:  # Small movement (fast flick)
            base_delay = random.uniform(0.005, 0.01)  # 5ms to 10ms
        elif distance < 300:  # Medium movement
            base_delay = random.uniform(0.01, 0.025)  # 10ms to 25ms
        else:  # Large movement (slow start, fast middle, slow end)
            base_delay = random.uniform(0.02, 0.05)  # 20ms to 50ms
        mouse = OxyMouse(algorithm="gaussian")
        movements = mouse.generate_coordinates(from_x=start_x, from_y=start_y, to_x=end_x, to_y=end_y)
        for x, y in movements:
            pyautogui.moveTo(x, y, duration=base_delay)
                
    def get_frame_axis(self, element, locator):
        """
            Get the locations of axis of the iframe and windows top bar height
        """
        
        x_iframe = None
        y_iframe = None
        top_height = None
        
        try:
            bounding_box = element.bounding_box()
            x_iframe = bounding_box['x']
            y_iframe = bounding_box['y']
            top_height = self.driver.evaluate("window.outerHeight - window.innerHeight;")
        except Exception as e:
            logging.exception(f'error while getting iframe axis : {e}')
            element = self.wait_for_element(locator, constants.WAIT_TIMEOUT, silent=True)
            time.sleep(2)
            if element:
                x_iframe = bounding_box['x']
                y_iframe = bounding_box['y']
                top_height = self.driver.evaluate("window.outerHeight - window.innerHeight;")
            
        return x_iframe, y_iframe, top_height
    

    def locate_iframe(self, iframe_selector: str, timeout: int=constants.WAIT_TIMEOUT):
        """
        Locate and return an iframe by its selector.
        :param iframe_selector: CSS or XPath selector for the iframe.
        :return: Playwright Frame object.
        """
        iframe_element = self.driver.frame_locator(iframe_selector).first
        if not iframe_element:
            logging.exception(f"Iframe with selector '{iframe_selector}' not found.")
        return iframe_element
    

    def locate_iframe_from_main_iframe(self, parent_iframe_selector: str, child_iframe_selector: str, timeout: int=constants.WAIT_TIMEOUT):
        """
        Locate an iframe within another iframe.
        :param parent_iframe_selector: Selector for the parent iframe.
        :param child_iframe_selector: Selector for the child iframe within the parent iframe.
        :return: Playwright Frame object for the child iframe.
        """
        parent_frame = self.locate_iframe(parent_iframe_selector)
        child_iframe_element = parent_frame.frame_locator(child_iframe_selector).first

        if not child_iframe_element:
            logging.exception(f"Child iframe with selector '{child_iframe_selector}' not found inside '{parent_iframe_selector}'.")
        return child_iframe_element


    def locate_iframe_within_iframe(self, parent_iframe_selector: str, child_iframe_selector: str, timeout: int=constants.WAIT_TIMEOUT):
        """
        Locate an iframe within another iframe.
        :param parent_iframe_selector: Selector for the parent iframe.
        :param child_iframe_selector: Selector for the child iframe within the parent iframe.
        :return: Playwright Frame object for the child iframe.
        """
        parent_frame = self.locate_iframe(parent_iframe_selector, timeout=timeout)
        child_iframe_element = parent_frame.frame_locator(child_iframe_selector).first
        if not child_iframe_element:
            logging.exception(f"Child iframe with selector '{child_iframe_selector}' not found inside '{parent_iframe_selector}'.")
        return child_iframe_element
    

    def find_element_in_iframe(self, iframe, element_selector: str, timeout: int=constants.WAIT_TIMEOUT):

        """
        Finds an element inside a specified iframe and returns it.
        :param iframe: The CSS or XPath selector for the iframe.
        :param element_selector: The CSS or XPath selector for the element inside the iframe.
        :param timeout: Maximum time to wait for the iframe and element to appear (in milliseconds). Default is 10 seconds.
        :return: Locator object for the found element inside the iframe.
        :raises Exception: If the iframe or element is not found within the timeout.
        """
        try:
            # Locate the iframe
            element = iframe.locator(element_selector).nth(0)
            element.wait_for(timeout=timeout)
            return element
        except Exception as e:
            logging.exception(f"Element with selector '{element_selector}' inside iframe '{iframe}' not found within {timeout} ms. Error: {str(e)}")
        return None


    def find_elements_in_iframe(self, iframe, element_selector: str, timeout: int=constants.WAIT_TIMEOUT):
        try:
            elements = iframe.locator(element_selector).nth(0)
            elements.wait_for(timeout=timeout)
            elements = iframe.locator(element_selector).all()
            return elements
        except Exception as e:
            logging.exception(f"Elements with selector '{element_selector}' inside iframe '{iframe}' not found within {timeout} ms. Error: {str(e)}")
        return None