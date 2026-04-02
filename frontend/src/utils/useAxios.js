import axios from 'axios';
import { jwtDecode } from 'jwt-decode';
import dayjs from 'dayjs';
import { useContext } from 'react';
import  AuthContext  from '../context/AuthContext';

// API base URL
const baseURL = 'http://127.0.0.1:8000/api'; // Replace with your API base URL

// Custom hook to use Axios with automatic token refresh
const useAxios = () => {
  // Get authTokens and setters from AuthContext
  const { authTokens, setAuthTokens, setUser } = useContext(AuthContext);

  // Create an Axios instance
  const axiosInstance = axios.create({
    baseURL,
    headers: { Authorization: `Bearer ${authTokens?.access}` },
  });

  // Add a request interceptor to handle token refresh
  axiosInstance.interceptors.request.use(async (req) => {
    if (!authTokens) {
      return req;
    }

    // Check if the access token is expired
    const user = jwtDecode(authTokens.access);
    const isExpired = dayjs.unix(user.exp).diff(dayjs()) < 1;

    if (!isExpired) {
      return req;
    }

    // Refresh the access token
    const response = await axios.post(`${baseURL}/token/refresh/`, {
      refresh: authTokens.refresh,
    });
    // Update local storage and context with new tokens
    localStorage.setItem('authTokens', JSON.stringify(response.data));
    
    // Update state with new tokens
    setAuthTokens(response.data);
    setUser(jwtDecode(response.data.access));
    
    // Attach the new access token to the request
    req.headers.Authorization = `Bearer ${response.data.access}`;
    return req; 
  });
  // Return the Axios instance
  return axiosInstance;
};

export default useAxios;


