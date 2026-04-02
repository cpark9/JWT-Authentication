import React from 'react'
import { Link } from 'react-router-dom'
import AuthContext from '../context/AuthContext'

function Loginpage() {

  const {loginUser} = React.useContext(AuthContext)
  const handleSubmit = e => {
    e.preventDefault()
    const email = e.target.email.value
    const password = e.target.password.value

    email.length > 0 && loginUser(email, password)

    // console.log(email)
    // console.log(password)
   
  }

  return (
    <div>
      <>
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
          <div class="container-fluid">
            <a class="navbar-brand" href="#">
              <img style={{"width": "100px", "height": "60px", "objectFit": "contain"}} src="https://i.imgur.com/juL1aAc.png" alt="" />
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
              <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
              <ul class="navbar-nav">
                <li class="nav-item">
                  <a class="nav-link active" aria-current="page" href="#">Home</a>
                </li>
                <li class="nav-item">
                  <a class="nav-link" href="#">Features</a>
                </li>
                <li class="nav-item">
                  <a class="nav-link" href="#">Pricing</a>
                </li>
                <li class="nav-item">
                  <a class="nav-link disabled">Disabled</a>
                </li>
              </ul>
            </div>
          </div>
        </nav>
        <section class="vh-100" style={{"background-color": "#9A616D"}}>
          <div class="container py-5 h-100">
            <div class="row d-flex justify-content-center align-items-center h-100">
              <div class="col col-xl-10">
                <div class="card" style={{"border-radius": "1rem"}}>
                  <div class="row g-0">
                    <div class="col-md-6 col-lg-5 d-none d-md-block">
                      <img  src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-login-form/img1.webp"
                        alt="login form" class="img-fluid" style={{"border-radius": "1rem 0 0 1rem"}} />
                    </div>
                    <div class="col-md-6 col-lg-7 d-flex align-items-center">
                      <div class="card-body p-4 p-lg-5 text-black">
        
                        <form onSubmit={handleSubmit}>
        
                          <div class="d-flex align-items-center mb-3 pb-1">
                            <i class="fas fa-cubes fa-2x me-3" style={{"color": "#ff6219"}}></i>
                            <div class="d-flex align-items-center mb-3 pb-1">
                              <i class="fas fa-cubes fa-2x me-3" style={{"color": "#ff6219"}}></i>
                              <span class="h2 fw-bold mb-0">Welcome back 👋</span>
                            </div>
                          </div>
        
                          <h5 class="fw-normal mb-3 pb-3" style={{"letter-spacing": "1px"}}>Sign into your account</h5>
        
                          <div class="form-outline mb-4">
                            <input type="email" id="form2Example17" class="form-control form-control-lg" name='email' />
                            <label class="form-label" for="form2Example17">Email address</label>
                          </div>
        
                          <div class="form-outline mb-4">
                            <input type="password" id="form2Example27" class="form-control form-control-lg" name='password' autocomplete="current-password"  />
                            <label class="form-label" for="form2Example27">Password</label>
                          </div>
        
                          <div class="pt-1 mb-4">
                            <button class="btn btn-dark btn-lg btn-block" type="submit">Login</button>
                          </div>
        
                          <a class="small text-muted" href="#!">Forgot password?</a>
                          <p class="mb-5 pb-lg-2" style={{"color": "#393f81"}}>Don't have an account?{" "} 
                            {/* <a href="#!" style={{"color": "#393f81"}}>Register here</a> */}
                            <Link to="/register" className="text-decoration-none" style={{ color: "#393f81" }}>
                              Register Now
                            </Link>
                          </p>
                          <a href="#!" class="small text-muted">Terms of use.</a>
                          <a href="#!" class="small text-muted">Privacy policy</a>
                        </form>
        
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <footer class="bg-light text-center text-lg-start">
          {/* <!-- Copyright --> */}
          <div class="text-center p-3" style={{"background-color": "rgba(0, 0, 0, 0.2)"}}>
            © 2019 - till date Copyright:
            <a class="text-dark" href="https://mdbootstrap.com/">desphixs.com</a>
          </div>
          {/* <!-- Copyright --> */}
        </footer> 
      </> 
    </div>
  )
}

export default Loginpage