import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
from tqdm import tqdm


def init_driver():
    """Initialize and return a Chrome WebDriver."""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Optional: run in headless mode
    service = Service()  # You can pass path to chromedriver if needed
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def get_total_pages(driver, base_url):
    """Return total number of pagination pages available."""
    driver.get(base_url)
    time.sleep(3)
    html_data = BeautifulSoup(driver.page_source, "html.parser")
    last_page = html_data.find("span", {'class': 's-pagination-item s-pagination-disabled'})
    return int(last_page.text.strip()) if last_page else 1


def extract_product_data(product):
    """Extract product details from a single product element."""
    title_tag = product.h2.find("span") if product.h2 else None
    title = title_tag.text.strip() if title_tag else None

    img_tag = product.find("img", {'class': 's-image'})
    image = img_tag['src'] if img_tag else None

    rating_tag = product.find('span', {'class': 'a-icon-alt'})
    try:
        rating = float(rating_tag.text.strip().split()[0]) if rating_tag else None
    except:
        rating = None

    price_tag = product.find('span', {'class': 'a-price-whole'})
    price = '₹' + price_tag.text.strip() if price_tag else None

    link_tag = product.find('a', {'class': 'a-link-normal s-line-clamp-2 s-link-style a-text-normal'})
    url = 'https://www.amazon.in' + link_tag['href'] if link_tag else None

    return title, image, price, rating, url


def scrape_amazon_products(driver, base_url, total_pages):
    """Scrape all product data from paginated search results."""
    titles, images, prices, ratings, urls = [], [], [], [], []

    for i in tqdm(range(total_pages), desc="Scraping pages"):
        url = f"{base_url}&page={i + 1}"
        driver.get(url)
        time.sleep(3)

        html_data = BeautifulSoup(driver.page_source, "html.parser")
        products = html_data.find_all("div", {'data-component-type': 's-search-result'})

        for product in products:
            title, image, price, rating, url = extract_product_data(product)
            titles.append(title)
            images.append(image)
            prices.append(price)
            ratings.append(rating)
            urls.append(url)

    return pd.DataFrame({
        'titles': titles,
        'images': images,
        'prices': prices,
        'ratings': ratings,
        'purls': urls
    })


def save_data_to_csv(df, filename="sunglass.csv"):
    """Save the scraped DataFrame to a CSV file."""
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")


def main():
    base_url = "https://www.amazon.in/s?k=sunglass&crid=389J7CS8RFIK9&sprefix=sungla%2Caps%2C356&ref=nb_sb_noss_2"

    driver = init_driver()
    try:
        total_pages = get_total_pages(driver, base_url)
        print(f"Total number of pages: {total_pages}")

        df = scrape_amazon_products(driver, base_url, total_pages)
        print(df.head())

        save_data_to_csv(df)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
