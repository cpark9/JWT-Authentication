import React from 'react'
import './style/Message.css'
import { useState, useEffect } from 'react'
import useAxios from '../utils/useAxios'
// import { jwtDecode } from 'jwt-decode' 
import { Link, useParams, useNavigate } from 'react-router-dom' 
// import moment from 'moment';
const swal = require('sweetalert2')

function SearchUsers() {

  const baseURL = 'http://127.0.0.1:8000/api'

  // 변화하는 데이터를 담는 바구니와 그 바구니 전용 집게
  const [users, setUsers] = useState([]) 
  const [profiles, setProfile] = useState([]) 
  const [newSearch, setNewSearch] = useState({ username: "" }); 
  const [loading, setLoading] = useState(true);

  // URL 주소창에 포함된 변수 값을 리액트가 쏙 뽑아낼 때 사용하는 코드
  const { username } = useParams() 
  // React Router v6에서 제공하는 훅으로, 코드를 통해 페이지를 이동시킬 때 사용하는 도구
  const navigate = useNavigate() 
  //  로그인 인증 정보(토큰)가 포함된 커스텀 통신 도구를 가져오는 코드
  const axios = useAxios()

  // 사용자가 검색 페이지에 들어왔을 때, URL에 포함된 이름으로 서버에 데이터를 요청하고 그 결과를 화면에 반영하는 핵심 로직
  useEffect(() => {
    const fetchUsers = async () => {
      if (!username) { 
        setLoading(false);
        return;
      }
      try {
        const res = await axios.get(baseURL + '/search/' + username + '/'); // destructured username 사용
        setUsers(res.data); // setUsers 사용
      } catch (error) {
      swal.fire({
        title: "User Does Not Exist",
        icon: "error",
        toast: true,
        timer: 2000,
        position: 'center',
        timerProgressBar: true,
        showConfirmButton: false,
        showCancelButton: true,
      })
      } finally {
        setLoading(false);
      }
    };
    fetchUsers();
  }, [axios, username]); 


  const handleSearchChange = (event) => {
    setNewSearch({ // setNewSearch 사용
      ...newSearch,
      [event.target.name]: event.target.value,
    });

  };

  // console.log(newSearch.username); // 디버깅용 로그는 필요에 따라 유지


  const SearchUser = async () => { // async/await 패턴 사용
    try {
      const res = await axios.get(baseURL + '/search/' + newSearch.username + '/');
      setUsers(res.data); // setUsers 사용
      navigate('/search/' + newSearch.username + '/'); // navigate 사용
    } catch (error) {
      console.error("Error searching user:", error); // 에러 로그 추가
      // axios는 4xx/5xx 응답 시 자동으로 에러를 throw하므로, .catch 블록에서 처리
      // .then() 블록 내에서 res.status === 404 체크는 불필요
        swal.fire({
          title: "User Does Not Exist",
          icon: "error",
          toast: true,
          timer: 2000,
          position: 'center',
          timerProgressBar: true,
          showConfirmButton: false,
          showCancelButton: true,
        })
    }
};


  // console.log(users); // 디버깅용 로그는 필요에 따라 유지
  // console.log(profiles); // 사용되지 않는 상태이므로 제거
  return (
      <main className="content" style={{ marginTop: "150px" }}>
        <div className="container p-0">
          <h1 className="h3 mb-3">Messages</h1>
          <div className="card">
            <div className="row g-0">
              <div className="col-12 col-lg-5 col-xl-3 border-right">
              <div className="px-4 ">
                  <div className="d-flex align-items-center"> {/* 클래스명 오타 수정 */}
                    <div className="flex-grow-1 d-flex align-items-center mt-2">
                      <input
                        type="text"
                        className="form-control my-3"
                        placeholder="Search..."
                        onChange={handleSearchChange}
                        name='username'

                      />
                      <button className='ml-2' onClick={SearchUser} style={{border:"none", borderRadius:"50%"}}><i className='fas fa-search'></i></button>
                    </div>
                  </div>
                </div>
                
                {users.map((user, index) => 
                  <Link 
                    key={user.id}
                    to={"/inbox/" + user.id}
                    className="list-group-item list-group-item-action border-0" // href="#" 제거
                  >
                    <small><div className="badge bg-success float-right text-white"></div></small> {/* 이 div는 현재 비어있습니다. */}
                    <div className="d-flex align-items-start">
                      <img src={user.image} className="rounded-circle mr-1" alt={user.full_name || user.username} width={40} height={40}/> {/* 의미 있는 alt 텍스트로 변경 */}
                    
                      <div className="flex-grow-1 ml-3">
                         {user.full_name}  

                        <div className="small">
                           <small><i className='fas fa-envelope'> Send Message</i></small>
                        </div>
                      </div>
                    </div>
                    </Link>
                )}
                
                <hr className="d-block d-lg-none mt-1 mb-0" />
              </div>
              
            </div>
          </div>
        </div>
      </main>
  )
}

export default SearchUsers