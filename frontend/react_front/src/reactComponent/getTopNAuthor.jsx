import {React, useState} from "react"
import "./getBook.css"
import BarChart from "./BarChart";

/**
 * The get top n author section
 * @param {parameter wrapper} props
 * @return the get top n author form in html
 */
export default function GetTopNauthor(props){
    const [num, setNum] = useState("");
    const [arr, setArr] = useState([]);
    const [err, setError] = useState(null)
    const handleSubmit = () =>{
        const url = "http://127.0.0.1:5000/vis/top-authors" + '?id=' + num;
        fetch(url).then((response) => {
            if (response.ok) {
                return response.json()
            }
            throw response;
        })
        .then(data => {
            setArr(data["authors"]);
        })
        .catch(error => {
            console.error("error fetching data: ", error);
            setError(error);
        })
    }
    return (
        <div className= "GetBookWrapper" >
            <h1 className = "getBookHead">Show Top N authors</h1>
            <form className = "inputForm" onSubmit={handleSubmit} >
            <label>
                Top N:
                <input
                type="text"
                placeholder="number"
                onChange={e => setNum(e.target.value)}
                />
            </label>
            </form>
            <div style={{display:"flex"}}>
                <button className="submitCode" onClick={handleSubmit}>
                    submit
                </button>
            </div>
            <div>
                <BarChart data={arr} />
            </div>
        </div>
      );
}