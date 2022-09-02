import {React, useState} from "react"
import "./postScrape.css"
/**
 * the post scrape result section
 * @param {parameter wrapper} props
 * @return the post scrape result section in html
 */
export default function PostScrape(props){
    const [url, setUrl] = useState("");
    const [display, setDisplay] = useState("");
    const requestOptions = {
        method: 'Post',
        headers: { 'Content-Type': 'application/json' },
        body: ''
    };
    const handleSubmit = () =>{
        const curl = 'http://127.0.0.1:5000/api/scrape?attr=' + url;
        fetch(curl, requestOptions).then((response) => {
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
            setDisplay("Invalid parameter, fail to update");
        })
        
    }
    return (
        <div className= "GetBookWrapper" >
            <h1 className = "getBookHead">Post scrape result</h1>
            <form className = "inputForm" onSubmit={handleSubmit} >
            <label>
                Page url:
                <input
                type="text"
                placeholder="url"
                onChange={e => setUrl(e.target.value)}
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