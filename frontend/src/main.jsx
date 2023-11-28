import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'

// Contexts
import { NavDropdownStoreProvider } from './context/nav-dropdown-store.context.jsx';
import { CalendarDateProvider } from './context/calendar-date.context.jsx';

// Date Providers
import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs'

import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <NavDropdownStoreProvider>
      <CalendarDateProvider>
        <LocalizationProvider dateAdapter={AdapterDayjs}>
          <App />
        </LocalizationProvider>
      </CalendarDateProvider>
    </NavDropdownStoreProvider>
  </React.StrictMode>
)
