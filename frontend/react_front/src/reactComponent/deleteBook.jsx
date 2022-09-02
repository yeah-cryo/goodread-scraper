import {React, useState} from "react"
import "./deleteBook.css"

/**
 * The delete book section
 * @param {parameter wrapper} props
 * @return the delete book form in html
 */
export default function DeleteBook(props){
    const [Id, setId] = useState("");
    const [display, setDisplay] = useState("");
    const requestOptions = {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: ''
    };
    const handleSubmit = () =>{
        const url = 'http://127.0.0.1:5000/api/book?id=' + Id;
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
            setDisplay("Invalid parameter, fail to delete");
        })
        
    }
    return (
        <div className= "GetBookWrapper" >
            <h1 className = "getBookHead">Delete Book</h1>
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
                    Submit
                </button>
            </div>
            <h1 className = "display">{display}</h1>
        </div>
      );
}