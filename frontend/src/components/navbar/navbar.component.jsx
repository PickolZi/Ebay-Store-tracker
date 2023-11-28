import { useState, useEffect, useContext } from "react";

import { NavDropdownStoreContext } from '../../context/nav-dropdown-store.context';

import "./navbar.styles.css";

const Navbar = () => {
    const { navDropdownStore,
        setNavDropdownStore,
        navDropdownStoreID,
        setNavDropdownStoreID,
        navDropdownStoreOptions
        } = useContext(NavDropdownStoreContext);

    // Sets the navDropdown store name and id to its changed value.
    const navDropdownEventHandler = (event) => {
        const store = event.target.value;
        setNavDropdownStore(store)
        navDropdownStoreOptions.map((dropdownStore) => {
            if (dropdownStore[0] == store) {
                setNavDropdownStoreID(dropdownStore[1])
            }
        });
    }

    useEffect(() => {
        console.log("Dropdown option was changed: ");
        console.log("Store Name: " + navDropdownStore);
        console.log("Store ID: " + navDropdownStoreID);
    }, [navDropdownStore]);

    return (
        <nav>
            <h1 className="nav__title">Ebay Store Tracker</h1>

            <select className="nav__store-dropdown" name="ebay-stores" onChange={navDropdownEventHandler}>
                {navDropdownStore ? 
                    navDropdownStoreOptions.map((store) => {
                        return (
                            <option key={store[0]} value={store[0]}>{store[0]}</option>
                        )
                    })
                    :
                    <option>No Stores Available</option>
                }
            </select>

            <div className="nav__calendar">
                <h1>Calendar will go here.</h1>
            </div>

        
        </nav>
        
    )
}

export default Navbar;