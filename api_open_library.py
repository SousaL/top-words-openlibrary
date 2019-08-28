"""
Author  Leonardo Pedro da Silva de Sousa
Date    26/08/2019
"""
import json
import urllib3
import progressbar
from loguru import logger

class ApiOpenLibrary:
    """Class responsible for obtaining OpenLibrary Api data
    """

    def __init__(self, src):
        self.__src = src
        self.__limit = 1000

    def query(self, text, max_pages=-1):
        """ Performs search.

        Args:
            text: the consultation to make.
            max_pages: if you want to restrict the number of pages.

        Returns:
            A concatenated list of all pages for the query made.
        """
        n_pages = self.__number_pages(text)

        logger.info(f'Total pages = {n_pages}')

        data = []

        pg_bar = progressbar.ProgressBar(max_value=n_pages)

        for i in range(n_pages + 1):
            response = self.__get_data(text, i)
            data += response
            if max_pages > 0 and i + 1 > max_pages:
                break

            pg_bar.update(i)

        return data

    def __number_pages(self, text):
        http = urllib3.PoolManager()
        query = text.strip().replace(" ", "+")
        request_addr = f'{self.__src}?q={query}&offset=0&limit=0'
        response = http.request('GET', request_addr)
        data = json.loads(response.data)

        number_pages = int(int(data['num_found']) / self.__limit)

        return number_pages

    def __get_data(self, text, page=0):
        http = urllib3.PoolManager()
        query = text.strip().replace(" ", "+")
        request_addr = f'{self.__src}?q={query}&offset={page * self.__limit}&limit={self.__limit}'

        while True:
            response = http.request('GET', request_addr)
            if response.status == 200:
                data = json.loads(response.data)
                docs = data["docs"]
                return docs
