import React, { useEffect, useState } from 'react';
import { useNavigate, useParams  } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

const OTP = () => {
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
  const [otp, setOtp] = useState(['', '', '', '', '']);
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const { isPhoneNumberVerified, isOtpVerified, verifyOtp, login } = useAuth();
  const { phoneNumber } = useParams();

  useEffect(() => {
    // Check if the user is not logged in or the phone number is not verified
    if (!isPhoneNumberVerified) {
        // Redirect to the login page or another appropriate location
        navigate('/login');
    }
  }, [isPhoneNumberVerified, isOtpVerified, navigate]);

//   Sending OTP Message
    useEffect(() => {
        try {
            const response = fetch('http://127.0.0.1:8000/api/account/send-otp/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ phoneNumber }),
            });
        }
        catch (error) {
            console.error('Error during OTP verification:', error.message);
        }
    }, []);

  const handleOtpChange = (index, value) => {
    const newOtp = [...otp];
    newOtp[index] = value;
    setOtp(newOtp);

    // Validate the OTP (5 digits)
    if (!/^\d{5}$/.test(newOtp.join(''))) {
      setError('Invalid OTP. It should be a 5-digit code.');
    } else {
      setError('');
    }

    // Move focus to the next input box
    if (index < otp.length - 1 && value !== '') {
      document.getElementById(`otpInput${index + 1}`).focus();
    }
  };

  const handleKeyDown = (index, e) => {
    if (e.key === 'Backspace' && index > 0 && otp[index] === '') {
      // Move focus to the previous input box on Backspace
      document.getElementById(`otpInput${index - 1}`).focus();
    }
  };

  const handleVerifyOtp = async () => {
    // Check if the OTP is valid before sending to the backend
    if (!error) {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/account/verify-otp/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            otp: otp.join(''),
            phone_number: phoneNumber,
            'first_name': firstName,
            'last_name': lastName,
            'password': password,
            'confirm_password': confirmPassword,
            'email': email, }),
        });
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const data = await response.json();
        if (data.success) {
          // If state is true, user is verified, navigate to the next page
          console.log('Profile created successfully');
          verifyOtp();
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
              login(data.access, data.refresh)
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
          navigate('/');
        } else {
          // If state is false, show error
          setError('Failed to create profile. Incorrect OTP. Please try again.');
        }
      } catch (error) {
        console.error('Error during OTP verification:', error.message);
      }
    } else {
      console.error('Invalid OTP. Please correct the errors.');
    }
  };

  return (
    <div>
      <h2>Create Your Profile</h2>
      <label value={phoneNumber}>Phone Number: {phoneNumber}</label>
      <label htmlFor="firstName">First Name:</label>
      <input
        type="text"
        id="firstName"
        value={firstName}
        onChange={(e) => setFirstName(e.target.value)}
      />

      <label htmlFor="lastName">Last Name:</label>
      <input
        type="text"
        id="lastName"
        value={lastName}
        onChange={(e) => setLastName(e.target.value)}
      />

      <label htmlFor="email">Email:</label>
      <input
        type="email"
        id="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />

      <label htmlFor="password">password:</label>
      <input
        type="password"
        id="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />

      <label htmlFor="confirm_password">confirm password:</label>
      <input
        type="password"
        id="confirm_password"
        value={confirmPassword}
        onChange={(e) => setConfirmPassword(e.target.value)}
      />
      <h2>Enter OTP</h2>
      <div style={{ display: 'flex', gap: '10px' }}>
        {otp.map((digit, index) => (
          <input
            key={index}
            type="text"
            value={digit}
            onChange={(e) => handleOtpChange(index, e.target.value)}
            onKeyDown={(e) => handleKeyDown(index, e)}
            id={`otpInput${index}`}
            maxLength="1"
          />
        ))}
      </div>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <button onClick={handleVerifyOtp} disabled={!!error}>
        Verify OTP
      </button>
    </div>
  );
};

export default OTP;
