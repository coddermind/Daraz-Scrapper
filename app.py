import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time


st.title("Daraz Scraper by Muhammad Abrar")
category_list = ["Feature Phone", "Smart Phones", "Gaming Consoles", "Smart Watches", "Monitors", "Laptops", "Mobile Accessories", "Computer Accessories","Camera Accessories","Wearable Technology","Computer Components","Landline Phones"]

selected_category = st.selectbox(label="Select Category", options=category_list)
number_of_pages = st.number_input("Number of pages you want to scrape", value=1)

url = "https://www.daraz.pk/"

if selected_category == "Feature Phone":
    url += "featurephones/"
elif selected_category == "Smart Phones":
    url += "smartphones/"
elif selected_category == "Gaming Consoles":
    url += "gaming-consoles/"
elif selected_category == "Smart Watches":
    url += "smart-watches/"
elif selected_category == "Monitors":
    url += "monitors/"
elif selected_category == "Laptops":
    url += "laptops"
elif selected_category == "Mobile Accessories":
    url += "mobiles-tablets-accessories/"
elif selected_category == "Computer Accessories":
    url += "computing-peripherals-accessories/"
elif selected_category=="Camera Accessories":
    url+="camera-accessories/"
elif selected_category=="Wearable Technology":
    url+="wearable-technology/"
elif selected_category=="Computer Components":
    url+="components-spare-parts/"
elif selected_category=="Landline Phones":
    url+="corded-phones/"

if st.button("Scrape Data"):
    while st.spinner("Scrapping..."):
        # Set up Selenium WebDriver options
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
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
                    link=item.find("a",class_="")["href"]
                    price = item.find("div", class_="aBrP0").get_text(strip=True) if item.find("div", class_="aBrP0") else "N/A"
                    sold = item.find("div", class_="_6uN7R").get_text(strip=True) if item.find("div", class_="_6uN7R") else "N/A"
                    
                    # Store the extracted data in a dictionary
                    context = {
                        "Title on Daraz": name,
                        "Price": price,
                        "Pieces Sold": sold,
                        "Product Link":link
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
