// NextPage.js
import React, { useState } from 'react';
import { useAuth } from './AuthContext';

const NextPage = () => {
  const { phoneNumber } = useAuth();
  const [enteredPassword, setEnteredPassword] = useState('');

  const handleVerifyPassword = async () => {
    // Send the form (phone number and password) to the backend
    try {
      const response = await fetch('/api/verify-password', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          phoneNumber,
          password: enteredPassword,
        }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();

      if (data.success) {
        // If success is true, user is logged in, and you receive a token
        console.log('Login successful');
        // You can store the token or perform other actions here

        // Navigate to the next page or redirect to the desired location
      } else {
        // If success is false, inform the user to change the entered password
        console.error('Incorrect password. Please change your password.');
      }
    } catch (error) {
      console.error('Error during password verification:', error.message);
    }
  };

  return (
    <div>
      <h2>Next Page</h2>
      <p>Your Phone Number: {phoneNumber}</p>

      <label htmlFor="enteredPassword">Enter Password:</label>
      <input
        type="password"
        id="enteredPassword"
        value={enteredPassword}
        onChange={(e) => setEnteredPassword(e.target.value)}
      />

      <button onClick={handleVerifyPassword}>Verify Password</button>
    </div>
  );
};

export default NextPage;
