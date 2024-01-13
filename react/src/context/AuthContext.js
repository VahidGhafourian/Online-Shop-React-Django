// AuthContext.js
import { createContext, useContext, useState } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [isLoggedIn, setLoggedIn] = useState(false);
  const [isPhoneNumberVerified, setPhoneNumberVerified] = useState(false);
  const [isOtpVerified, setOtpVerified] = useState(false);
  const login = () => {
    // Simulate a successful login
    setLoggedIn(true);
    setPhoneNumberVerified(false); // Reset the verification status
    setOtpVerified(false); // Reset the verification status
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
  };

  return (
    <AuthContext.Provider
      value={{ isLoggedIn, isPhoneNumberVerified, isOtpVerified, login, verifyPhoneNumber, verifyOtp, logout }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  return useContext(AuthContext);
};
