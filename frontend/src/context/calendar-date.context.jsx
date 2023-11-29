import { createContext, useState } from "react";

import dayjs from 'dayjs';

export const CalendarDateContext = createContext({
    startDate: dayjs("2004-01-04").format("YYYY-MM-DD"),
    setStartDate: () => {return null},
    endDate: dayjs().format("YYYY-MM-DD"),
    setEndDate: () => {return null},
    isCalendarSidebar: false,
    setIsCalendarSidebar: () => {return null}
});

export const CalendarDateProvider = ({children}) => {
    const [startDate, setStartDate] = useState(dayjs("2004-01-04").format("YYYY-MM-DD"));
    const [endDate, setEndDate] = useState(dayjs().format("YYYY-MM-DD"));
    const [isCalendarSidebar, setIsCalendarSidebar] = useState(false);
    const value = {startDate, setStartDate, endDate, setEndDate, isCalendarSidebar, setIsCalendarSidebar};

    return (
        <CalendarDateContext.Provider value={value}>{children}</CalendarDateContext.Provider>
    );
}