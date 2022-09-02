# fa21-cs242-assignment_2

## my implementation

* The beautiful soup is used for scraping
 * there are functions working on extract one attribute from author or book accordingly.
 * there are Author and Book class to hold the attributes for author page and book page respectively.
 * in each iteration of the loop in my main, every attribute of book or author will be scraped from the the web page, and they will be imported into the database at the end of the iteration.
 Also there find_next_url function for both author and book that decides the next web page to scrape.
 * There are functions that can convert attribute into json or convert json into a tuple pf attributes.
 * database can be exported into json file and json file can be imported into database.
 * implemented multi-thread to speed up the process of scraping

## Usage

#### implementation detail
* with correct starting url, book counts and author as parameter, the scraper.py will scrape books and author up both counts. This is accomplished by a while loop that keeps check the remaining book count or author count. And in each iteration, a web page will be scraped. Also, at each iteation, the scraped data will be sent to the mysql database.
* the read and write of database is accomplished by two sets of converter. what converter does is basically converting json type into a tuple that contains every attribute or converting such tuple into json type. 

#### How to Run
* scrapy.py
* scraping: python /backend/scraper.py <url> <book_count> <author_count>
* GET book: python /backend/scraper.py <url> <book_count> <author_count> GET book <book_id>
* GET author: python /backend/scraper.py <url> <book_count> <author_count> GET author <author_id>
* GET by search: python /backend/scraper.py <url> <book_count> <author_count> GET search <query_line>. For example run scrape.py https://www.goodreads.com/book/show/6091075-so-long-and-thanks-for-all-the-fish 200 200 GET search books.rating:NOT3ANDbooks.review_count:>1234. the query_line should contain no space.
* PUT book: python /backend/scraper.py <url> <book_count> <author_count> PUT book <book_id> <key> <value>. key is the field name in the database, value is the value to update.
* PUT author: python /backend/scraper.py <url> <book_count> <author_count> PUT author <author_id> <key> <value>. key is the field name in the database, value is the value to update.
* POST scrape: python /backend/scraper.py <url> <book_count> <author_count> POST scrape <url>.
* POST book: python /backend/scraper.py <url> <book_count> <author_count> POST book <json that represent rows>.
* POST author: python /backend/scraper.py <url> <book_count> <author_count> POST author <json string that represents rows>.
* delete author: python /backend/scraper.py <url> <book_count> <author_count> DELETE author <author_id>.
* delete book: python /backend/scraper.py <url> <book_count> <author_count> DELETE book <book_id>.

#### how to start backend and frontend
*first of all, open mysql and log in into the database.
*(backend)go to ../backend/src/, and run api.py.
*(frontend)go to ../frontend/react_front, enter command line "npm start".


