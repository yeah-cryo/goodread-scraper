import {React, useState} from "react"
import "./getBook.css"

/**
 * The get book section
 * @param {parameter wrapper} props
 * @return the get book form in html
 */
export default function GetBook(props){
    const [Id, setId] = useState("");
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
    const [err, setError] = useState(null)
    const handleSubmit = () =>{
        const url = "http://127.0.0.1:5000/api/book" + '?id=' + Id;
        fetch(url).then((response) => {
            if (response.ok) {
                return response.json()
            }
            throw response;
        })
        .then(data => {
            setBookUrl(data["books"][0]["book_url"]);
            setTitle(data["books"][0]["title"]);
            setBookId(data["books"][0]["book_id"]);
            setISBN(data["books"][0]["ISBN"]);
            setAuthorUrl(data["books"][0]["author_url"]);
            setAuthorName(data["books"][0]["author"]);
            setRating(data["books"][0]["rating"]);
            setRatingCount(data["books"][0]["rating_count"]);
            setReviewCount(data["books"][0]["review_count"]);
            setImgUrl(data["books"][0]["image_url"]);
            setSimilarBook(data["books"][0]["similar_books"]);
        })
        .catch(error => {
            console.error("error fetching data: ", error);
            setError(error);
        })
        
    }
    return (
        <div className= "GetBookWrapper" >
            <h1 className = "getBookHead">GET Book</h1>
            <form className = "inputForm" onSubmit={handleSubmit} >
            <label>
                Book id:
                <input
                type="text"
                placeholder="book id"
                onChange={e => setId(e.target.value)}
                />
            </label>
            </form>
            <div style={{display:"flex"}}>
                <button className="submitCode" onClick={handleSubmit}>
                    submit code
                </button>
            </div>
            <ul className="Bookattribute">
                <li>Book url: {bookUrl}</li>
                <li>title: {title}</li>
                <li>Book Id: {BookId}</li>
                <li>ISBN: {ISBN}</li>
                <li>author Url: {authorUrl}</li>
                <li>author Name: {authorName}</li>
                <li>rating: {rating}</li>
                <li>rating Count: {ratingCount}</li>
                <li>review Count: {reviewCount}</li>
                <li>img Url: {imgUrl}</li>
                <li>similar Book: {similarBook}</li>
            </ul>
        </div>
      );
}