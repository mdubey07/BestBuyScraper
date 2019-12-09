import requests
import re
import socket
from bs4 import BeautifulSoup
from unidecode import unidecode
import json
import time
import sys
from multiprocessing import pool
from multiprocessing.dummy import Pool  # This is a thread-based Pool
from multiprocessing import cpu_count
import csv


remote_url = "www.bestbuy.com"
p_name = []
p_cat = []
p_scat = []
p_key = []
p_rating = []
p_review = []
p_url = []


def is_connected(hostname):
    try:
        host = socket.gethostbyname(hostname)
        s = socket.create_connection((host, 80), 2)
        s.close()
        return True
    except Exception as exc:
        print(exc)
        pass
    return False


file_name = 'products.csv'
fr = open(file_name, 'w')
csv_headers = 'Product_name, Category, Subcategory, SearchTerm, Rating, Reviews, Product_Url\n'
fr.write(csv_headers)

front_url = "https://www.bestbuy.com/site/searchpage.jsp?cp="
middle_url = "&searchType=search&st="
end_url = "&_dyncharset=UTF-8&id=pcat17071&type=page&sc=Global&nrp=&sp=&qp=&list=n&af=true&iht=y&intl=nosplash&usc=All%20Categories&ks=960&keys=keys"
agent = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}


# Parses user input to correct query string format
def parse_input(mystring):
    # Removing extra spaces (if any)
    mystring = mystring.strip()
    while '  ' in mystring:
        mystring = mystring.replace('  ', ' ')
    return mystring.replace(' ', '%20')


def search_result(search_term_list):
    page_count = 1
    str1 = search_term_list[0]
    searchname = search_term_list[0].strip()
    search_term = parse_input(searchname)
    url = front_url + str(page_count) + middle_url + search_term + end_url
    # While the next page exists:
    while True:
        wnt_process("Checking before calling request")
        try:
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
                        product_url = title_container[0].find_all('a', href=True)
                        product_url = 'https://www.bestbuy.com' + product_url[0]['href']
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
                                    reviews = re.findall(r'\d+,?', reviews.text.replace(',', ''))
                                    reviews = reviews[0]
                                else:
                                    reviews = reviews_stats_container[0].find('span', 'c-reviews-none')
                                    reviews = reviews.text
                            else:
                                print("useless, nothing found as reviews or rating")
                                rating = '0'
                                reviews = 'Product-We can not make reviews'

                        p_name.append(product_name.replace(',', '|'))
                        p_cat.append(search_term_list[1])
                        p_scat.append(search_term_list[2])
                        p_key.append(searchname)
                        p_rating.append(rating)
                        p_review.append(str(reviews))
                        p_url.append(product_url)
                        # fr.write(product_name.replace(',', '|') + ',' + search_term_list[1] + ',' + search_term_list[2] + ',' + searchname
                        #          + ',' + rating + ',' + str(reviews) + ',' + product_url + '\n')
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
                            print("found and next page enabled and going to iterate next page")
                            url = front_url + str(page_count) + middle_url + search_term + end_url
                            # time.sleep(1)
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
        except requests.exceptions.Timeout:
            print("TimeOut Occurred")
        except Exception as ex:
            print(ex)
            print("Oops!", sys.exc_info()[0], "occurred.")
            pass
    return p_name


def wnt_process(message):
    print(message)
    if is_connected(remote_url) is True:
        print(is_connected(remote_url))
        time.sleep(1)
        # wnt_process()
    else:
        attempt = 1
        while is_connected(remote_url) is False:
            wait_time = .5 * attempt
            print("waiting the connection for " + str(wait_time) + " Second")
            time.sleep(wait_time)
            attempt += 1
        wnt_process("Self Retrying...")


# with open('output.json', encoding="utf8") as jsonFile:
#     jsonData = json.load(jsonFile)
#     key_count = 1
#     # key_parameter = []
#     for data in jsonData:
#         search_name = data['name']
#         cat = data['category']
#         sub_cat = data['subcategory']
#         try:
#             if search_name is not None:
#                 if search_name.lower != 'none':
#                     print(str(key_count) + " Keyword is " + search_name)
#                     # search_name = 'android'
#                     key_parameter = [search_name, cat, sub_cat]
#                     p = pool.Pool(10)
#                     test_result = p.map(search_result, key_parameter)
#                     p.terminate()
#                     p.join()
#                     # search_result(key_parameter)
#                     # print("will iterate after 0 second!")
#         except Exception as e:
#             print(e)
#             print("Oops1!", sys.exc_info()[0], "occured.")
#             pass
#         key_count += 1


if __name__ == "__main__":
    key_parameter = ['android', 'test', 'sub test']
    pool = Pool(cpu_count() * 2)  # Creates a Pool with cpu_count * 2 threads.
    results = pool.map(search_result, key_parameter)  # results is a list of all the placeHolder lists returned from each call to crawlToCSV
    with open("products1.csv", "ab") as f:
        writeFile = csv.writer(f)
        for result in results:
            writeFile.writerow(result)

fr.close()
