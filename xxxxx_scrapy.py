import scrapy
import json


class xxxxxScrapySpider(scrapy.Spider):
    name = "xxxxx_scrapy"
    allowed_domains = ["www.xxxxx.com"]
    start_urls = ["https://www.xxxxx.com"]
    

    def parse(self, response):
        animals = response.xpath("//ul[@class='mobile-sub wsmenu-list']/li/a[@class='navtext nav-bigger']")
        animalList = []

        try:
            with open("xxxxx_products.json", "x") as json_file:
                json.dump([], json_file)
        except FileExistsError:
            pass

        for animal in animals:
            animal_name = animal.xpath(".//span/text()").get()
            animal_name = animal_name.strip().lower()
            animalList.append(animal_name)
            newUrl = "http://www.xxxxx.com/" + animal_name + "-petshop-urunleri"
            
            yield scrapy.Request(newUrl, callback=self.parse_page2)
        
        
    def parse_page2(self, response):
        products = response.xpath("//div[@class='row listitempage']/div/div")
        for product in products:
                product_url = product.xpath(".//div[@class='card-body pb-0 pt-2 pl-3 pr-3']/a/@href").get()
                product_info = product.xpath(".//div[@class='card-body pb-0 pt-2 pl-3 pr-3']/a/@data-gtm-product").get()
                try:
                    product_info1 = json.loads(product_info)
                    product_image = product.xpath(".//div[@class ='col-md-12']/center/img/@data-original").get()
                    
                    dict = {
                        "product url": product_url,
                        "product name": product_info1["name"],
                        "product price": product_info1["price"],
                        "product stock": product_info1["quantity"],
                        "product image": product_image,
                        "category": product_info1["category"],
                        "product id": product_info1["id"],
                        "brand": product_info1["brand"],
                        "product barcode": "",
                        "description": "",
                        "sku": ""
                    }

                    

                    with open("xxxxx_products.json", "r", encoding='utf-8') as json_file:
                        products_list = json.load(json_file)

                    products_list.append(dict)

                    with open("xxxxx_products.json", "w", encoding='utf-8') as json_file:
                        json.dump(products_list, json_file, indent=4)
                    

                except Exception as e:
                    pass 
        nextPageUrl = response.xpath("//a[@rel='next']/@href").extract_first()
        if nextPageUrl:
            yield response.follow(nextPageUrl, callback=self.parse_page2)

