// AuthContext.js
import { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [isLoggedIn, setLoggedIn] = useState(false);
  const [isPhoneNumberVerified, setPhoneNumberVerified] = useState(false);
  const [isOtpVerified, setOtpVerified] = useState(false);
  const [token, setToken] = useState(null);
  const [refresh, setRefresh] = useState(null);
  const [user, setUser] = useState(null);

  const getUserInfo = async (token) => {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/account/user-info/", {
        method: "GET",
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
      })
      .then(response => response.json())
      .catch(error => console.error('Error:', error));
      setUser(response);
      return user
    } catch (error) {
      // Handle error (e.g., token expired, unauthorized)
      console.error("Error fetching user information:", error);
    }
  };

  const login = (token, refresh) => {
    setToken(token);
    setRefresh(refresh);
    localStorage.setItem("authToken", token);
    localStorage.setItem("authRefresh", refresh);
    setLoggedIn(true)
    // setUser(getUserInfo(token))
  };

  const verifyPhoneNumber = () => {
    // Simulate a successful phone number verification
    setPhoneNumberVerified(true);
  };

  const verifyOtp = () => {
    // Simulate a successful OTP verification
    setOtpVerified(true);
  };

  const logout = () => {
    // Implement your logout logic here
    // Reset all verification statuses
    setLoggedIn(false);
    setPhoneNumberVerified(false);
    setOtpVerified(false);
    setToken(null);
    setRefresh(null);
    setUser(null);
    localStorage.removeItem("authToken");
    localStorage.removeItem("authRefresh");
  };

  return (
    <AuthContext.Provider
      value={{ isLoggedIn, isPhoneNumberVerified, isOtpVerified, login, verifyPhoneNumber, verifyOtp, logout, getUserInfo }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  return useContext(AuthContext);
};
