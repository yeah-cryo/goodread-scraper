import React, { useEffect,useState} from 'react';
import ReactDataSheet from 'react-datasheet';
// Be sure to include styles at some point, probably during your bootstrapping
import 'react-datasheet/lib/react-datasheet.css';

/**
 * The spreadsheet for displaying the query result
 * @param {parameter wrapper} props
 * @return the spreadsheet in html
 */
export default function Handsontb(props) { 
    const [dataArr, setarr] = useState([])
    const fields = []
    for (let i = 0; i < props.data.length; i++) {
        const curArr = []
        for (let key in props.data[i]) {
            if (i === 0) {
                fields.push({value:key})
            }
            curArr.push({value:props.data[i][key]})
        }
        if (i === 0) {
            dataArr.push(fields)
        }
        dataArr.push(curArr)
    }
    const [gridy, setGrid] = useState(dataArr)
    useEffect(() => {
        setGrid(dataArr);
    }, [dataArr]);
    return (
        <ReactDataSheet
        data={gridy}
        valueRenderer={cell => cell.value}
        onCellsChanged={changes => {
            const grid = gridy.map(row => [...row]);
            changes.forEach(({ cell, row, col, value }) => {
            grid[row][col] = { ...grid[row][col], value };
            });
            setGrid({ grid });
        }}
        />
      );
}
