import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

const OTP = () => {
  const [otp, setOtp] = useState(['', '', '', '', '']);
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const { isLoggedIn, isPhoneNumberVerified, isOtpVerified, verifyOtp } = useAuth();


  useEffect(() => {
    // Check if the user is not logged in or the phone number is not verified
    if (!isLoggedIn || !isPhoneNumberVerified) {
        // Redirect to the login page or another appropriate location
        navigate('/login');
    }
  }, [isLoggedIn, isPhoneNumberVerified, isOtpVerified, navigate]);

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
        const response = await fetch('/api/verify-otp', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ otp: otp.join('') }),
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const data = await response.json();

        if (data.state) {
          // If state is true, user is verified, navigate to the next page
          verifyOtp();
          if (isOtpVerified) {
            navigate('/createProfile');
          }
        } else {
          // If state is false, show error
          setError('Incorrect OTP. Please try again.');
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
