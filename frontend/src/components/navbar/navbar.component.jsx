import { useContext } from "react";

import { NavDropdownStoreContext } from '../../context/nav-dropdown-store.context';
import { CalendarDateContext } from "../../context/calendar-date.context";

import "./navbar.styles.css";
import CalendarSVG  from "../../assets/calendar.svg";

const Navbar = () => {
    const { navDropdownStore,
        setNavDropdownStore,
        navDropdownStoreID,
        setNavDropdownStoreID,
        navDropdownStoreOptions
        } = useContext(NavDropdownStoreContext);
    const {
        isCalendarSidebar,
        setIsCalendarSidebar
    } = useContext(CalendarDateContext);

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

    const toggleCalendarSidebar = () => {
        setIsCalendarSidebar(!isCalendarSidebar);
    }

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

            <img 
                className="nav__calendar-icon" 
                src={CalendarSVG} 
                alt="Calendar SVG" 
                onClick={toggleCalendarSidebar}/>        
        </nav>        
    )
}

export default Navbar;