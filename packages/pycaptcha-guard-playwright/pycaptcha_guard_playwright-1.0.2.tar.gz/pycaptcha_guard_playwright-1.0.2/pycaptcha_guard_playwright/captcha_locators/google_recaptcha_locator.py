# from selenium.webdriver.common.by import By

class GoogleReCaptchaLocator:
    
    @staticmethod
    def get_matched_image_path(number, total_cols):
        if number:
            row = (number - 1) // total_cols
            col = (number - 1) % total_cols
            # return (By.XPATH, f'//table//tr[{row+1}]/td[{col+1}]')
            return f'//table//tr[{row+1}]/td[{col+1}]'
        return None
    
    
    iframe_checkbox_unusual_traffic_recaptcha = "iframe[title='Captcha']"
    iframe_checkbox_recaptcha = "iframe[title='reCAPTCHA']"
    recaptcha_checkbox = "div.recaptcha-checkbox-border"
    iframe_popup_recaptcha = "iframe[title='recaptcha challenge expires in two minutes']"
    instruction_text1 = ".rc-imageselect-desc-no-canonical"
    table_iframe = 'table'
    instruction_text2 = ".rc-imageselect-desc"
    # recaptcha_images_rows = "//table//tr"
    recaptcha_images_rows = "table tr"
    # recaptcha_images = "//table//img"
    recaptcha_images = "table img"
    # recaptcha_full_image = "//img[contains(@class, 'rc-image-tile')]"
    recaptcha_full_image = "img[class*='rc-image-tile']"
    submit_button = '#recaptcha-verify-button'
    try_again_error = ".rc-imageselect-incorrect-response"
    select_more_error = ".rc-imageselect-error-select-more"
    select_new_error = ".rc-imageselect-error-select-something"
    # image_link = (By.TAG_NAME, "img")
    # image_link = "//div[contains(@class,'rc-imageselect')]//img"
    image_link = "div[class*='rc-imageselect'] img"
    captcha_expired_msg = "//span[contains(., 'challenge expired')]"