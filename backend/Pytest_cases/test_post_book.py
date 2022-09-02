import requests

# API url
url = "http://127.0.0.1:5000/api/book"
url_s = "http://127.0.0.1:5000/api/books"

def test_post_one_book_success():
    data = """{
       "book_url": "https://www.goodreads.com/book/show/41593581-dziewczyna-z-poci-gu-barwa-ciszy",
       "title": "Dziewczyna z poci\u0105gu / Barwa ciszy",
       "book_id": "41593581",
       "ISBN": "null",
       "author_url": "https://www.goodreads.com/author/show/1063732.Paula_Hawkins",
       "author": "Paula Hawkins",
       "rating": "3.27",
       "rating_count": "33",
       "review_count": "0",
       "image_url": "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1535887068l/41593581._SX318_.jpg",
       "similar_books": "https://www.goodreads.com/book/similar/64931733-the-girl-on-the-train-the-quality-of-silence"
       }"""
    data = data.encode('utf-8')
    post_obj = requests.post(url, data)
    assert post_obj.status_code == 200
    assert post_obj.text == '<h1>POST SUCCESS</h1>'

def test_post_one_book_fail_not_json():
    data = "not a json"
    post_obj = requests.post(url, data)
    assert post_obj.status_code == 415
    assert post_obj.text == "<h1>415</h1><p>Invalid data Type, requiring JSON</p>"

def test_post_books_success():
    datas = """{
       "content": [
       {
       "book_url": "https://www.goodreads.com/book/show/34452.Many_Lives_Many_Masters",
       "title": "Many Lives, Many Masters: The True Story of a Prominent Psychiatrist, His Young Patient, and the Past Life Therapy That Changed Both Their Lives",
       "book_id": "34452",
       "ISBN": "null",
       "author_url": "https://www.goodreads.com/author/show/72099.Brian_L_Weiss",
       "author": "Brian L. Weiss",
       "rating": "4.15",
       "rating_count": "47394",
       "review_count": "3739",
       "image_url": "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1390099381l/34452.jpg",
       "similar_books": "https://www.goodreads.com/book/similar/2176901-many-lives-many-masters"
       },
       {
       "book_url": "https://www.goodreads.com/book/show/54075385-the-soul-of-a-woman",
       "title": "The Soul of a Woman",
       "book_id": "54075385",
       "ISBN": "null",
       "author_url": "https://www.goodreads.com/author/show/2238.Isabel_Allende",
       "author": "Isabel Allende",
       "rating": "4.07",
       "rating_count": "11689",
       "review_count": "1313",
       "image_url": "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1607320425l/54075385.jpg",
       "similar_books":
       "https://www.goodreads.com/book/similar/85515782-mujeres-del-alma-m-a-sobre-el-amor-impaciente-la-vida-larga-y-las-bruj"
       },
       {
       "book_url": "https://www.goodreads.com/book/show/341735.Replay",
       "title": "Replay",
       "book_id": "341735",
       "ISBN": "null",
       "author_url": "https://www.goodreads.com/author/show/19651.Ken_Grimwood",
       "author": "Ken Grimwood",
       "rating": "4.14",
       "rating_count": "38689",
       "review_count": "3655",
       "image_url": "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1441156728l/341735._SY475_.jpg",
       "similar_books": "https://www.goodreads.com/book/similar/1804797-replay"
       }
       ]
       }"""
    datas = datas.encode('utf-8')
    post_obj = requests.post(url_s, datas)
    assert post_obj.status_code == 200
    assert post_obj.text == '<h1>POST SUCCESS</h1>'