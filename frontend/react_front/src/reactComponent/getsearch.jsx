import {React, useState} from "react"
import "./getsearch.css"
import Handsontb from "./hstb.jsx"

/**
 * The query section
 * @param {parameter wrapper} props
 * @return the query form in html
 */
export default function GetSearch(props){
    const [query, setQuery] = useState("");
    const [table, setTable] = useState("");
    const [array, setArr] = useState([]);
    const [err, setError] = useState(null)
    const handleSubmit = () =>{
        const url = 'http://127.0.0.1:5000/api/search?q=' + query;
        fetch(url).then((response) => {
            if (response.ok) {
                return response.json()
            }
            throw response;
        })
        .then(data => {
            if (table === "authors") {
                setArr(data["authors"]);
            }
            if (table === "books") {
                setArr(data["books"]);
            }
        })
        .catch(error => {
            console.error("error fetching data: ", error);
            setError(error);
        })
    }
    return (
        <div className= "GetAuthorWrapper" >
            <div>
                <h1 className = "getAuthorHead">Query</h1>
                <form className = "inputForm" onSubmit={handleSubmit} >
                <label>
                    Query line:
                    <input
                    type="text"
                    placeholder="query"
                    onChange={e => setQuery(e.target.value)}
                    />
                </label>
                <label>
                    Table name:
                    <input
                    type="text"
                    placeholder="table"
                    onChange={e => setTable(e.target.value)}
                    />
                </label>
                </form>
                <div style={{display:"flex"}}>
                    <button className="submitCode" onClick={handleSubmit}>
                        Submit
                    </button>
                </div>
            </div>
            <div>
                <Handsontb data = {array}/>
            </div>
        </div>
      );
}