import {React, useState} from "react"
import "./getAuthor.css"

/**
 * The get author section
 * @param {parameter wrapper} props
 * @return the get author form in html
 */
export default function GetAuthor(props){
    const [Id, setId] = useState("");
    const [name, setName] = useState("");
    const [authorUrl, setAuthorUrl] = useState("")
    const [authorId, setAuthorId] = useState("")
    const [rating, setRating] = useState("")
    const [authorRatingCount, setAuthorRatingCount] = useState("")
    const [authorReviewCount, setAuthorReviewCount] = useState("")
    const [imgUrl, setImgUrl] = useState("")
    const [relatedAuthors, setRelatedAuthors] = useState("")
    const [authorsBook, setAuthorBooks] = useState("")
    const [err, setError] = useState(null)
    const handleSubmit = () =>{
        const url = "http://127.0.0.1:5000/api/author" + '?id=' + Id;
        fetch(url).then((response) => {
            if (response.ok) {
                return response.json()
            }
            throw response;
        })
        .then(data => {
            setName(data["authors"][0]["name"]);
            setAuthorUrl(data["authors"][0]["author_url"]);
            setAuthorId(data["authors"][0]["author_id"]);
            setRating(data["authors"][0]["rating"]);
            setAuthorRatingCount(data["authors"][0]["rating_count"]);
            setAuthorReviewCount(data["authors"][0]["review_count"]);
            setImgUrl(data["authors"][0]["image_url"]);
            setRelatedAuthors(data["authors"][0]["related_authors"]);
            setAuthorBooks(data["authors"][0]["author_books"]);
        })
        .catch(error => {
            console.error("error fetching data: ", error);
            setError(error);
        })
    }
    return (
        <div className= "GetAuthorWrapper" >
            <h1 className = "getAuthorHead">GET Author</h1>
            <form className = "inputForm" onSubmit={handleSubmit} >
            <label>
                Author id:
                <input
                type="text"
                placeholder="author id"
                onChange={e => setId(e.target.value)}
                />
            </label>
            </form>
            <div style={{display:"flex"}}>
                <button className="submitCode" onClick={handleSubmit}>
                    submit code
                </button>
            </div>
            <ul className="Authorattribute">
                <li>Author name: {name}</li>
                <li>author url: {authorUrl}</li>
                <li>author Id: {authorId}</li>
                <li>rating: {rating}</li>
                <li>author Rating Count: {authorRatingCount}</li>
                <li>author Review Count: {authorReviewCount}</li>
                <li>image Url: {imgUrl}</li>
                <li>related Authors: {relatedAuthors}</li>
                <li>author's books: {authorsBook}</li>
            </ul>
        </div>
      );
}