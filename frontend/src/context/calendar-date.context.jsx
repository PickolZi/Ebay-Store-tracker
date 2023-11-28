import { createContext, useState } from "react";

import dayjs from 'dayjs';

export const CalendarDateContext = createContext({
    startDate: dayjs("2004-01-04").toISOString(),
    setStartDate: () => {return null},
    endDate: dayjs().toISOString(),
    setEndDate: () => {return null},
    isCalendarSidebar: false,
    setIsCalendarSidebar: () => {return null}
});

export const CalendarDateProvider = ({children}) => {
    const [startDate, setStartDate] = useState(dayjs("2004-01-04").toISOString());
    const [endDate, setEndDate] = useState(dayjs().toISOString());
    const [isCalendarSidebar, setIsCalendarSidebar] = useState(false);
    const value = {startDate, setStartDate, endDate, setEndDate, isCalendarSidebar, setIsCalendarSidebar};

    return (
        <CalendarDateContext.Provider value={value}>{children}</CalendarDateContext.Provider>
    );
}