# Manual Test Plan

## Table of content
- [1.Introducation](#1introducation)
- [2.Environment Setup](#2environment-setup)
- [3.unittest cases](#3unittest-cases)
- [4.scraping method](#4scraping-method)
    + [4.1.scraping book functions](#41scraping-book-functions)
    + [4.2.scraping author function](#42scraping-author-function)
- [5.database importing method](#5database-importing-method)
- [6.Manual testing strategy](#6manual-testing-strategy)
    + [6.1 verifying scraping result](#61-verifying-scraping-result)
    + [6.2 verifying data imported into database](#62-verifying-data-imported-into-database)
    + [6.3 verifying importing json file and exporting to json file](#63-verifying-importing-json-file-and-exporting-to-json-file)
- [7. Backend Test cases](#7-backend-test-cases)
  * [7.1 scraping test cases](#71-scraping-test-cases)
    + [7.1.1 @test matching rating, rating count and review count](#711--test-matching-rating--rating-count-and-review-count)
    + [7.1.2 @test matching matching other attributes](#712--test-matching-matching-other-attributes)
    + [7.1.3 @test scraping error testing](#713--test-scraping-error-testing)
  * [7.2 importing data to database test cases](#72-importing-data-to-database-test-cases)
    + [7.2.1 @test send data with wrong format into database](#721--test-send-data-with-wrong-format-into-database)
    + [7.2.2 @test database server closed error](#722--test-database-server-closed-error)
    + [7.2.3 @test data matching test](#723--test-data-matching-test)
  * [7.3 read database into json file](#73-read-database-into-json-file)
    + [7.3.1 @test invalid file](#731--test-invalid-file)
    + [7.3.2 @test database server closed error](#732--test-database-server-closed-error)
    + [7.3.3 @test verify the correctness of data](#733--test-verify-the-correctness-of-data)
  * [7.4 write json file into database](#74-write-json-file-into-database)
    + [7.4.1 test invalid file](#741-test-invalid-file)
    + [7.4.2 @test database server closed error](#742--test-database-server-closed-error)
    + [7.4.3 @test verify the correctness of data](#743--test-verify-the-correctness-of-data)
- [8. Frontend Test cases](#8-frontend-test-cases)
  * [8.1 GET author test](#81-get-author-test)
  * [8.2 GET book test](#82-get-book-test)
  * [8.3 GET query test](#83-get-query-test)
  * [8.4 PUT book success test](#84-put-book-success-test)
  * [8.5 PUT book fail test](#85-put-book-fail-test)
  * [8.6 PUT author success test](#86-put-author-success-test)
  * [8.7 PUT author fail test](#87-put-author-fail-test)
  * [8.8 POST book success test](#88-post-book-success-test)
  * [8.9 POST book fail test](#89-post-book-fail-test)
  * [8.10 POST author success test](#810-post-author-success-test)
  * [8.11 POST author fail test](#811-post-author-fail-test)
  * [8.12 POST scrape success test](#812-post-scrape-success-test)
  * [8.13 POST scrape fail test](#813-post-scrape-fail-test)
  * [8.14 DELETE book success test](#814-delete-book-success-test)
  * [8.15 DELETE book fail test](#815-delete-book-fail-test)
  * [8.16 DELETE author success test](#816-delete-author-success-test)
  * [8.17 DELETE author fail test](#817-delete-author-fail-test)
  * [8.18 d3 get top n book test](#818-d3-get-top-n-book-test)
  * [8.19 d3 get top n author test](#819-d3-get-top-n-author-test)


## 1.Introducation
The program under test is a web scraping program for the Goodreads.com.
This program is capable of scraping 200 - 2000 book page and 50 - 2000 author page
, and it is able to store the scraped data in to mysql database. 
User could choose to export the data in database as json file or import a json file with correct format into database.
In this manual test plan, some test cases and testing method like testing environment will be presented.

## 2.Environment Setup
* Python 3.9.5
* pip install : bueatiful soup, dotenv, pylint.
* Vscode with Python 3.9.5 64-bit extension
* windows 10

## 3.unittest cases
there is a unittest case in the program file that verifies the functionality of helper function.
To do the unit testing, run the test_file.py in the backend file.

## 4.scraping method

The scraping library this program is beautiful soup. The main program feeds the beautiful soup object of requested webpage into various scraping function to get the wanted data.

#### 4.1.scraping book functions
* get_book_title(soup, cur_book_url) # get book title from book page
* get_book_id(book_url) # get the book id
* get_book_isbn(soup) # get ISBN from book page
* get_book_author_url(soup) # scraping author url in book webpage.
* get_book_author(soup) # get author name from book page
* get_book_rating(soup) # get rating from book page
* get_book_rating_counts(soup) # get rating count from book page
* get_book_review_count(soup) # get review count from book page
* get_book_img(soup) # get the book cover from book page
* get_book_similar(soup) # get the similar books link from book page
* get_nxt_book_url(book_list_link, book_list) # get next book page url for scraping

#### 4.2.scraping author function
* get_author_name(soup) # get author name from author page
* get_author_id(book_author_url) # get the author id from author url
* get_author_rating(soup) # get author rating from author page
* get_author_rating_count(soup) # get author rating count from author page
* get_author_review_count(soup) # get author review count from author page
* get_author_img(soup) # get author image from author page
* get_similar_author(soup) # get similar author from the author page
* get_list_books(soup) # get book list from author page
* get_next_author_url(similar_url, author_list) # get next author page url for scraping

## 5.database importing method

This program imports data into the mysql database by using the library mysql.connector.
mysql.connector can be taken as a medium for communication between the scraping program and the mysql database.
After setting the server user and password correctly, we can use the sql cursor from cursor() to manipulate the content of database.

## 6.Manual testing strategy

#### 6.1 verifying scraping result
Although unit testing tests some of the scraping function with fixed website, the functionality of this program still need to be tested with more stimuli.
We can verify the scraping result by manually checking the difference between the output of the program and the data shown in the web page.
For example, for verifying the author url in book page. we can click both output url and url in the web page to check if the following pages are identical.

#### 6.2 verifying data imported into database
We can import data into database row by row, and check if the data in the data set matches the data we use to import.

#### 6.3 verifying importing json file and exporting to json file
we can first check row by row like 6.2 for importing and exporting. Then we can have a json file contains large amount of data and import the json file into the database
, then export the data into from database into a new json file. We can use diff to check if two json files are identical.

## 7. Backend Test cases

### 7.1 scraping test cases

#### 7.1.1 @test matching rating, rating count and review count
since the rating, rating count and review count are updating all the time
, it's impossible to unit tests these functions with fix references.
We can verify the outcome of these function by comparing the outputs with actual rating, rating count and review count at the top of the review section in both book and author page.

#### 7.1.2 @test matching matching other attributes
since unit test only use one reference web page to test the scraping functions,  the outcome is not very reliable. we could match the output with all other attribute by looking at the section top of the review section.

#### 7.1.3 @test scraping error testing
While the program is scraping, some data might be unavailable due to blocking. The program need to catch the error incurred by data unavailable. We can feed our scraping functions with
any web page that lacks corresponding attributes. The correct behavior of these functions are outputing 'null' without any error.

### 7.2 importing data to database test cases

#### 7.2.1 @test send data with wrong format into database
if the program is attempting to send data with wrong format (author data should contains 9 strings, book data should contains 11 strings),
this attempt will be canceled and "err:unable to send data to the database" will be printed on the terminal.

#### 7.2.2 @test database server closed error
if the server of database closes due to some misbehavior like too many characters in one row. This data importing attempt will be canceled and "err:unable to send data to the database" will be printed on the terminal.

#### 7.2.3 @test data matching test
We can use the strategy described in 6.2 to verify that the data is correct.

### 7.3 read database into json file

#### 7.3.1 @test invalid file
if the file used to read from database is not a json file, program will exit and "not a json file" will be shown on the terminal. if the file does not exist, the program will automatically create it.

#### 7.3.2 @test database server closed error
if the server of database closes due to some misbehavior like too many characters in one row. This reading attempt will be canceled and "err:unable to send data to the database" will be printed on the terminal.

#### 7.3.3 @test verify the correctness of data
we can use the method at 6.3 to verify the correctness of read data

### 7.4 write json file into database

#### 7.4.1 test invalid file
if the file is not a json file, program will exit and "not a json file" will be shown on the terminal.
if the file doesn't exist, the program will exit safely and "fail to convert, please check your input file." will be printed in the terminal.

#### 7.4.2 @test database server closed error
if the server of database closes due to some misbehavior like too many characters in one row. This reading attempt will be canceled and "err:unable to send data to the database" will be printed on the terminal.

#### 7.4.3 @test verify the correctness of data
we can use the method at 6.3 to verify the correctness of read data.

## 8. Frontend Test cases

### 8.1 GET author test
After typing appropriate author id, the author infor will show, otherwise nothing will happen.
![](screenshots/GET_author_scrshot.png)
### 8.2 GET book test
After typing appropriate author id, the book infor will show, otherwise nothing will happen.
![](screenshots/GET_book_scrshot.png)
### 8.3 GET query test
After typing appropriate query line and table name, a spreadsheet of author/book attributes will show
![](screenshots/GET_query_scrshot.png)
### 8.4 PUT book success test
After typing appropriate id and content, a PUT SUCCESS will show, and corresponding row will be updated.
![](screenshots/PUT_book_scrshot.png)
### 8.5 PUT book fail test
if the content is not in json format, "invalid parameter, fail to update" will show.
![](screenshots/PUT_book_fail_scrshot.png)
### 8.6 PUT author success test
After typing appropriate id and content, a PUT SUCCESS will show, and corresponding row will be updated.
![](screenshots/PUT_author_scrshot.png)
### 8.7 PUT author fail test
if the content is not in json format, "invalid parameter, fail to update" will show.
![](screenshots/PUT_author_fail_scrshot.png)
### 8.8 POST book success test
if every attributes are set correctly, "POST SUCESS" will show.
![](screenshots/POST_book_scrshot.png)
### 8.9 POST book fail test
if error is sent from backend, "Invalid dataType, fail to post" will show.

### 8.10 POST author success test
if every attributes are set correctly, "POST SUCESS" will show.
![](screenshots/POST_author_scrshot.png)

### 8.11 POST author fail test
if error is sent from backend, "Invalid dataType, fail to post" will show.

### 8.12 POST scrape success test
if the url is valid, "POST SUCESS" will show.
![](screenshots/POST_scrape_scrshot.png)

### 8.13 POST scrape fail test
if the url is invalid, "invalid parameter, fail to update" will show.
![](screenshots/POST_scrape_fail_scrshot.png)

### 8.14 DELETE book success test
if the id is valid, "DELETE success" will show.
![](screenshots/DELETE_book_scrshot.png)

### 8.15 DELETE book fail test
is the id is invalid, for example empty, "invalid parameter, fail to delete" will show.
![](screenshots/DELETE_book_fail_scrshot.png)

### 8.16 DELETE author success test
if the id is valid, "DELETE success" will show.
![](screenshots/DELETE_author_scrshot.png)

### 8.17 DELETE author fail test
is the id is invalid, for example empty, "invalid parameter, fail to delete" will show.
![](screenshots/DELETE_author_fail_scrshot.png)

### 8.18 d3 get top n book test
Typing number in the box and clicking submit will return this bar chart.
![](screenshots/POST_top_n_book_scrshot.png)

### 8.19 d3 get top n author test
Typing number in the box and clicking submit will return this bar chart.
![](screenshots/POST_top_n_author_scrshot.png)
