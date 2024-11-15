import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time
import subprocess
import os

# Install Google Chrome and ChromeDriver
def install_chrome_driver():
    if not os.path.exists("/usr/bin/google-chrome"):
        subprocess.run("wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb", shell=True)
        subprocess.run("apt-get update && apt-get install -y ./google-chrome-stable_current_amd64.deb", shell=True)
    if not os.path.exists("/usr/bin/chromedriver"):
        subprocess.run("wget -N https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip", shell=True)
        subprocess.run("unzip -o chromedriver_linux64.zip -d /usr/bin/", shell=True)
        subprocess.run("chmod +x /usr/bin/chromedriver", shell=True)

install_chrome_driver()

# Set up Streamlit interface
st.title("Daraz Scraper by Muhammad Abrar")
category_list = [
    "Feature Phone", "Smart Phones", "Gaming Consoles", "Smart Watches", "Monitors",
    "Laptops", "Mobile Accessories", "Computer Accessories", "Camera Accessories",
    "Wearable Technology", "Computer Components", "Landline Phones"
]

selected_category = st.selectbox(label="Select Category", options=category_list)
number_of_pages = st.number_input("Number of pages you want to scrape", value=1)

# Category URL Mapping
url = "https://www.daraz.pk/"
category_urls = {
    "Feature Phone": "featurephones/",
    "Smart Phones": "smartphones/",
    "Gaming Consoles": "gaming-consoles/",
    "Smart Watches": "smart-watches/",
    "Monitors": "monitors/",
    "Laptops": "laptops",
    "Mobile Accessories": "mobiles-tablets-accessories/",
    "Computer Accessories": "computing-peripherals-accessories/",
    "Camera Accessories": "camera-accessories/",
    "Wearable Technology": "wearable-technology/",
    "Computer Components": "components-spare-parts/",
    "Landline Phones": "corded-phones/"
}
url += category_urls.get(selected_category, "")

# Scraping process
if st.button("Scrape Data"):
    with st.spinner("Scraping..."):
        # Set up Selenium WebDriver
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.binary_location = "/usr/bin/google-chrome"
        
        driver = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=chrome_options)
        products = []

        try:
            # Loop over pages
            for page in range(1, int(number_of_pages) + 1):
                driver.get(f"{url}?page={page}")
                time.sleep(5)  # Allow time for the page to load
                
                # Get HTML content rendered by Selenium
                page_html = driver.page_source
                soup = BeautifulSoup(page_html, "html.parser")
                
                # Locate and extract product details
                for item in soup.find_all("div", class_="buTCk"):
                    name = item.find("div", class_="RfADt").get_text(strip=True) if item.find("div", class_="RfADt") else "N/A"
                    link = item.find("a", class_="")["href"] if item.find("a", class_="") else "N/A"
                    price = item.find("div", class_="aBrP0").get_text(strip=True) if item.find("div", class_="aBrP0") else "N/A"
                    sold = item.find("div", class_="_6uN7R").get_text(strip=True) if item.find("div", class_="_6uN7R") else "N/A"
                    
                    # Store the extracted data in a dictionary
                    context = {
                        "Title on Daraz": name,
                        "Price": price,
                        "Pieces Sold": sold,
                        "Product Link": "https://www.daraz.pk" + link if link != "N/A" else "N/A"
                    }
                    products.append(context)
                    
        finally:
            # Close the WebDriver
            driver.quit()
    
        # Display the data
        if products:
            df = pd.DataFrame(products)
            st.dataframe(df)
            # Optionally, save to CSV
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name='daraz_data.csv',
                mime='text/csv',
            )
        else:
            st.write("No products found.")
