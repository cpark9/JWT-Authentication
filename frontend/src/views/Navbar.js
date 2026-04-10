import React from 'react'
// import { jwtDecode } from "jwt-decode"
import AuthContext from '../context/AuthContext'
import { Link } from 'react-router-dom'

function Navbar() {

  // const {user, logoutUser} = React.useContext(AuthContext)
  const {logoutUser} = React.useContext(AuthContext)
  const token = localStorage.getItem("authTokens")

  // if (token){
  //   const decoded = jwtDecode(token);
  //   var user_id = decoded.user_id
  // }

  return (
    <div>
      <nav class="navbar navbar-expand-lg navbar-dark fixed-top bg-dark">
        <div class="container-fluid">
          <a class="navbar-brand" href="/">
            <img style={{width:"120px", padding:"6px"}} src="https://i.imgur.com/juL1aAc.png" alt="" />
          </a>
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse justify-content-start" id="navbarNav">
            <ul class="navbar-nav">
              <li class="nav-item">
                <a class="nav-link active" aria-current="page" href="/">Home</a>
              </li>
              {token === null && 
              <>
                <li class="nav-item">
                  <a class="nav-link" href="/login">Login</a>
                </li>
                <li class="nav-item">
                  <a class="nav-link" href="/register">Register</a>
                </li>
              </>
              }
              {token !== null && 
              <>
              {/* <a> 태그 : 전체 화면을 새로고침, <Link> 태그 : 페이지 이동 (새로고침 X) */}
                <li class="nav-item">
                  <a class="nav-link" href="/dashboard">Dashboard</a>
                </li>
                <li class="nav-item">
                  <Link class="nav-link" to="/todo">Todo</Link>
                </li>
                <li class="nav-item">
                  <a class="nav-link" href="#!" onClick={logoutUser} style={{cursor:"pointer"}}>Logout</a>
                </li>
              </>
              }   
            </ul>
          </div>
        </div>
      </nav>    
    </div>
  )
}

export default Navbar