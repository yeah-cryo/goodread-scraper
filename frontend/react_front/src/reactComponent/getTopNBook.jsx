import {React, useState} from "react"
import "./getBook.css"
import BarChart from "./BarChart";

/**
 * The get top n book section
 * @param {parameter wrapper} props
 * @return the get top n book form in html
 */
export default function GetTopNBook(props){
    const [num, setNum] = useState("");
    const [arr, setArr] = useState([]);
    const [err, setError] = useState(null)
    const handleSubmit = () =>{
        const url = "http://127.0.0.1:5000/vis/top-books" + '?id=' + num;
        fetch(url).then((response) => {
            if (response.ok) {
                return response.json()
            }
            throw response;
        })
        .then(data => {
            setArr(data["books"]);
        })
        .catch(error => {
            console.error("error fetching data: ", error);
            setError(error);
        })
    }
    return (
        <div className= "GetBookWrapper" >
            <h1 className = "getBookHead">Show Top N books</h1>
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