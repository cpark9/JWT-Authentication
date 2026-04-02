import {createContext, useState, useEffect} from "react";
import { jwtDecode } from "jwt-decode"; 
import { useNavigate } from "react-router-dom";
const swal = require('sweetalert2')

// Create Context
const AuthContext = createContext();

export default AuthContext

// AuthProvider : 애플리케이션 전체(또는 특정 범위)를 감싸는 공급자 역할을 합니다. 이 안에 담긴 데이터는 children(하위 컴포넌트들) 어디서든 접근 가능
export const AuthProvider = ({ children }) => {
    const [authTokens, setAuthTokens] = useState(() =>
        localStorage.getItem("authTokens")
            // 데이터가 있고, 'undefined' 문자열이 아닐 때만 파싱
            ? JSON.parse(localStorage.getItem("authTokens"))
            : null
    );
    
    const [user, setUser] = useState(() => 
        localStorage.getItem("authTokens")
            ? jwtDecode(localStorage.getItem("authTokens"))
            : null
    );

    const [loading, setLoading] = useState(true);

    const navigate = useNavigate();

    const loginUser = async (email, password) => {
        try {
        
            // // 1. API 요청 시도 
            // 사용자가 입력한 email, password를 JSON 형태로 변환하여 백엔드 서버(Django 등)의 인증 엔드포인트로 비동기 POST 요청을 보냅니다.
            const response = await fetch("http://127.0.0.1:8000/api/token/", {
                method: "POST",
                headers:{
                    "Content-Type":"application/json"
                },
                body: JSON.stringify({
                    email, password
                })
            })

            // 2. 응답 데이터 파싱
            // 서버로부터 받은 응답(주로 Access/Refresh 토큰 포함)을 JavaScript 객체로 변환합니다.
            const data = await response.json()
            console.log(data);

            // 3. 응답 상태 체크 (200 OK)
            // HTTP 상태 코드가 200(OK)인 경우에만 로그인 성공 로직을 실행합니다.
            if(response.status === 200){
                console.log("Logged In");

                // 데이터 저장 및 상태 업데이트
                // 받은 토큰을 상태 관리 라이브러리(Context API, Redux 등)에 저장하고, jwt-decode를 사용해 토큰 내 사용자 정보(이름, ID 등)를 추출하여 UI에 반영합
                setAuthTokens(data)
                setUser(jwtDecode(data.access))
                // 브라우저를 새로고침해도 로그인이 유지되도록 토큰 데이터를 로컬 스토리지에 물리적으로 저장합니다.
                // localStorage에 저장된 토큰은 자바스크립트로 누구나 접근 가능합니다.
                // 보안을 강화하려면 Refresh Token은 브라우저 자바스크립트가 접근할 수 없는 HttpOnly; Secure 설정이 된 Cookie에 저장하는 것이 권장됩니다. MDN: HTTP 쿠키 가이드를 참고하세요.
                localStorage.setItem("authTokens", JSON.stringify(data))

                // 페이지 이동 및 성공 알림
                // 사용자를 메인 페이지로 리다이렉트하고, SweetAlert2를 이용해 성공/실패 알림창을 띄웁니다.
                navigate("/"); 
                swal.fire({
                    title: "Login Successful",
                    icon: "success",
                    toast: true,
                    timer: 6000,
                    position: 'top-right',
                    timerProgressBar: true,
                    showConfirmButton: false,
                })

            } else {
                // 4. 서버에서 의도한 에러 응답 (401, 400 등) 처리    
                console.log(response.status);
                console.log("there was a server issue");
                swal.fire({
                    title: "Username or passowrd does not exists",
                    icon: "error",
                    toast: true,
                    timer: 6000,
                    position: 'top-right',
                    timerProgressBar: true,
                    showConfirmButton: false,
                })
            }
        } catch (error) {
            // 5. 네트워크 연결 끊김, 서버 다운 등 예상치 못한 예외 처리
            console.error("Network or Server Error:", error);
            swal.fire({
                title: "Server is not responding",
                text: "Please check your internet connection or try again later.",
                icon: "warning",
                toast: true,
                timer: 6000,
                position: 'top-right',
                timerProgressBar: true,
                showConfirmButton: false,
            });
        }
    }

    const registerUser = async (email, username, password, password2) => {
        const response = await fetch("http://127.0.0.1:8000/api/register/", {
            method: "POST",
            headers: {
                "Content-Type":"application/json"
            },
            body: JSON.stringify({
                email, username, password, password2
            })
        })
        if(response.status === 201){
            navigate("/login"); 
            swal.fire({
                title: "Registration Successful, Login Now",
                icon: "success",
                toast: true,
                timer: 6000,
                position: 'top-right',
                timerProgressBar: true,
                showConfirmButton: false,
            })
        } else {
            console.log(response.status);
            console.log("there was a server issue");
            swal.fire({
                title: "An Error Occured " + response.status,
                icon: "error",
                toast: true,
                timer: 6000,
                position: 'top-right', 
                timerProgressBar: true,
                showConfirmButton: false,
            })
        }
    }

    const logoutUser = () => {
        setAuthTokens(null)
        setUser(null)
        localStorage.removeItem("authTokens")
        navigate("/login"); 
        swal.fire({
            title: "YOu have been logged out...",
            icon: "success",
            toast: true,
            timer: 6000,
            position: 'top-right',
            timerProgressBar: true,
            showConfirmButton: false,
        })
    }

    const contextData = {
        user, 
        setUser,
        authTokens,
        setAuthTokens,
        registerUser,
        loginUser,
        logoutUser,
    }

    useEffect(() => {
        if (authTokens) {
            setUser(jwtDecode(authTokens.access))
        }
        setLoading(false)
    }, [authTokens, loading])

    return (
        <AuthContext.Provider value={contextData}>
            {loading ? null : children}
        </AuthContext.Provider>
    )

}