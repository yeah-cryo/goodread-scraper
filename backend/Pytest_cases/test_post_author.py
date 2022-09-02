import requests

# API url
url = "http://127.0.0.1:5000/api/author"
url_s = "http://127.0.0.1:5000/api/authors"

def test_post_one_author_success():
    data = """{
       "name": "Douglas Adams",
       "author_url": "https://www.goodreads.com/author/show/4.Douglas_Adams",
       "author_id": "4",
       "rating": "4.19",
       "rating_count": "3001700",
       "review_count": "67094",
       "image_url": "https://images.gr-assets.com/authors/1616277702p5/4.jpg",
       "related_authors": "https://www.goodreads.com/author/similar/4.Douglas_Adams",
       "author_books": "The Hitchhiker's Guide to the Galaxy (Hitchhiker's Guide to the Galaxy, #1);The Ultimate Hitchhiker's Guide to the Galaxy (Hitchhiker's Guide to the Galaxy, #1-5);"
       }"""
    data = data.encode('utf-8')
    post_obj = requests.post(url, data)
    assert post_obj.status_code == 200
    assert post_obj.text == '<h1>POST SUCCESS</h1>'
def test_post_one_author_fail_not_json():
    data = "not a json"
    post_obj = requests.post(url, data)
    assert post_obj.status_code == 415
    assert post_obj.text == "<h1>415</h1><p>Invalid data Type, requiring JSON</p>"
def test_post_authors_success():
    datas = """{
            "content": [
            {
            "name": "Sandra Boynton",
            "author_url": "https://www.goodreads.com/author/show/3161.Sandra_Boynton",
            "author_id": "3161",
            "rating": "4.18",
            "rating_count": "200279",
            "review_count": "7201",
            "image_url": "https://images.gr-assets.com/authors/1272640545p5/3161.jpg",
            "related_authors": "https://www.goodreads.com/author/similar/3161.Sandra_Boynton",
            "author_books": "Moo, Baa, La La La!;The Going to Bed Book;"
            },
            {
            "name": "Eric Carle",
            "author_url": "https://www.goodreads.com/author/show/3362.Eric_Carle",
            "author_id": "3362",
            "rating": "4.22",
            "rating_count": "929848",
            "review_count": "25172",
            "image_url": "https://images.gr-assets.com/authors/1622147696p5/3362.jpg",
            "related_authors": "https://www.goodreads.com/author/similar/3362.Eric_Carle",
            "author_books": "The Very Hungry Caterpillar;The Very Busy Spider;"
            },
            {
            "name": "Douglas Adams",
            "author_url": "https://www.goodreads.com/author/show/4.Douglas_Adams",
            "author_id": "4",
            "rating": "4.19",
            "rating_count": "3001700",
            "review_count": "67094",
            "image_url": "https://images.gr-assets.com/authors/1616277702p5/4.jpg",
            "related_authors": "https://www.goodreads.com/author/similar/4.Douglas_Adams",
            "author_books": "The Hitchhiker's Guide to the Galaxy (Hitchhiker's Guide to the Galaxy, #1);The Ultimate Hitchhiker's Guide to the Galaxy (Hitchhiker's Guide to the Galaxy, #1-5);"
            }
            ]
    }"""
    datas = datas.encode('utf-8')
    post_obj = requests.post(url_s, datas)
    assert post_obj.status_code == 200
    assert post_obj.text == '<h1>POST SUCCESS</h1>'