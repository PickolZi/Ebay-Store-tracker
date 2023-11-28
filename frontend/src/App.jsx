import { useContext } from 'react'

import Navbar from './components/navbar/navbar.component'
import CalendarSideBar from './components/calendar-sidebar/calendar-sidebar.component'

import { CalendarDateContext } from './context/calendar-date.context'

import './App.css'


function App() {
  const { isCalendarSidebar } = useContext(CalendarDateContext);

  return (
    <>
      <Navbar></Navbar>
      {isCalendarSidebar && <CalendarSideBar></CalendarSideBar>}
      
    </>
  )
}

export default App