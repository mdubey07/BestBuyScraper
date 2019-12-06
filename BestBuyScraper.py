import requests, re, csv
from bs4 import BeautifulSoup
from collections import Counter
from unidecode import unidecode
import json

person = '{"name": "Bob", "languages": ["English", "Fench"]}'
person_dict = json.loads(person)
# Output: {'name': 'Bob', 'languages': ['English', 'Fench']}
print(person_dict)
# Output: ['English', 'French']
print(person_dict['languages'][0])

exit(0)

#Parses user input to correct query string format
def parseInput(mystring):
    # Removing extra spaces (if any)
    mystring = mystring.strip()
    while '  ' in mystring:
        mystring = mystring.replace('  ', ' ')
    return mystring.replace(' ', '%20')


list_brands = []
list_avg_rating = []
list_num_ratings = []
file_name = 'products.csv'
fr = open(file_name, 'w')
csv_headers = 'Product_name, Rating, Reviews\n'
fr.write(csv_headers)
front_url = "https://www.bestbuy.com/site/searchpage.jsp?cp="
page_count = 1
middle_url = "&searchType=search&st="
user_input = parseInput(input("Enter search term please:"))
search_term = user_input
end_url = "&_dyncharset=UTF-8&id=pcat17071&type=page&sc=Global&nrp=&sp=&qp=&list=n&af=true&iht=y&intl=nosplash&usc=All%20Categories&ks=960&keys=keys"
url = front_url + str(page_count) + middle_url + search_term + end_url
print(url)
agent = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}

# While the next page exists:
while True:
    page = requests.get(url, headers=agent, timeout=50)
    if page.status_code == 200:
        print(page.status_code)
        soup = BeautifulSoup(page.text, "html.parser")
        print('Page ' + str(page_count))
        # print(soup.prettify())

        products = soup.find_all("li", {"class": "sku-item"})
        # Do all scraping when we have products
        if products:
            for product in products:
                title_container = product.findAll("div", {"class": "sku-title"})
                new_product_indicator = title_container[0].findAll("span", {"class": "new-indicator"})
                product_name = title_container[0].text
                product_name = unidecode(product_name)
                if new_product_indicator:
                    print("New Product Found")
                    rating = '0'
                    reviews = 'New Product'
                else:
                    reviews_stats_container = product.findAll("ul", {"class": "reviews-stats-list"})
                    if reviews_stats_container:
                        rating = reviews_stats_container[0].find("i")['alt']
                        if float(rating) > 0:
                            reviews = reviews_stats_container[0].find('span', 'c-total-reviews')
                            reviews = re.findall(r'\d+', reviews.text)
                            reviews = reviews[0]
                        else:
                            reviews = reviews_stats_container[0].find('span', 'c-reviews-none')
                            reviews = reviews.text
                    else:
                        print("useless, nothing found as reviews or rating")
                        rating = '0'
                        reviews = 'Product-We can not make reviews'

                fr.write(product_name.replace(',', '|') + ',' + rating + ',' + str(reviews) + '\n')
                # print('Rating = ' + rating + ' and ' + 'Reviews = ' + str(reviews))

        else:
            print("No product Found based on search terms")
            break

        page_count += 1

        # checking the paging and updating the url
        paging_container = soup.find_all("div", {"class": "right-side"})
        if paging_container:
            next_container = paging_container[0].find("a", {"class": "ficon-caret-right"})
            if next_container:
                if next_container.has_attr('class') and next_container['class'][0] == 'disabled':
                    print("found and next page disabled")
                    break
                else:
                    print("found and next page enabled")
                    url = front_url + str(page_count) + middle_url + search_term + end_url
            else:
                print("Again no paging")
                break
        else:
            print("no paging exist")
            break
    else:
        print(page.status_code)
        print("Web Server not reachable due to " + str(page.status_code))
        break


    # print(next_container)
#Inputting into csv file
# with open('data.csv', 'w', newline='') as mycsv:
#     writer = csv.writer(mycsv)
#     writer.writerow(list_brands)
#     writer.writerow(list_avg_rating)
#     writer.writerow(list_num_ratings)
#     dict_writer = csv.DictWriter(mycsv, Counter(list_brands).keys())
#     dict_writer.writeheader()
#     dict_writer.writerow(Counter(list_brands))

