import {React, useState} from "react"
import "./deleteAuthor.css"

/**
 * The delete author section
 * @param {parameter wrapper} props
 * @return the delete author form in html
 */
export default function DeleteAuthor(props){
    const [Id, setId] = useState("");
    const [display, setDisplay] = useState("");
    const requestOptions = {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: ''
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
            setDisplay("Invalid parameter, fail to Delete");
        })
        
    }
    return (
        <div className= "GetBookWrapper" >
            <h1 className = "getBookHead">Delete Author</h1>
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
                    Submit
                </button>
            </div>
            <h1 className = "display">{display}</h1>
        </div>
      );
}