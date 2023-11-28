import { createContext, useEffect, useState } from "react";

import fetchFromAPIUsingEndpoint from "../utils/fetch_from_backend"

export const NavDropdownStoreContext = createContext({
    navDropdownStore: "",
    navDropdownStoreID: 0,
    navDropdownStoreOptions: [],
    setNavDropdownStore: () => {return null},
    setNavDropdownStoreID: () => {return null},
    setNavDropdownStoreOptions: () => {return null}
});

export const NavDropdownStoreProvider = ({children}) => {
    const [navDropdownStore, setNavDropdownStore] = useState("");
    const [navDropdownStoreID, setNavDropdownStoreID] = useState(0);
    const [navDropdownStoreOptions, setNavDropdownStoreOptions] = useState([]);
    const value = {navDropdownStore, setNavDropdownStore, navDropdownStoreID, setNavDropdownStoreID, navDropdownStoreOptions};

    useEffect(() => {
        // Adds list of k,v => [[store_name, store_id],...] in navDropdownStoreOptions 
        // Sets navDropdownStore and navDropdownStoreID to first store.
        const endpoint = "/api/getAllStores"
        const fetchFromAPI = async () => {
            await fetchFromAPIUsingEndpoint(endpoint).then((res) => {
                const stores = []
                Object.keys(res['stores']).forEach((store) => {
                    stores.push([store, res['stores'][store]])
                });
                setNavDropdownStoreOptions(stores);
            });
        }
        fetchFromAPI();
    }, []);

    useEffect(() => {
        if (navDropdownStoreOptions.length > 0) {
            setNavDropdownStore(navDropdownStoreOptions[0][0]);
            setNavDropdownStoreID(navDropdownStoreOptions[0][1]);
        }
    }, [navDropdownStoreOptions])

    return (
        <NavDropdownStoreContext.Provider value={value}>{children}</NavDropdownStoreContext.Provider>
    );
}