from typing import List

import scrapy
from scrapy import Selector


class RwidSpider(scrapy.Spider):
    name = 'rwid'
    allowed_domains = ['127.0.0.1']


    start_urls = ['http://127.0.0.1:5000/']

    def parse(self, response):
        # beda yield & return
        ## kalo yield contoh ada list_data = [] maka dia akan mereturn generator

        # yield{"title": response.css("title::text").get()}

        data = {
            "username" : "user",
            "password" : "user12345"
        }

        return scrapy.FormRequest(
            url = "http://127.0.0.1:5000/login",
            formdata = data,
            callback = self.after_login
        )

    def after_login(self, response):
        """
        2 task disini :

        1. ambil semua data barang yg ada di halaman hasil -> akan menuji detail (parsing detail)
        2. ambil semua link next -> akan kembali ke after_login

        :param response:
        :return:
        """

        # Task 1 : get detail products
        detail_products: List[Selector] = response.css(".card .card-title a")
        for detail in detail_products:
            href = detail.attrib.get("href")
            yield response.follow(href, callback=self.parse_detail)


        # Task 2 : Get Pagination

        paginations: List[Selector] = response.css(".pagination a.page-link")
        for pagination in paginations:
            href = pagination.attrib.get("href")
            yield response.follow(href, callback=self.after_login)

    def parse_detail(self,response):
        """"
        Fungsi/Method ini digunakan untuk mengambil text dari title, stock, dan description
        dan juga untuk mengambil URL dari image
        """
        image = response.css(".card-img-top").attrib.get("src")
        title = response.css(".card-title::text").get()
        stock = response.css(".card-stock::text").get()
        description = response.css(".card-text::text").get()


        return {
            "image" : image,
            "title" : title,
            "stock" : stock,
            "description" : description
        }

        # yield {"title": response.css("title::text").get()}
        # pass

