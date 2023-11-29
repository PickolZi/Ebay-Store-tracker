import { useEffect, useContext } from 'react';

import { CalendarDateContext } from '../../context/calendar-date.context';

import dayjs from 'dayjs';
import { DatePicker } from '@mui/x-date-pickers';

import "./calendar-sidebar.styles.css";

const CalendarSideBar = () => {
    const {startDate, setStartDate, endDate, setEndDate} = useContext(CalendarDateContext);

    return (
        <section className="calendar__sidebar">
            <DatePicker 
                value={dayjs(startDate)} 
                onChange={(curDate) => {setStartDate(curDate.format("YYYY-MM-DD"))}} />
            <DatePicker 
                value={dayjs(endDate)} 
                onChange={(curDate) => {setEndDate(curDate.format("YYYY-MM-DD"))}} />
        </section>
    );
}

export default CalendarSideBar;