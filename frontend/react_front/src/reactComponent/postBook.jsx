import {React, useState} from "react"
import "./postBook.css"

/**
 * the post book section
 * @param {parameter wrapper} props
 * @return the post book section in html
 */
export default function PostBook(props){
    const [bookUrl, setBookUrl] = useState("");
    const [title, setTitle] = useState("")
    const [BookId, setBookId] = useState("")
    const [ISBN, setISBN] = useState("")
    const [authorUrl, setAuthorUrl] = useState("")
    const [authorName, setAuthorName] = useState("")
    const [rating, setRating] = useState("")
    const [ratingCount, setRatingCount] = useState("")
    const [reviewCount, setReviewCount] = useState("")
    const [imgUrl, setImgUrl] = useState("")
    const [similarBook, setSimilarBook] = useState("")
    const [display, setDisplay] = useState("");
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({"book_url":bookUrl, "title":title
        , "book_id":BookId, "ISBN":ISBN, "author_url":authorUrl
        , "author":authorName, "rating":rating
        , "rating_count": ratingCount, "review_count":reviewCount
        , "image_url":imgUrl, "similar_books":similarBook})
    };
    const handleSubmit = () =>{
        const url = 'http://127.0.0.1:5000/api/book';
        fetch(url, requestOptions).then((response) => {
            if (response.ok) {
                return response.json()
            }
            throw response;
        })
        .then(data => {
            setDisplay(data['message']);
        })
        .catch(error => {
            console.error("error fetching data: ", error);
            setDisplay("Invalid dataType, fail to post");
        })
        
    }
    return (
        <div className= "GetBookWrapper" >
            <h1 className = "getBookHead">Post Book</h1>
            <form className = "inputForm" onSubmit={handleSubmit} >
            <label>
                Book Url:
                <input
                type="text"
                placeholder="url"
                onChange={e => setBookUrl(e.target.value)}
                />
            </label>
            <label>
                Title:
                <input
                type="text"
                placeholder="title"
                onChange={e => setTitle(e.target.value)}
                />
            </label>
            <label>
                Book Id:
                <input
                type="text"
                placeholder="id"
                onChange={e => setBookId(e.target.value)}
                />
            </label>
            <label>
                ISBN:
                <input
                type="text"
                placeholder="ISBN"
                onChange={e => setISBN(e.target.value)}
                />
            </label>
            <label>
                Author Url:
                <input
                type="text"
                placeholder="author url"
                onChange={e => setAuthorUrl(e.target.value)}
                />
            </label>
            <label>
                Author Name:
                <input
                type="text"
                placeholder="author name"
                onChange={e => setAuthorName(e.target.value)}
                />
            </label>
            <label>
                Rating:
                <input
                type="text"
                placeholder="rating"
                onChange={e => setRating(e.target.value)}
                />
            </label>
            <label>
                Rating Count:
                <input
                type="text"
                placeholder="rating count"
                onChange={e => setRatingCount(e.target.value)}
                />
            </label>
            <label>
                Review Count:
                <input
                type="text"
                placeholder="review count"
                onChange={e => setReviewCount(e.target.value)}
                />
            </label>
            <label>
                Image Url:
                <input
                type="text"
                placeholder="image url"
                onChange={e => setImgUrl(e.target.value)}
                />
            </label>
            <label>
                Similar Book:
                <input
                type="text"
                placeholder="similar book url"
                onChange={e => setSimilarBook(e.target.value)}
                />
            </label>
            </form>
            <div style={{display:"flex"}}>
                <button className="submitCode" onClick={handleSubmit}>
                    Submit
                </button>
            </div>
            <h1 className = "display">{display}</h1>
        </div>
      );
}