// src/context/AuthContext.js
import React, { createContext, useState, useContext, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [isNewUser, setIsNewUser] = useState(false);
  const [accessToken, setAccessToken] = useState(null);
  const [refreshToken, setRefreshToken] = useState(null);

  useEffect(() => {
    // Retrieve tokens from localStorage on component mount
    const storedAccessToken = localStorage.getItem('authToken');
    const storedRefreshToken = localStorage.getItem('authRefresh');

    if (storedAccessToken && storedRefreshToken) {
      setAccessToken(storedAccessToken);
      setRefreshToken(storedRefreshToken);
      setIsLoggedIn(true);
    }
  }, []);

  const login = (tokens) => {
    setAccessToken(tokens.access);
    setRefreshToken(tokens.refresh);
    localStorage.setItem("authToken", tokens.access);
    localStorage.setItem("authRefresh", tokens.refresh);
    setIsLoggedIn(true);
  };

  const logout = () => {
    setAccessToken(null);
    setRefreshToken(null);
    localStorage.removeItem("authToken");
    localStorage.removeItem("authRefresh");
    setIsLoggedIn(false);
  };

  const resetAccessToken = async () => {
    const response = await fetch("http://127.0.0.1:8000/api/account/user-info/", {
      method: "GET",
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,
      },
    }).then(response => response.json())
    try {
      if (response.code==='token_not_valid') {
        const res = await axios.post(`http://127.0.0.1:8000/api/account/token/refresh/`, {
          refresh: localStorage.getItem('authRefresh'),
        });
        setAccessToken(res.data.access)
        localStorage.setItem("authToken", res.data.access);
      }
    } catch (error) {
      console.error('Error refreshing access token:', error);
      console.log("logging out ");
      logout()
      // throw error;
    }
  }

  const getUserInfo = async (token) => {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/account/user-info/", {
        method: "GET",
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
      }).then(response => response.json())
      .catch(error => console.error('Error:', error));
    } catch (error) {
      // Handle error (e.g., token expired, unauthorized)
      console.error("Error fetching user information:", error);
    }
  };

  const setNew = (value) => {
    setIsNewUser(value)
  }

  const contextValue = {
    isLoggedIn, isNewUser, setNew, setIsLoggedIn, resetAccessToken,
    accessToken,
    refreshToken,
    login,
    logout,
  };

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  return useContext(AuthContext);
};
