from bs4 import BeautifulSoup
import urllib.request
import csv
import requests

fileNumber = 0
file_name = 'products.csv'
fr = open(file_name, 'w')
csv_headers = 'Product_name, Description, Product_Price\n'
fr.write(csv_headers)
agent = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
url = 'https://www.etsy.com/in-en/listing/739028044/the-evermore-rose-deep-red-ecuadorian'

def productScrape():
    global fieldsWritten
    global fileNumber
    # page = urllib.request.urlopen(url)
    page = requests.get(url, headers=agent, timeout=50)
    soup = BeautifulSoup(page.text, "html.parser")
    # soup = BeautifulSoup(page.read(), "html.parser")

    quantity = 1

    # Field values
    # title = soup.find("span", {"itemprop": "name"}).text
    title_container = soup.find("div", {"class": "listing-page-title-component"})
    print(title_container)
    title = title_container.findAll("h1", {"class": "normal"})
    title = title[0].text
    desc = soup.find("div", {"id": "description-text-content-toggle"})
    description = desc.find("span").text
    # price = soup.find(itemprop="price").get("content")
    price = soup.find("span", {"class": "override-listing-price"}).text
    fr.write(title + ',' + description + ',' + price + '\n')
    # currencyCode = soup.find(itemprop="currency").get("content")
    # materials = soup.find("span", {"id":"overview-materials"} ).text
    # Quantity
    # for selector in soup.find_all("select", {"id": 'inventory-select-quantity'}):
    #     for child in selector.find_all('option'):
    #         quantity = child.string
    #
    # # Tags
    # tags = []
    # for selector in soup.find_all("ul", {"id": 'listing-tag-list'}):
    #     for child in selector.find_all('li'):
    #         tags.append(child.text.replace("\n", ""))
    # tags = str.join(', ', tags)

    # Images
    # images = []
    # carouseEntries = soup.select("#image-carousel > li")
    # for image in carouseEntries: images.append(image.get('data-full-image-href'))
    #
    # # Variant categories
    # variantRawCategories = soup.find_all("label")
    # variationCategories = []
    # for category in variantRawCategories:
    #     if 'inventory-variation-select' in str((category.get('for'))):
    #         variationCategories.append(category.text)
    #
    # # Variant choices (or values)
    # variationValuesRaw = soup.find_all("select", {"class": "variation-select"})
    # variationValues = []
    # currentList = []
    # for value in variationValuesRaw:
    #     valueList = value.text
    #     valueList = valueList.split('\n')
    #     newValueList = [x for x in valueList if str(x) != 'Select an option']
    #     variationValues.append(newValueList[1:len(valueList) - 2])
    # for i in range(0, len(variationValues)):
    #     for x in range(0, len(variationValues[i])): variationValues[i][x] = variationValues[i][x].replace(",", "")
    #     variationValues[i] = str.join(",", variationValues[i])
    #
    # # Image fields/values
    # fields = [["TITLE", "DESCRIPTION", "PRICE", "QUANTITY", "TAGS"]]
    # values = [[title, description, price, quantity, tags]]
    # # Add image fields
    # for i in range(1, len(images) + 1):
    #     fields[0].append("IMAGE" + str(i))
    #     values[0].append(images[i - 1])
    #
    # # Variation fields/values
    # for i in range(1, len(variationCategories) + 1):
    #     # fields[0].append("VARIATION " + str(i) + " TYPE")
    #     fields[0].append("VARIATION " + str(i) + " NAME")
    #     fields[0].append("VARIATION " + str(i) + " VALUES")
    #     # values[0].append("Color")
    #     values[0].append(variationCategories[i - 1])
    #     values[0].append(variationValues[i - 1])

    # fields = [["TITLE", "DESCRIPTION", "PRICE"]]
    # values = [[title, description, price]]
    #
    # csvName = 'file' + str(fileNumber)
    # with open(csvName + '.csv', 'w', newline='', encoding="utf8") as csvfile:
    #     writer = csv.writer(csvfile)
    #     writer.writerows(fields)
    #     writer.writerows(values)
    # csvfile.close()


productScrape()

# with open('links.txt', 'r', encoding="utf8") as links:
#     for url in links:
#         productScrape(url)
#         fileNumber = fileNumber + 1
