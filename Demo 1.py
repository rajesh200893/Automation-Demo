import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sbvt import VisualTest

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def setup_driver():
    """Sets up the WebDriver."""
    driver = webdriver.Chrome()
    logging.info("WebDriver initialized successfully.")
    return driver

def accept_cookies(driver):
    """Accept cookies if the popup is present."""
    try:
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Accept cookies']"))).click()
        logging.info("Cookies accepted successfully.")
    except Exception as e:
        logging.info("No cookies popup to accept or already accepted. Skipping.")

def perform_visual_test(driver, page_name):
    """Performs visual testing on the given page."""
    try:
        visual_test = VisualTest(driver, {'projectToken': 'XvOGPPvK/VKX14VrtDzY='})
        visual_test.capture(page_name, {'lazyload': 1000})
        visual_test.printReport()
        result = visual_test.getTestRunResult()
        assert result['failed'] == 0, f"VisualTest comparison failed on {page_name}"
        logging.info(f"VisualTest passed for {page_name}.")
    except AssertionError as ae:
        logging.error(ae)  # Log assertion errors
    except Exception as e:
        logging.error(f"An error occurred during visual testing on {page_name}: {e}")

def main():
    # Define the list of pages to test
    pages = [
        ("https://www.crodabeauty.com/en-gb", "Beauty Global - Homepage"),
        ("https://www.crodabeauty.com/en-gb/products?currentPage=1&pageSize=20&sortBy=recommended&lang=en-gb", "Beauty Global - Product Finder Page"),
        ("https://www.crodabeauty.com/en-gb/products/product/5780-solaveil_1_ct-60w", "Beauty Global - Product Details Page")
    ]

    driver = None
    try:
        driver = setup_driver()
        for url, page_name in pages:
            logging.info(f"Navigating to: {url}")
            driver.get(url)
            accept_cookies(driver)
            perform_visual_test(driver, page_name)
            time.sleep(2)  # Allow a small delay before navigating to the next page
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    finally:
        if driver:
            driver.quit()
            logging.info("WebDriver closed successfully.")

if __name__ == "__main__":
    main()
