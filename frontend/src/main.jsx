import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'

import { NavDropdownStoreProvider } from './context/nav-dropdown-store.context.jsx'

import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <NavDropdownStoreProvider>
      <App />
    </NavDropdownStoreProvider>
  </React.StrictMode>
)
