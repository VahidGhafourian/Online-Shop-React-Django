// Import useEffect to handle side effects and useHistory to navigate
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';


const Login = () => {
  const { login, setNew, isLoggedIn, setIsLoggedIn } = useAuth();
  const navigate = useNavigate();

  const [phoneNumber, setPhoneNumber] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [showPasswordForm, setShowPasswordForm] = useState(false);

  useEffect(() => {
    if (isLoggedIn)
      navigate('/')
  }, [isLoggedIn])


  const handlePhoneNumberChange = (e) => {
    const inputPhoneNumber = e.target.value;
    setPhoneNumber(inputPhoneNumber);

    // Validate the phone number
    if (!/^(09)\d{9}$/.test(inputPhoneNumber)) {
      setError('شماره تماس درست نیست. شماره تماس شما باید با 09 شروع شده و دقیقا 11 رقم باشد');
    } else {
      setError('');
    }
  };

  const handleLogin = async () => {
    // Call API to check login status based on phone number
    try {
      // Dummy API call, replace with actual API calls
      const response = await fetch('http://127.0.0.1:8000/api/account/check-login-phone/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ phoneNumber }),
      });

      const result = await response.json();

      if (result.newUser) {
        setNew(true);
        navigate(`/otp/${phoneNumber}`);
      } else {
        // If existing user, show password field
        // You may want to redirect to the main page or handle login logic here
        // For simplicity, assuming the API returns is_new_user correctly
        // You should replace this with actual API response handling
        setShowPasswordForm(true);
      }
    } catch (error) {
      console.error('Error checking login status:', error);
    }
  };

  const handleFormSubmit = async () => {
    // Handle logic for existing user (e.g., login and save tokens)
    try {
      // Dummy API call, replace with actual API calls
      const response = await fetch('http://127.0.0.1:8000/api/account/token/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          phone_number: phoneNumber,
          password: password,
        }),
      });

      const result = await response.json();

      if (result.access) {
        // Save tokens and update login status
        login(result);
        setIsLoggedIn(true)
        navigate('/');
      } else {
        // Handle login failure
        console.error('Login failed:', result.error);
      }
    } catch (error) {
      console.error('Error during login:', error);
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <label htmlFor="phoneNumber">Phone Number:</label>
      <input
        type="text"
        id="phoneNumber"
        value={phoneNumber}
        onChange={handlePhoneNumberChange}
      />

    {showPasswordForm && (
        <>
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </>
      )}

      {error && <p style={{ color: 'red' }}>{error}</p>}

      <button onClick={showPasswordForm ? handleFormSubmit : handleLogin} disabled={!!error}>{showPasswordForm ? 'Login' : 'Next'}</button>

    </div>
  );
};

export default Login;
