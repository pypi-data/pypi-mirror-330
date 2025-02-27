import time
import logging
import nopecha

from pycaptcha_guard_playwright.base_page import BasePage
from pycaptcha_guard_playwright.captcha_locators.google_recaptcha_locator import GoogleReCaptchaLocator
from pycaptcha_guard_playwright.common_components import constants
from playwright.sync_api import sync_playwright, TimeoutError, Error 


class nopechaGoogleReCaptcha(BasePage):
    
    def __init__(self, driver, browser_context, key: str) -> None:
        
        """
            Initializes the nopechaGoogleReCaptcha class.

            Args:
                driver (WebDriver): The WebDriver object for interacting with the web browser.
                key (str): The key for accessing the nopecha API.
        """
        super().__init__(driver, browser_context)
        self.captcha = True
        self.nopecha_key = key
    

    def check_captcha_expired(self):

        captcha_expired = False
        iframe_unusual_recaptcha_checkbox_locator = self.wait_for_element(GoogleReCaptchaLocator.iframe_checkbox_unusual_traffic_recaptcha, 3000)  
        if iframe_unusual_recaptcha_checkbox_locator:
            iframe_recaptcha_checkbox_locator = self.locate_iframe_within_iframe(GoogleReCaptchaLocator.iframe_checkbox_unusual_traffic_recaptcha, GoogleReCaptchaLocator.iframe_checkbox_recaptcha)
        else:
            iframe_recaptcha_checkbox_locator = self.locate_iframe(GoogleReCaptchaLocator.iframe_checkbox_recaptcha)  

        captcha_expired = self.find_element_in_iframe(iframe_recaptcha_checkbox_locator, GoogleReCaptchaLocator.captcha_expired_msg, 2000)
        
        self.switch_to_default_content()

        return captcha_expired

    
    def recaptcha_solution(self): 
               
        """
            This function solves the reCAPTCHA challenge by clicking the checkbox, completing the captcha, and returning the result.

            Returns:
                bool: False if the reCAPTCHA challenge is successfully solved, True otherwise otherwise.
        """
        self.click_captcha_checkbox()
        tries_count = 0
        start_time = time.time()
        
        while self.captcha and tries_count < constants.RECURSION_COUNT_SIX:
            # captcha_expired = self.check_captcha_expired()
            if round(time.time() - start_time) > constants.CAPTCHA_MAX_TIME:
                logging.info('Going to click to checkbox again')
                start_time = time.time()
                self.click_captcha_checkbox()
            
            tries_count += 1
            
            try:            
                iframe_unusual_recaptcha_checkbox_locator = self.wait_for_element(GoogleReCaptchaLocator.iframe_checkbox_unusual_traffic_recaptcha, 3000)  
                if iframe_unusual_recaptcha_checkbox_locator:
                    iframe_recaptcha_checkbox = self.locate_iframe(GoogleReCaptchaLocator.iframe_checkbox_unusual_traffic_recaptcha)  
                    iframe_popup = self.find_element_in_iframe(iframe_recaptcha_checkbox, GoogleReCaptchaLocator.iframe_popup_recaptcha, 3000)  
                else:    
                    iframe_popup = self.wait_for_element(GoogleReCaptchaLocator.iframe_popup_recaptcha, 3000)
                time.sleep(2)
                iframe_popup_measures = self.get_frame_axis(iframe_popup, GoogleReCaptchaLocator.iframe_popup_recaptcha)
                iframe_popup = self.locate_iframe(GoogleReCaptchaLocator.iframe_popup_recaptcha)  

                try:
                    logging.info("Solving captcha")                
                    self.complete_captcha(iframe_popup, iframe_popup_measures)   
                except Exception as e:
                    logging.exception(f"Error while solving captcha {e}")

                    
                logging.info('Going to switch to the default content')
                self.switch_to_default_content()
            except TimeoutError:
                logging.warning("Timeout error occurred while solving captcha.")
            except Error as e:
                logging.warning(f"Playwright error occurred while solving captcha: {str(e)}")

            time.sleep(3)
            iframe_unusual_recaptcha_checkbox_locator = self.wait_for_element(GoogleReCaptchaLocator.iframe_checkbox_unusual_traffic_recaptcha, 3000)  
            if iframe_unusual_recaptcha_checkbox_locator:
                iframe_recaptcha_checkbox = self.locate_iframe(GoogleReCaptchaLocator.iframe_checkbox_unusual_traffic_recaptcha)  
                iframe_popup = self.find_element_in_iframe(iframe_recaptcha_checkbox, GoogleReCaptchaLocator.iframe_popup_recaptcha, 3000) 
                iframe_recaptcha_checkbox_locator = self.locate_iframe_within_iframe(GoogleReCaptchaLocator.iframe_checkbox_unusual_traffic_recaptcha, GoogleReCaptchaLocator.iframe_checkbox_recaptcha)
            else:    
                iframe_popup = self.wait_for_element(GoogleReCaptchaLocator.iframe_popup_recaptcha, 3000)
                iframe_recaptcha_checkbox_locator = self.locate_iframe(GoogleReCaptchaLocator.iframe_checkbox_recaptcha)  

            captcha_expired = self.find_element_in_iframe(iframe_recaptcha_checkbox_locator, GoogleReCaptchaLocator.captcha_expired_msg, 2000)

            logging.info('Iframe found Trying again')

            # if not iframe_popup:
            #     self.captcha = False
            
            if not captcha_expired and iframe_popup:
                self.captcha = True
            elif captcha_expired and not iframe_popup: 
                self.captcha = True
            else:
                self.captcha = False

            self.switch_to_default_content()
            
        return self.captcha, tries_count
    
        
    def click_captcha_checkbox(self):
        
        """
            Clicks the reCAPTCHA checkbox to verify the user's action.
        """        

        iframe_unusual_recaptcha_checkbox_locator = self.wait_for_element(GoogleReCaptchaLocator.iframe_checkbox_unusual_traffic_recaptcha)  
        if iframe_unusual_recaptcha_checkbox_locator:
            iframe_recaptcha_checkbox = self.locate_iframe(GoogleReCaptchaLocator.iframe_checkbox_unusual_traffic_recaptcha)  
            iframe_recaptcha_checkbox_locator = self.find_element_in_iframe(iframe_recaptcha_checkbox, GoogleReCaptchaLocator.iframe_checkbox_recaptcha)  
            iframe_recaptcha_checkbox_locator_measures = self.get_frame_axis(iframe_recaptcha_checkbox_locator, GoogleReCaptchaLocator.iframe_checkbox_recaptcha)
            iframe_recaptcha_checkbox = self.locate_iframe_within_iframe(GoogleReCaptchaLocator.iframe_checkbox_unusual_traffic_recaptcha, GoogleReCaptchaLocator.iframe_checkbox_recaptcha)  
        else:
            iframe_recaptcha_checkbox_locator = self.wait_for_element(GoogleReCaptchaLocator.iframe_checkbox_recaptcha)  
            iframe_recaptcha_checkbox_locator_measures = self.get_frame_axis(iframe_recaptcha_checkbox_locator, GoogleReCaptchaLocator.iframe_checkbox_recaptcha)   
            iframe_recaptcha_checkbox = self.locate_iframe(GoogleReCaptchaLocator.iframe_checkbox_recaptcha) 

        recaptcha_checkbox_locator = self.find_element_in_iframe(iframe_recaptcha_checkbox, GoogleReCaptchaLocator.recaptcha_checkbox)
        # self.click_captcha(recaptcha_checkbox_locator, iframe_recaptcha_checkbox_locator_measures)
        self.click_captcha(recaptcha_checkbox_locator, iframe_recaptcha_checkbox_locator_measures, False)
        
        
    def get_recaptcha_text_instructions(self, iframe):
        
        """
            Returns:
                str: The text instructions for completing the reCAPTCHA.
        """        
        time.sleep(2)
        instructions_text_locator = None
        try:
            instructions_text_locator = self.find_element_in_iframe(iframe, GoogleReCaptchaLocator.instruction_text1, 3000).inner_text()
        except:            
            try:
                instructions_text_locator = self.find_element_in_iframe(iframe, GoogleReCaptchaLocator.instruction_text2, 3000).inner_text()
            except:
                pass
        
        return instructions_text_locator
            
         
    def complete_captcha(self, iframe, iframe_popup_measures, counter=1, image_link=None, all_imgs_list=[]):
        
        """
            Completes the captcha challenge using the provided parameters.

            Args:
                iframe measures (list, required): List of measures of iframe's x-axis and y-axis and top height of browser. 
                counter (int, optional): The number of the captcha challenge. Defaults to 1.
                image_link (str, optional): The URL of the captcha image. Defaults to None.
                all_imgs_list (list, optional): List of all captcha image URLs. Defaults to [].
        """
        text = self.get_recaptcha_text_instructions(iframe)
        total_rows = len(self.find_elements_in_iframe(iframe, GoogleReCaptchaLocator.recaptcha_images_rows))
        all_imgs = self.find_elements_in_iframe(iframe, GoogleReCaptchaLocator.recaptcha_images)
        unique_image_links = []
        positions = []
        
        if counter == 1 or total_rows == 4:
            image_link = self.find_element_in_iframe(iframe, GoogleReCaptchaLocator.image_link).get_attribute("src")  
            unique_image_links.append(image_link)

        for one_img in all_imgs:
            img_src = one_img.get_attribute("src")
            if img_src != image_link:
                if img_src not in unique_image_links:
                    if img_src not in all_imgs_list:
                        td_ancestor = one_img.locator("xpath=ancestor::td")
                        positions.append(int(td_ancestor.get_attribute("tabIndex"))-3)
                        unique_image_links.append(img_src)

        for each in unique_image_links:
            all_imgs_list.append(each)
                            
        if total_rows == 3:
            grid = '3x3'
        else:
            grid = '4x4'
            
        if grid == '3x3':
            if len(unique_image_links) > 1:
                grid = '1x1'
            if int(counter) > 1:
                grid = '1x1'

        for _ in range(constants.MAX_RECURSION_COUNT):
            try:
                grid_click_array, bool_array = self.nopecha_captcha(text, unique_image_links, grid)
                break
            except Exception as e:
                logging.exception(f"Unable to get the API response : {e}") 
                time.sleep(4)
                       

        if counter > 1 and total_rows != 4:
            grid_click_array = [pos for pos, is_true in zip(positions, bool_array) if is_true]
        

        self.click_captcha_image(iframe, iframe_popup_measures, grid_click_array, counter, image_link, all_imgs_list, text)


    def nopecha_captcha(self, text, unique_image_links, grid):
                
        """
            This function uses the nopecha API to solve the captcha challenge.

            Args:
                text (str): The captcha challenge text.
                unique_image_links (List[str]): List of unique image URLs.
                grid (str): The grid size of the captcha challenge.

            Returns:
                List[int]: List of grid indices to click on.
                List[bool]: List of boolean values indicating whether to click on each grid index.
        """        
        nopecha.api_key = self.nopecha_key

        try:
            clicks = nopecha.Recognition.solve(
                type='recaptcha',
                task=text,
                image_urls=unique_image_links,
                grid=grid
            )
            
        except nopecha.error.InvalidRequestError as e:
            logging.error(f'Nopecha request failed with parameters: task={text}, image_urls={unique_image_links}, grid={grid}')            
            return [], []


        true_indices = [i for i, value in enumerate(clicks) if value]
        
        grid_click_array = true_indices
        grid_click_array = [int(x+1) for x in grid_click_array]

        return grid_click_array, clicks
    

    def click_captcha_image(self, iframe, iframe_popup_measures, grid_click_array, counter, image_link, all_imgs_list, text):
        
        """
            This function will click on the captcha images by finding its xpath and element through grid_click_array.

            Args:
                grid_click_array (List[int]): List of numbers which are returned from the nopecha key.
        """        
        total_rows = len(self.find_elements_in_iframe(iframe, GoogleReCaptchaLocator.recaptcha_images_rows))

        for number in grid_click_array:
            cell_xpath = GoogleReCaptchaLocator.get_matched_image_path(number, total_rows)            
            cell = self.find_element_in_iframe(iframe, cell_xpath)
            self.click_captcha(cell, iframe_popup_measures)
        
        submit_button = self.find_element_in_iframe(iframe, GoogleReCaptchaLocator.submit_button)
        text_submit_button = submit_button.inner_text()
        text_submit_button = text_submit_button.lower().strip()
        time.sleep(4)
            
        if grid_click_array == []:
            self.click_captcha(submit_button, iframe_popup_measures)
        elif "Click verify once there are none left" in text:
            self.complete_captcha(iframe, iframe_popup_measures, counter+1, image_link, all_imgs_list)
        else:
            if "skip" in text_submit_button:
                self.complete_captcha(iframe, iframe_popup_measures, counter+1, image_link, all_imgs_list)
            self.click_captcha(submit_button, iframe_popup_measures)

