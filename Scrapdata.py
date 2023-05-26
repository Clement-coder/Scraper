import csv
import requests
from bs4 import BeautifulSoup
import time

base_url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_'

# Create and open the CSV file
with open('product_details.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews', 'Description', 'ASIN', 'Product Description', 'Manufacturer'])

    # Scrape 20 pages of product listings
    for page in range(1, 21):
        url = base_url + str(page)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        product_containers = soup.find_all('div', {'data-component-type': 's-search-result'})

        for container in product_containers:
            # Extract product URL
            product_url_suffix = container.find('a', class_='a-link-normal s-no-outline')['href']
            product_url = 'https://www.amazon.in' + product_url_suffix if product_url_suffix.startswith('/') else product_url_suffix
            # Extract product name
            product_name = container.find('span', class_='a-size-medium a-color-base a-text-normal').text.strip()
            # Extract product price
            product_price_element = container.find('span', class_='a-offscreen')
            product_price = product_price_element.text.strip() if product_price_element else 'No price available'

            # Check if rating is available
            rating = container.find('span', class_='a-icon-alt')
            if rating:
                rating = rating.text.strip()
            else:
                rating = 'Not available'

            # Check if number of reviews is available
            reviews = container.find('span', class_='a-size-base s-underline-text')
            if reviews:
                reviews = reviews.text.strip()
            else:
                reviews = 'No reviews'

            # Hit each product URL to scrape additional information
            product_response = requests.get(product_url)
            product_soup = BeautifulSoup(product_response.content, 'html.parser')

            # Add delay to allow the page to load
            #time.sleep(3)

            # Extract description
            description_element = product_soup.find('div', {'class': 'a-section a-spacing-medium a-spacing-top-small'})
            description = description_element.get_text(separator=' ').strip() if description_element else 'No description available'

            # Extract ASIN
            asin = product_url.split('/')[-1]

            # Extract product description
            product_description_element = product_soup.find('div', {'id': 'productDescription'})
            product_description = product_description_element.get_text(separator=' ').strip() if product_description_element else 'No product description available'

            # Extract manufacturer
            words = product_name.split()

            if len(words) >= 2 and words[1][0].isdigit():
                manufacturer= words[0]
            else:
                manufacturer= " ".join(words[:2])


            # Print or further process the scraped information
            print("Product URL:", product_url)
            print("Product Name:", product_name)
            print("Product Price:", product_price)
            print("Rating:", rating)
            print("Number of Reviews:", reviews)
            print("Description:", description)
            print("ASIN:", asin)
            print("Product Description:", product_description)
            print("Manufacturer:", manufacturer)
            print()

            # Write the scraped information to the CSV file
            writer.writerow([product_url, product_name, product_price, rating, reviews, description, asin, product_description, manufacturer])

            # Pause the loop for a few seconds to avoid overwhelming the server
            #time.sleep(3)
