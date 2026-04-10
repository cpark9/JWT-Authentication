import {useState, useEffect, useCallback } from 'react'
import useAxios from '../utils/useAxios'
// import jwtDecode from 'jwt-decode'
import { jwtDecode } from 'jwt-decode';
import Swal from 'sweetalert2'


function Todo() {
    const baseUrl = "http://127.0.0.1:8000/api"
    const api = useAxios()

    const token = localStorage.getItem("authTokens") // 233704237huhweioyop;yrwriweyrwe
    const decoded = jwtDecode(token)
    const user_id = decoded.user_id

    const [todo, setTodo] = useState([])
    useEffect(() => {
        fetchTodos()
    }, [])

    const fetchTodos = async () => {
        await api.get(baseUrl + '/todo/').then((res) => {
            console.log(res.data);
            setTodo(res.data)
        })
    }
    
    const [createTodo, setCreateTodo] = useState({title: "", completed: ""})
    // 입력 감지 함수 (Event Handler)
    // [event.target.name]: 입력창(input)의 name 속성값
    // event.target.value: 입력창에 실제로 입력된 텍스트
    const handleNewTodoTitle = (event) => {
        setCreateTodo({
            ...createTodo,
            [event.target.name]: event.target.value
        })
    }
    // 콘솔에 입력된 할 일 제목이 잘 담기는지 확인하는 로그입니다. 개발할 때만 잠깐 찍어보는 용도입니다.
    console.log(createTodo.title);  

    
    const formSubmit = () => {
        // 1. 필수 입력 체크 로직 추가
        if (!createTodo.title || createTodo.title.trim() === "") {
            Swal.fire({
                title: "Error",
                text: "할 일 제목을 입력해주세요!",
                icon: "error",
                toast: true,
                position: "top-right",
                timer: 2000,
                showConfirmButton: false
            });
            return; // 제목이 없으면 여기서 함수 종료
        }

        const formdata = new FormData()

        formdata.append("user", user_id)
        formdata.append("title", createTodo.title)
        formdata.append("completed", false)

        try{
            api.post(baseUrl + '/todo/', formdata).then((res) => {
                console.log(res.data);
                Swal.fire({
                    title: "Todo Added",
                    icon:"success",
                    toast: true,
                    timer: 2000,
                    position: "top-right",
                    timerProgressBar: true,
                })
                fetchTodos()
                // 2. 상태를 통한 입력창 초기화 (권장 방식)
                setCreateTodo({title: "", completed: false}) 
            })
        } catch (error){
            console.log(error);
        }
    }

    const deleteTodo = async (todo_id) => {
        await api.delete(baseUrl + '/todo-detail/' + todo_id + '/')
        Swal.fire({
            title: "Todo Deleted",
            icon:"success",
            toast: true,
            timer: 2000,
            position: "top-right",
            timerProgressBar: true,
        })
        fetchTodos()
    }

    // const markTodoAsComplete = async (todo_id) => {
    //     await api.patch(baseUrl + '/todo-mark-as-completed/' + todo_id + '/')
    //     Swal.fire({
    //         title: "Todo Completed",
    //         icon:"success",
    //         toast: true,
    //         timer: 2000,
    //         position: "top-right",
    //         timerProgressBar: true,
    //     })
    //     fetchTodos()
    // }
    const markTodoAsComplete = async (todo_id) => {
        // 3. 완료 처리 시 데이터(completed)를 명시적으로 전달
        // PATCH 요청이라도 서버 시리얼라이저 설정에 따라 데이터를 요구할 수 있습니다.
        try {
            await api.patch(baseUrl + `/todo-mark-as-completed/${todo_id}/`, {
                completed: true
            })
            Swal.fire({
                title: "Todo Completed",
                icon: "success",
                toast: true,
                timer: 2000,
                position: "top-right",
                timerProgressBar: true,
            })
            fetchTodos()
        } catch (error) {
            console.error("완료 처리 중 에러 발생:", error.response?.data);
        }
    }


  return (
        <div>
            <div>
                <div className="container" style={{marginTop:"150px", padding:"10px"}}>
                    <div className="row justify-content-center align-items-center main-row">
                        <div className="col shadow main-col bg-white">
                            <div className="row bg-primary text-white">
                                <div className="col p-2">
                                    <h4>Todo App</h4>
                                </div>
                            </div>
                            <div className="row justify-content-between text-white p-2">
                                <div className="form-group flex-fill mb-2">
                                    <input id="todo-input" name='title' onChange={handleNewTodoTitle} value={createTodo.title} type="text" className="form-control" placeholder='Write a todo...'  />
                                </div>
                                <button type="button" onClick={formSubmit}  className="btn btn-primary mb-2 ml-2"> Add todo </button>
                            </div>
                            <div className="row" id="todo-container">
                                {todo.map((todo) => 
                                
                                <div className="col col-12 p-2 todo-item">
                                    <div className="input-group">
                                        {todo.completed.toString() === "true" && 
                                            <p className="form-control"><strike>{todo.title}</strike></p>
                                        }
                                        {todo.completed.toString() === "false" && 
                                            <p className="form-control">{todo.title}</p>
                                        }
                                        <div className="input-group-append">
                                            <button className="btn bg-success text-white ml-2" type="button" id="button-addon2 " onClick={() => markTodoAsComplete(todo.id)}><i className='fas fa-check' ></i></button>
                                            <button className="btn bg-danger text-white me-2 ms-2 ml-2" type="button" id="button-addon2 " onClick={() => deleteTodo(todo.id)}><i className='fas fa-trash' ></i></button>
                                        </div>
                                    </div>
                                </div>
                                )}
                                
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
  )
}

export default Todo