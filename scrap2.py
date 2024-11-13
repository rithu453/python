from playwright.sync_api import sync_playwright
import pandas as pd

#file 
csv_file = r"C:\Users\marpa\Desktop\python\Products_1.csv" #csv file
df = pd.read_csv(csv_file)
#file saver
output = r"C:\Users\marpa\Desktop\python\output.txt"  

# scrape reviews
def scrape_reviews(page, url):
    temp_reviews = []#return
    page.goto(url)
    page.wait_for_timeout(2000)# page load

    page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
    page.wait_for_timeout(2000)#load for others

    review_containers = page.locator('div.cPHDOP.col-12-12').element_handles() 
    for review in review_containers:

        try:review_title = review.query_selector('p.z9E0IG').inner_text().strip()  
        except:review_title = "No title"

        try:review_body = review.query_selector('div.ZmyHeo').inner_text().strip()  
        except:review_body = "No review body"

            #review data
            # print(f"Product URL: {url}")
        print(f"Review Title: {review_title}")
        print(f"Review Body: {review_body}\n")
        temp_reviews.append({
          # 'Product_URL': url,
            'Review_Title': review_title, #appending in the liust
            'Review_Body': review_body,
            })
        # nextbutton = page.locator('//*[@id="container"]/div/div[3]/div/div/div[2]/div[13]/div/div/nav/a[8]/span')
        # if nextbutton.is_visible():
        #         try:
        #             nextbutton.click()
        #             page.wait_for_timeout(3000)  
        #         except Exception as e:
        #             print(f"Error clicking Next button: {e}")
        #         break
        # else:
        #     break 
    return temp_reviews
#Scrapper code
#multiple product urls(Main function)//*[@id="container"]/div/div[3]/div/div/div[2]/div[13]/div/div/nav/a[8]/span
with sync_playwright() as sp:
    browser = sp.chromium.launch(headless=False)
    with open(output, "w", encoding="utf-8") as f: #false for opening the head gui (browser) 
        for index, row in df.iterrows():
            if index >= 5:
                break
            url = row['Product Url']
            print(f"Processing product {index }: {url}\n")

            page = browser.new_page()

            try:
                reviews= scrape_reviews(page, url)

                for review in reviews:
                    # f.write(f"Product URL: {review['Product_URL']}\n")
                    f.write(f"Review Title: {review['Review_Title']}\n")
                    f.write(f"Review Body: {review['Review_Body']}\n")
                    f.write("\n" + "-"*50 + "\n")

            except Exception as e:
                print(f"Error processing product {index }: {e}")

            finally:
                page.close()

    browser.close()


