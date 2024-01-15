// Import useEffect to handle side effects and useHistory to navigate
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';


const Login = () => {
  const [phoneNumber, setPhoneNumber] = useState('');
  const [error, setError] = useState('');
  const [isNewUser, setIsNewUser] = useState(false);
  const [otp, setOtp] = useState('');
  const navigate = useNavigate();
  const { isLoggedIn, isPhoneNumberVerified, login, verifyPhoneNumber } = useAuth();
  const [showPasswordForm, setShowPasswordForm] = useState(false);
  const [password, setPassword] = useState('');



  useEffect(() => {
    if (isNewUser) {
        console.log('redirct to otp');
      navigate(`/otp/${phoneNumber}`);
    }
  }, [isNewUser, navigate]);

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
    // Check if the phone number is valid before attempting to log in
    if (!error) {
        if(showPasswordForm) {
            try {
                const response = await fetch('http://127.0.0.1:8000/api/account/token/', {
                  method: 'POST',
                  headers: {
                    'Content-Type': 'application/json',
                  },
                  body: JSON.stringify({
                    'phone_number': phoneNumber,
                    password,
                  }),
                });

                if (!response.ok) {
                  throw new Error('Network response was not ok');
                }

                const data = await response.json();
                if (data.access) {
                  // If success is true, user is logged in, and you receive a token
                  console.log('Login successful');
                  console.log(data);
                  localStorage.setItem('access', data.access)
                  localStorage.setItem('refresh', data.refresh)
                  navigate('/');
                  // You can store the token or perform other actions here

                  // Navigate to the next page or redirect to the desired location
                } else {
                  // If success is false, inform the user to change the entered password
                  console.error('Incorrect password. Please change your password.');
                }
              } catch (error) {
                console.error('Error during password verification:', error.message);
              }
        }
        try {
            const response = await fetch('http://127.0.0.1:8000/api/account/check-login-phone/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ phoneNumber }),
            });

            if (!response.ok) {
            throw new Error('Network response was not ok');
            }

            const data = await response.json();

            login();
            verifyPhoneNumber();

            if (data.newUser) {
                setIsNewUser(true);
            } else {
            // If the user is not new, show the password form
                if (!isNewUser) {
                    setShowPasswordForm(true);
                }
            }


        } catch (error) {
            console.error('Error during login:', error.message);
        }
    } else {
      console.error('Invalid phone number. Please correct the errors.');
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

      <button onClick={handleLogin} disabled={!!error}>{showPasswordForm ? 'Login' : 'Next'}</button>

    </div>
  );
};

export default Login;
