// Profile.js

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from "../../context/AuthContext";
import { useNavigate } from 'react-router-dom';
import './profile.css';

const Profile = () => {
  const [userInfo, setUserInfo] = useState({});
  const [userAddresses, setUserAddresses] = useState([]);
  const [orders, setOrders] = useState([]);
  const { accessToken, resetAccessToken, isLoggedIn } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!isLoggedIn)
      navigate('/')
  }, [isLoggedIn])

  useEffect(() => {
    // Fetch user info
    const fetchData = async () => {
      await resetAccessToken();

      await axios.get('http://127.0.0.1:8000/api/account/user-info/', {
        headers: {
          'Authorization': `Bearer ${accessToken}`,
          'Content-Type': 'application/json',
        }})
        .then(response => setUserInfo(response.data))
        .catch(error => console.error('Error fetching user info:', error));

      // Fetch user addresses
      await axios.get('http://127.0.0.1:8000/api/account/user-addresses/', {
        headers: {
          'Authorization': `Bearer ${accessToken}`,
          'Content-Type': 'application/json',
        }})
        .then(response => setUserAddresses(response.data))
        .catch(error => console.error('Error fetching user addresses:', error));

      // Fetch user orders
      await axios.get('http://127.0.0.1:8000/api/orders/', {
        headers: {
          'Authorization': `Bearer ${accessToken}`,
          'Content-Type': 'application/json',
        }})
        .then(response => setOrders(response.data))
        .catch(error => console.error('Error fetching user orders:', error));
    }
    fetchData();
  }, [accessToken]);



  return (
    <div>
          {/* Display User Info */}
          <table>
            <thead>
              <tr>
                <th colspan="2">Account Information</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>First Name: </td>
                <td>{userInfo.first_name}</td>
              </tr>
              <tr>
                <td>Last Name: </td>
                <td>{userInfo.last_name}</td>
              </tr>
              <tr>
                <td>Phone Number: </td>
                <td>{userInfo.phone_number}</td>
              </tr>
              <tr>
                <td>Email:</td>
                <td>{userInfo.email}</td>
              </tr>
            </tbody>
          </table>

          {/* Display User Orders */}
          <table>
            <thead>
              <tr>
                <th>Order ID</th>
                <th>Is send</th>
                <th>Total</th>
              </tr>
            </thead>
            <tbody>
              {orders.map(order => (
                <tr key={order.id}>
                  <td>{order.id}</td>
                  <td>{order.is_send ? 'Sent' : 'Not Sent'}</td>
                  <td>{order.total}</td>
                </tr>
              ))}
            </tbody>
          </table>

          {/* Display User Addresses */}
          <table>
            <thead>
              <tr>
                <th>Address ID</th>
                <th>Address</th>
              </tr>
            </thead>
            <tbody>
              {userAddresses.map(address => (
                <tr key={address.id}>
                  <td>{address.id}</td>
                  <td>{address.street}, {address.city}, {address.country} </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
    // <div>
    //   <h1>User Profile</h1>

    //   {/* Display User Info */}
    //   <div>
    //     <h2>User Information</h2>
    //     <p>First Name: {userInfo.first_name}</p>
    //     <p>Last Name: {userInfo.last_name}</p>
    //     <p>Phone Number: {userInfo.phone_number}</p>
    //     <p>Email: {userInfo.email}</p>
    //     {/* Add other user information fields as needed */}
    //   </div>

    //   {/* Display User Addresses */}
    //   <div>
    //     <h2>User Addresses</h2>
    //     <ul>
    //       {userAddresses.map(address => (
    //         <li key={address.id}>
    //           {address.street}, {address.city}, {address.country}
    //         </li>
    //       ))}
    //     </ul>
    //   </div>

    //   {/* Display User Orders */}
    //   <div>
    //     <h2>User Orders</h2>
    //     <ul>
    //       {orders.map(order => (
    //         <li key={order.id}>
    //           Order ID: {order.id}, Total: {order.total}
    //         </li>
    //       ))}
    //     </ul>
    //   </div>
    // </div>
  );
};

export default Profile;
