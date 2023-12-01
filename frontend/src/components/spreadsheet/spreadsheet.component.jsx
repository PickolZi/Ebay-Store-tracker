import dayjs from "dayjs";

import "./spreadsheet.styles.css";

const Spreadsheet = ({soldItemsData, setSoldItemsData}) => {
    
    const setSoldItemsDataHandler = (event) => {
        console.log(event.target.textContent)
        // setSoldItemsData()
    }

    return (
        <div className="spreadsheet">
            <div className="spreadsheet__titles">
                <h2 className="spreadsheet__rows-picture spreadsheet__cell" onClick={setSoldItemsDataHandler}>Picture</h2>
                <h2 className="spreadsheet__rows-title spreadsheet__cell" onClick={setSoldItemsDataHandler}>Title</h2>
                <h2 className="spreadsheet__rows-make spreadsheet__cell" onClick={setSoldItemsDataHandler}>Make</h2>
                <h2 className="spreadsheet__rows-model spreadsheet__cell" onClick={setSoldItemsDataHandler}>Model</h2>
                <h2 className="spreadsheet__rows-price spreadsheet__cell" onClick={setSoldItemsDataHandler}>Price</h2>
                <h2 className="spreadsheet__rows-listed_date spreadsheet__cell" onClick={setSoldItemsDataHandler}>Listed date</h2>
                <h2 className="spreadsheet__rows-date_sold spreadsheet__cell" onClick={setSoldItemsDataHandler}>Date sold</h2>
                <h2 className="spreadsheet__rows-date_diff spreadsheet__cell" onClick={setSoldItemsDataHandler}>Days till sold</h2>
            </div>

            {soldItemsData && soldItemsData.map((item) => {
                const date_listed = dayjs(item["listed_date"]);
                const date_sold = dayjs(item["date_sold"])
                const date_diff = date_sold.diff(date_listed, 'days')
                
                return (
                    <div key={item["item_id"]} className="spreadsheet__rows">
                        <a href={item["image_url"]} className="spreadsheet__rows-picture-link spreadsheet__cell" target="_blank">
                            <img src={item["image_url"]} alt={item["title"]} className="spreadsheet__rows-picture" />
                        </a>
                        <h2 className="spreadsheet__rows-title spreadsheet__cell">
                            <a className="spreadsheet__rows-title-link" href={item["item_url"]} target="_blank">
                                {item["title"]}
                            </a>
                        </h2>
                        <h2 className="spreadsheet__rows-make spreadsheet__cell">{item["make"]}</h2>
                        <h2 className="spreadsheet__rows-model spreadsheet__cell">{item["model"]}</h2>
                        <h2 className="spreadsheet__rows-price spreadsheet__cell">${item["price"]}</h2>
                        <h2 className="spreadsheet__rows-listed_date spreadsheet__cell">{date_listed.toString().substring(0, 16)}</h2>
                        <h2 className="spreadsheet__rows-date_sold spreadsheet__cell">{date_sold.toString().substring(0, 16)}</h2>
                        <h2 className="spreadsheet__rows-date_diff spreadsheet__cell">{date_diff}</h2>
                    </div>
                )
            })}
        </div>
    )
}

export default Spreadsheet;