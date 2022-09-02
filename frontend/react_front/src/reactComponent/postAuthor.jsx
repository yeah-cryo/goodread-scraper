import {React, useState} from "react"
import "./postAuthor.css"

/**
 * the post author section
 * @param {parameter wrapper} props
 * @return the post author section in html
 */
export default function PostAuthor(props){
    const [name, setName] = useState("");
    const [authorUrl, setAuthorUrl] = useState("")
    const [AuthorId, setAuthorId] = useState("")
    const [rating, setRating] = useState("")
    const [ratingCount, setRatingCount] = useState("")
    const [reviewCount, setReviewCount] = useState("")
    const [imgUrl, setImgUrl] = useState("")
    const [relatedAuthor, setRelatedAuthor] = useState("")
    const [authorBooks, setAuthorBooks] = useState("")
    const [display, setDisplay] = useState("");
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({"name":name, "author_url":authorUrl
        , "author_id":AuthorId, "rating":rating
        , "rating_count": ratingCount, "review_count":reviewCount
        , "image_url":imgUrl, "related_authors":relatedAuthor, "author_books":authorBooks})
    };
    const handleSubmit = () =>{
        const url = 'http://127.0.0.1:5000/api/author';
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
            <h1 className = "getBookHead">Post Author</h1>
            <form className = "inputForm" onSubmit={handleSubmit} >
            <label>
                Author Name:
                <input
                type="text"
                placeholder="name"
                onChange={e => setName(e.target.value)}
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
                Author Id:
                <input
                type="text"
                placeholder="id"
                onChange={e => setAuthorId(e.target.value)}
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
                Related Author:
                <input
                type="text"
                placeholder="related Author url"
                onChange={e => setRelatedAuthor(e.target.value)}
                />
            </label>
            <label>
                Author Books:
                <input
                type="text"
                placeholder="author books"
                onChange={e => setAuthorBooks(e.target.value)}
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