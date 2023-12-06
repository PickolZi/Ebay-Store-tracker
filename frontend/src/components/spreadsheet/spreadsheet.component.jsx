import dayjs from "dayjs";

import "./spreadsheet.styles.css";
import { useEffect, useState } from "react";

const Spreadsheet = ({soldItemsData, setSoldItemsData}) => {
    const [isTitleSort, setTitleSort] = useState(false);
    const [isMakeSort, setMakeSort] = useState(false);
    const [isModelSort, setModelSort] = useState(false);
    const [isPriceSort, setPriceSort] = useState(false);
    const [isListedDateSort, setListedDateSort] = useState(false);
    const [isDateSoldSort, setDateSoldSort] = useState(false);
    const [isDaysTillSoldSort, setDaysTillSoldSort] = useState(false);
    
    const sortArrayAscending = (header) => {
        // Three conditionals below are dates. Need special sorting algorithm.
        if (header == "listed_date" || header == "date_sold") {
            return [...soldItemsData].sort((a, b) => {
                const dateAInSec = dayjs(a[header]).unix();
                const dateBInSec = dayjs(b[header]).unix();

                if (dateAInSec > dateBInSec) {
                    return 1;
                } else if (dateAInSec < dateBInSec) {
                    return -1;
                } else {
                    return 0;
                }
            })
        } else if (header == "days_till_sold") {
            return [...soldItemsData].sort((a, b) => {
                const dateAInSec = dayjs(a["date_sold"]).diff(dayjs(a["listed_date"]), 'days');
                const dateBInSec = dayjs(b["date_sold"]).diff(dayjs(b["listed_date"]), 'days');

                if (dateAInSec > dateBInSec) {
                    return 1;
                } else if (dateAInSec < dateBInSec) {
                    return -1;
                } else {
                    return 0;
                }
            })
        }

        // Rest are plain text or numbers.
        return [...soldItemsData].sort((a, b) => {
            if (a[header] > b[header]) {
                return 1;
            } else if (a[header] < b[header]) {
                return -1;
            } else {
                return 0;
            }
        })
    }

    const sortArrayDescending = (header) => {
        // Three conditionals below are dates. Need special sorting algorithm.
        if (header == "listed_date" || header == "date_sold") {
            return [...soldItemsData].sort((a, b) => {
                const dateAInSec = dayjs(a[header]).unix();
                const dateBInSec = dayjs(b[header]).unix();

                if (dateAInSec > dateBInSec) {
                    return -1;
                } else if (dateAInSec < dateBInSec) {
                    return 1;
                } else {
                    return 0;
                }
            })
        } else if (header == "days_till_sold") {
            return [...soldItemsData].sort((a, b) => {
                const dateAInSec = dayjs(a["date_sold"]).diff(dayjs(a["listed_date"]), 'days');
                const dateBInSec = dayjs(b["date_sold"]).diff(dayjs(b["listed_date"]), 'days');

                if (dateAInSec > dateBInSec) {
                    return -1;
                } else if (dateAInSec < dateBInSec) {
                    return 1;
                } else {
                    return 0;
                }
            })
        }

        // Rest are plain text or numbers.
        return [...soldItemsData].sort((a, b) => {
            if (a[header] > b[header]) {
                return -1;
            } else if (a[header] < b[header]) {
                return 1;
            } else {
                return 0;
            }
        })
    }

    const setSoldItemsDataHandler = (event) => {
        const clicked = event.target.textContent;
        let sortedItems = []

        if (clicked == "Picture") {
            return;
        } else if (clicked == "Title") {
            setTitleSort(!isTitleSort);
            if (isTitleSort) {
                sortedItems = sortArrayAscending("title");
            } else {
                sortedItems = sortArrayDescending("title");
            }
        } else if (clicked == "Make") {
            setMakeSort(!isMakeSort);
            if (isMakeSort) {
                sortedItems = sortArrayAscending("make");
            } else {
                sortedItems = sortArrayDescending("make");
            }
        } else if (clicked == "Model") {
            setModelSort(!isModelSort);
            if (isModelSort) {
                sortedItems = sortArrayAscending("model");
            } else {
                sortedItems = sortArrayDescending("model");
            }
        } else if (clicked == "Price") {
            setPriceSort(!isPriceSort);
            if (isPriceSort) {
                sortedItems = sortArrayAscending("price");
            } else {
                sortedItems = sortArrayDescending("price");
            }
        } else if (clicked == "Listed date") {
            setListedDateSort(!isListedDateSort);
            if (isListedDateSort) {
                sortedItems = sortArrayAscending("listed_date");
            } else {
                sortedItems = sortArrayDescending("listed_date");
            }
        } else if (clicked == "Date sold") {
            setDateSoldSort(!isDateSoldSort);
            if (isDateSoldSort) {
                sortedItems = sortArrayAscending("date_sold");
            } else {
                sortedItems = sortArrayDescending("date_sold");
            }
        } else if (clicked == "Days till sold") {
            setDaysTillSoldSort(!isDaysTillSoldSort);
            if (isDaysTillSoldSort) {
                sortedItems = sortArrayAscending("days_till_sold");
            } else {
                sortedItems = sortArrayDescending("days_till_sold");
            }
        }

        setSoldItemsData(sortedItems);
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