# Import required libraries
import pandas as pd
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

# Define the CSV file containing the product data.
csv_file = r"C:\Users\marpa\Desktop\python\Products_1.csv"


# Read the data from the CSV file into a DataFrame.
df = pd.read_csv(csv_file)

# Initialize a new DataFrame to store reviews with columns for product, review, rating, and more.
reviews_df = pd.DataFrame(columns=['Product_URL', 'Review_Title', 'Review_Body', 'Rating'])

# Function to scrape reviews using Playwright
def scrape_reviews(page, url):
    # Store the reviews in a temporary list
    temp_reviews = []

    # Wait for the reviews section to load
    page.wait_for_selector('div[class*="cPHDOP col-12-12"]')  # Adjust selector for the website
    
    # Scroll down to load all reviews (if necessary)
    page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
    page.wait_for_timeout(3000)  # Wait for content to load

    # Try clicking the "View More Reviews" button if it exists
    try:
        more_reviews_button = page.locator('//span[contains(text(), "View More Reviews")]')
        if more_reviews_button.is_visible():
            more_reviews_button.click()
            page.wait_for_timeout(2000)  # Wait for the reviews to load
    except:
        print("No 'View More Reviews' button found.")

    # Get the page content and parse it with BeautifulSoup
    html = page.content()
    soup = BeautifulSoup(html, 'html.parser')

    # Find all review containers
    review_containers = soup.find_all('div', class_='cPHDOP col-12-12')  # Adjust class based on actual structure

    # Loop through the review containers and extract details
    for review in review_containers:
        try:
            review_title = review.find('p', class_='z9E0IG').text.strip()  # Extract review title
        except:
            review_title = "No title"

        # try:
        #     review_body = review.find('div', class_='t-ZTKy').text.strip()  # Extract review body
        # except:
        #     review_body = "No review body"

        # try:
        #     rating = review.find('div', class_='_3LWZlK').text.strip()  # Extract rating
        # except:
        #     rating = "No rating"

        # Append the review data to the temp list
        temp_reviews.append({
            'Product_URL': url,
            'Review_Title': review_title,
            # 'Review_Body': review_body,
            # 'Rating': rating
        })

    return temp_reviews

# Main script to scrape reviews from multiple product URLs
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)  # Set to False for debugging
    for index, row in df.iterrows():

        # Limit the number of URLs processed (optional, here set to 5).
        if index >= 5:
            break

        # Get the URL for the current product
        url = row['Product Url']
        print(f"Processing product {index + 1}: {url}")

        # Create a new browser page
        page = browser.new_page()

        try:
            # Navigate to the product URL
            page.goto(url)

            # Scrape reviews from the product page
            product_reviews = scrape_reviews(page, url)
            print(product_reviews)
            # Append the reviews to the reviews DataFrame
            # reviews_df = reviews_df.append(product_reviews, ignore_index=True)

        # except Exception as e:
        #     print(f"Error processing product {index + 1}: {e}")

        finally:
            # Close the page after processing each product
            page.close()

    # Close the browser
    browser.close()

# Save the reviews to a new CSV file
# output_csv_file = "Product_Reviews_Playwright.csv"
# reviews_df.to_csv(output_csv_file, index=False)

# print(f"Reviews saved to {output_csv_file}")

