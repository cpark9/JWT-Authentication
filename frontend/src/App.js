import React from 'react'

// import { BrowserRouter as Router, Route, Switch } from 'react-router-dom'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import PrivateRoute from './utils/PrivateRoute'
import { AuthProvider } from './context/AuthContext'

import Dashboard from './views/Dashboard'
import Homepage from './views/Homepage'
import Loginpage from './views/Loginpage'
import Registerpage from './views/Registerpage'
import Navbar from './views/Navbar'

function App() {
  return (
    <Router>
      <AuthProvider>
        < Navbar/>
        <Routes>
           {/* 보호하고 싶은 페이지는 PrivateRoute로 감싸서 element에 전달  */}
          <Route path="/dashboard" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
          <Route path="/login" element={<Loginpage />} />
          <Route path="/register" element={<Registerpage />} />
          {/* <Route path="/" element={<Homepage />} /> */}
          <Route path="/" element={<PrivateRoute><Homepage /></PrivateRoute>} />
        </Routes>
      </AuthProvider>
    </Router>
  )
}

export default App

