// CreateProfile.js

import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

const CreateProfile = () => {
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const { isLoggedIn, isPhoneNumberVerified, isOtpVerified } = useAuth();

  useEffect(() => {
    // Check if the user is not logged in, the phone number is not verified, or the OTP is not verified
    if (!isLoggedIn || !isPhoneNumberVerified || !isOtpVerified) {
      // Redirect to the login page or another appropriate location
      navigate('/login');
    }
  }, [isLoggedIn, isPhoneNumberVerified, isOtpVerified, navigate]);

  const handleCreateProfile = async () => {
    // Basic validation
    if (!firstName || !lastName || !email) {
      setError('All fields are required.');
      return;
    }

    // Send user profile data to the backend
    try {
      const response = await fetch('/api/create-profile', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          firstName,
          lastName,
          email,
        }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();

      if (data.success) {
        // If the backend indicates success, navigate to a success page or perform further actions
        console.log('Profile created successfully');
        navigate('/profileSuccess'); // Adjust the route according to your application
      } else {
        // If the backend indicates an error, show an error message
        setError('Failed to create profile. Please try again.');
      }
    } catch (error) {
      console.error('Error during profile creation:', error.message);
    }
  };

  return (
    <div>
      <h2>Create Your Profile</h2>
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
      {error && <p style={{ color: 'red' }}>{error}</p>}

      <button onClick={handleCreateProfile}>Create Profile</button>
    </div>
  );
};

export default CreateProfile;
