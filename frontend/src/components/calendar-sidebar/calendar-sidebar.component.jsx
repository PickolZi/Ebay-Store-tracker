import { useState, useEffect, useContext } from 'react';

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
                onChange={(curDate) => {setStartDate(curDate.toISOString())}} />
            <DatePicker 
                value={dayjs(endDate)} 
                onChange={(curDate) => {setEndDate(curDate.toISOString())}} />
        </section>
    );
}

export default CalendarSideBar;