import { useState, useEffect, useContext } from "react";

import Card from "../card/card.component";
import Spreadsheet from "../spreadsheet/spreadsheet.component";

import { NavDropdownStoreContext } from "../../context/nav-dropdown-store.context";
import { CalendarDateContext } from "../../context/calendar-date.context";

import "./dashboard.styles.css"

import fetchFromAPIUsingEndpoint from "../../utils/fetch_from_backend";
import addMakeAndModels from "../../utils/add_make_and_model_to_cars"

const Dashboard = () => {
    const { navDropdownStore, navDropdownStoreID} = useContext(NavDropdownStoreContext);
    const { startDate, endDate } = useContext(CalendarDateContext);
    const [soldItemsData, setSoldItemsData] = useState(0);
    const [soldItems, setSoldItems] = useState(0);
    const [soldItemsWorth, setSoldItemsWorth] = useState(0);
    const [listedItems, setListedItems] = useState(0);
    const [listedItemsWorth, setListedItemsWorth] = useState(0);

    useEffect(() => {
        const query = navDropdownStoreID + "?startDate=" + startDate + "&endDate=" + endDate;

        const soldItemsEndpoint = "/api/getAllSoldItems/store/" + query;
        const listedItemsEndpoint = "/api/getListedItemsInfo/store/" + query;

        fetchFromAPIUsingEndpoint(soldItemsEndpoint).then((res) => {
            setSoldItemsData(addMakeAndModels(res["data"]));
            setSoldItems(res["numOfItems"]);
            setSoldItemsWorth(res["totalWorth"].toFixed(2));
        });

        fetchFromAPIUsingEndpoint(listedItemsEndpoint).then((res) => {
            setListedItems(res["numOfItems"]);
            setListedItemsWorth(res["totalWorth"].toFixed(2));
        });
    }, [navDropdownStore, startDate, endDate]);

    // TO FIX: Glitch where not all data displayed by API is fully loaded on first try.
    // useEffect(() => {
    //     console.log("listed items: " + listedItems);
    //     console.log("listed items worth: " + listedItemsWorth);
    //     console.log("sold items: " + soldItems);
    //     console.log("sold items worth: " + soldItemsWorth);
    // }, [listedItems, soldItems]);

    return (
        <div className="dashboard">
            <div className="card-list">
                <Card title="Total Listings" content={listedItems + " listings"} />
                <Card title="Total Listings Value" content={"$" + listedItemsWorth} />
                <Card title="Total Sold Items" content={soldItems + " sold"} />
                <Card title="Total Sold Items Value" content={"$" + soldItemsWorth} />
            </div>
            
            <Spreadsheet soldItemsData={soldItemsData} setSoldItemsData={setSoldItemsData}/>
        </div>
    )
}

export default Dashboard;