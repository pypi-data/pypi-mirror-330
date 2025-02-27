import time
import logging
import capsolver
import requests
import base64

from pycaptcha_guard_playwright.base_page import BasePage
from pycaptcha_guard_playwright.captcha_locators.google_recaptcha_locator import GoogleReCaptchaLocator
from pycaptcha_guard_playwright.common_components import constants
from playwright.sync_api import sync_playwright, TimeoutError, Error 

class capsolverGoogleReCaptcha(BasePage):
    
    def __init__(self, driver, browser_context, key: str) -> None:
        
        """
            Initializes the capsolverGoogleReCaptcha class.

            Args:
                driver (WebDriver): The WebDriver object for interacting with the web browser.
                key (str): The key for accessing the capsolver API.
        """
        super().__init__(driver, browser_context)
        self.captcha = True
        self.capsolver_key = key
    
    
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
                # switch to unusual traffic google iframe
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
                
        
    def complete_captcha(self, iframe, iframe_popup_measures):
        
        """
            Completes the captcha challenge using the provided parameters.

            Args:
                iframe measures (list, required): List of measures of iframe's x-axis and y-axis and top height of browser. 
                counter (int, optional): The number of the captcha challenge. Defaults to 1.
                image_link (str, optional): The URL of the captcha image. Defaults to None.
                all_imgs_list (list, optional): List of all captcha image URLs. Defaults to [].
        """
        text = self.get_recaptcha_text_instructions(iframe)
        full_image_locator = self.find_element_in_iframe(iframe, GoogleReCaptchaLocator.recaptcha_full_image)
        if full_image_locator:
            img_source = full_image_locator.get_attribute('src')
            logging.info(f"Image source found: {img_source}")
                
        all_imgs = self.find_elements_in_iframe(iframe, GoogleReCaptchaLocator.recaptcha_images)
        unique_image_links = []
        positions = []
        all_imgs_list=[]
        
        image_link = self.find_element_in_iframe(iframe, GoogleReCaptchaLocator.image_link).get_attribute("src")  
        unique_image_links.append(image_link)

        for one_img in all_imgs:            
            img_src = one_img.get_attribute("src")
            if img_src != image_link:
                if img_src not in [img[0] for img in unique_image_links]:
                    if img_src not in all_imgs_list:
                        td_ancestor = one_img.locator("xpath=ancestor::td")
                        position_index = int(td_ancestor.get_attribute("tabIndex"))-3
                        positions.append(position_index)
                        unique_image_links.append((img_src, position_index))

        for each in unique_image_links:
            all_imgs_list.append(each)
        
        for _ in range(constants.MAX_RECURSION_COUNT):
            try:
                grid_click_array = self.capsolver_captcha(text, unique_image_links)
                break
            except Exception as e:
                logging.exception(f"Unable to get the API response : {e}") 
                time.sleep(2)
        

        self.click_captcha_image(iframe, iframe_popup_measures, grid_click_array, text)
        
            
    def click_captcha_image(self, iframe, iframe_popup_measures, grid_click_array, text):
        
        """
            This function will click on the captcha images by finding its xpath and element through grid_click_array.

            Args:
                grid_click_array (List[int]): List of numbers which are returned from the nopecha key.
        """        
        total_rows = len(self.find_elements_in_iframe(iframe, GoogleReCaptchaLocator.recaptcha_images_rows))

        for number in grid_click_array.get("objects"):
            cell_xpath = GoogleReCaptchaLocator.get_matched_image_path(number+1, total_rows)
            cell = self.find_element_in_iframe(iframe, cell_xpath)
            self.click_captcha(cell, iframe_popup_measures)
        
        submit_button = self.find_element_in_iframe(iframe, GoogleReCaptchaLocator.submit_button)
        text_submit_button = submit_button.inner_text()
        text_submit_button = text_submit_button.lower().strip()
        time.sleep(2)
            
        if grid_click_array.get("objects") == []:
            self.click_captcha(submit_button, iframe_popup_measures)
        elif "Click verify once there are none left" in text:
            self.complete_captcha(iframe, iframe_popup_measures)
        else:
            if "skip" in text_submit_button:
                self.complete_captcha(iframe, iframe_popup_measures)
            self.click_captcha(submit_button, iframe_popup_measures)
            
                    
    def capsolver_captcha(self, text, image_url):
        """
        This function sends the captcha image to the capsolver API and returns the solution.

        Args:
            text (str): The text instructions for completing the reCAPTCHA.
            image_url (str): The URL of the captcha image.

        Returns:
            solution: The solution returned by the capsolver API.
        """
        
        capsolver.api_key = self.capsolver_key

        keyword = text.split('\n')[1]
        
        keyword_map = {
            "/m/0pg52": "taxis",
            "/m/01bjv": "bus",
            "/m/02yvhj": "school bus",
            "/m/04_sv": "motorcycles",
            "/m/013xlm": "tractors",
            "/m/01jk_4": "chimneys",
            "/m/014xcs": "crosswalks",
            "/m/015qff": "traffic lights",
            "/m/0199g": "bicycles",
            "/m/015qbp": "parking meters",
            "/m/0k4j": "cars",
            "/m/015kr": "bridges",
            "/m/019jd": "boats",
            "/m/0cdl1": "palm trees",
            "/m/09d_r": "mountains or hills",
            "/m/01pns0": "fire hydrant",
            "/m/01lynh": "stairs"
        }
        
        for code, word in keyword_map.items():
            if word in keyword:
                question_code = code
                break

        if len(image_url) == 1:
            if requests.get(image_url[0]).status_code == 200:

                with requests.get(image_url[0]) as response, open("captcha_image.png", "wb") as f:
                    f.write(response.content)
                
                with open("captcha_image.png", "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            
                payload = {
                    "type": "ReCaptchaV2Classification",
                    "image": encoded_string,
                    "question": question_code,
                }
                
                solution = capsolver.solve(payload)
                
                logging.info(f'Captcha Solution {solution}')
                return solution
        else:
            
            img_solution = []  
            solution = {}          
            for url in image_url[1:]:                              
                if requests.get(url[0]).status_code == 200:                    
                    with requests.get(url[0]) as response, open("captcha_image.png", "wb") as f:
                        f.write(response.content)
                
                with open("captcha_image.png", "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            
                payload = {
                    "type": "ReCaptchaV2Classification",
                    "image": encoded_string,
                    "question": question_code,
                }
                
                indices = capsolver.solve(payload)               
                logging.info(f'Captcha Solution {indices}')
                
                if indices.get('hasObject'):
                    img_solution.append(url[1]-1) 
                    
                solution['objects'] = img_solution
                
        return solution   
                    
            
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
            
        logging.info(f"instructions_text_locator : {instructions_text_locator}")
        
        return instructions_text_locator