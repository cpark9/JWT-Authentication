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
import Todo from './views/Todo'

function App() {
  return (
    <Router>
      <AuthProvider>
        < Navbar/>
        <Routes>
          {/* <PrivateRoute component={Dashboard} path="/dashboard" exact />
          <Route component={Loginpage} path="/login" />
          <Route component={Registerpage} path="/register" exact />
          <Route component={Homepage} path="/" exact />
          <Route component={Todo} path="/todo" exact /> */}

           {/* 보호하고 싶은 페이지는 PrivateRoute로 감싸서 element에 전달  */}
          <Route path="/dashboard" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
          <Route path="/login" element={<Loginpage />} />
          <Route path="/register" element={<Registerpage />} />
          <Route path="/" element={<PrivateRoute><Homepage /></PrivateRoute>} />
          <Route path="/todo" element={<PrivateRoute><Todo /></PrivateRoute>} />
        </Routes>
      </AuthProvider>
    </Router>
  )
}

export default App

