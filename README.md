# Most recurring words in Open Library titles

This project uses the API provided by [OpenLibrary](https://openlibrary.org/) and saves them in a NoSQL database, then searches for the 10 most recurring words in the titles.

## Getting Started/Development

The search API returns a JSON file, but has a restriction that searches the result in 1000 items per request. However, it has the total result information, so a class has been implemented to perform data collection between all pages.

The script was also parameterized, and could for one or more words. Parameterization of other configurations, such as the database, the n-top words and the api access host are found in the config.ini file.

### api_open_library.py

Class responsible for searching in the OpenLibrary API. The API alone allows a maximum of 1000 results per request. Collect data on all pages and group them all into a resulting list.

### main.py

Main module that reads config.ini with the parameters, uses the Api class, saves all the data in MongoDB and searches for the main words.


### Libraries
* Pandas
* Urllib3
* ProgressBar2
* PyMongo

### Prerequsites

MongoDB database must be installed.

Link: [https://docs.mongodb.com/manual/installation/](https://docs.mongodb.com/manual/installation/)

### Installing

All the libraries needed to perform the problem are in the require.txt file.

```
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
```

## Running

```
python3 main.py [query ...]
```

Example

```
python3 main.py lord
```

```
python3 main.py lord of the rings
```

## Results

For the search of the Lord, the 10 most recurring words (word - no. occurrences):
* LORD'S - 1898
* LETTER - 1381
* HONOURABLE - 1219
* SERMON - 1174
* CHRIST - 1122
* BISHOP - 1112
* CHURCH - 1034
* PARLIAMENT - 1033
* BEFORE - 965
* LETTERS - 902

## Authors

* **Leonardo Sousa** - [SousaL](https://github.com/SousaL)
