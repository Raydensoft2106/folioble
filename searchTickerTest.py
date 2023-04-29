from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Set up the web driver (make sure to download the appropriate driver for your browser)
driver = webdriver.Chrome()

# Navigate to the Yahoo Finance website
driver.get('https://finance.yahoo.com/')

# Find the search bar element and enter the keyword to search for
search_bar = driver.find_element_by_xpath('//*[@id="header-search-input"]')
search_bar.send_keys('gold')
search_bar.send_keys(Keys.RETURN)

# Wait for the search results to load and find the first search result
driver.implicitly_wait(10)  # Wait for up to 10 seconds for the search results to load
search_results = driver.find_elements_by_xpath('//*[@id="quote-header-info"]/div[2]/div[1]/div[1]/h1')
if search_results:
    first_result = search_results[0].text
    # Extract the ticker symbol from the search result (assuming it is in the format "LONG NAME (TICKER SYMBOL)")
    ticker = first_result.split(' ')[-1].strip('()')
    print(f"The top resulting ticker for 'gold' is {ticker}.")
else:
    print("No search results found.")
    
# Close the web driver
driver.quit()
