import {React, useState} from "react"
import "./putAuthor.css"

/**
 * the update author section
 * @param {parameter wrapper} props
 * @return the update author section in html
 */
export default function PutAuthor(props){
    const [Id, setId] = useState("");
    const [body, setBody] = useState("");
    const [display, setDisplay] = useState("");
    const requestOptions = {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: body
    };
    const handleSubmit = () =>{
        const url = 'http://127.0.0.1:5000/api/author?id=' + Id;
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
            setDisplay("Invalid parameter, fail to update");
        })
        
    }
    return (
        <div className= "GetBookWrapper" >
            <h1 className = "getBookHead">Update Author</h1>
            <form className = "inputForm" onSubmit={handleSubmit} >
            <label>
                Author id:
                <input
                type="text"
                placeholder="author id"
                onChange={e => setId(e.target.value)}
                />
            </label>
            <label>
                content:
                <input
                type="text"
                placeholder="content"
                onChange={e => setBody(e.target.value)}
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