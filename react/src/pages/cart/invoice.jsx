import React, { useContext, useState, useEffect } from "react";
import { ShopContext } from "../../context/shopContext";
import './invoice.css';
import axios from 'axios';
import { useAuth } from "../../context/AuthContext";
import { useNavigate } from 'react-router-dom';

const Invoice = () => {
  const { cartItems, resetCart, addToCart, removeFromCart, setInvoice } = useContext(ShopContext);
  const [addresses, setAddresses] = useState([]);
  const [ selected_address_id, setSelectedAddress ] = useState(0);
  const { accessToken, resetAccessToken } = useAuth();
  const navigate = useNavigate();
  const [newAddressForm, setNewAddressForm] = useState({
    country: "",
    state: "",
    city: "",
    street: "",
    postal_code: "",
    is_default: false,
  });

  const handleSelectAddress = (addressId) => {
    setSelectedAddress(addressId)
  };

  useEffect(() => {
    // Fetch user's addresses from the backend
    const fetchAddresses = async () => {
      await resetAccessToken();
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/account/user-addresses/', {
          headers: {
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type': 'application/json',
          }});
        setAddresses(response.data);
      } catch (error) {
        console.error('Error fetching addresses:', error);
      }
    };

    fetchAddresses();
    // handleSelectAddress(0);
  }, [accessToken]);



  const handleCompletePayment = async () => {
    try {
      const items = cartItems.map(item => ({ id: item.id, quantity: item.count }));
      // Make a POST request to the backend to complete payment
      const invoice = await axios.post('http://127.0.0.1:8000/api/order_check_add/',
        { items: items,
          shipping_address: selected_address_id},
        { headers: {
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type': 'application/json',
        }});
      await setInvoice(invoice.data)
      // Reset the cart after successful payment
      // TODO:
      // resetCart();
      // Redirect to the payment page if needed
      navigate('/payment');  // Import useHistory from 'react-router-dom'
    } catch (error) {
      console.error('Error completing payment:', error);
    }
  };

  const handleAddAddress = async () => {
    try {
      // Make a POST request to add a new address
      const response = await axios.post('http://127.0.0.1:8000/api/account/add-address/', { newAddressForm: newAddressForm }, {
        headers: {
          'Authorization': `Bearer ${accessToken}`,
          'Content-Type': 'application/json',
        },
      });

      setAddresses([...addresses, response.data]);
      // Reset the new address form
      setNewAddressForm({
        country: "",
        state: "",
        city: "",
        street: "",
        postal_code: "",
        is_default: false,
      });
    } catch (error) {
      console.error('Error adding address:', error);
    }
  };


  return (
    <React.Fragment>
      <h1>Your Invoice</h1>

      {/* Addresses */}
      <div>
        <h2>Addresses</h2>
        <select onChange={(e) => handleSelectAddress(e.target.value)}>
          <option key='0' value='انتخاب کنید' selected={true} >
          انتخاب کنید
          </option>
          {addresses.map((address) => {
            return (
              <option key={address.id} value={address.id} selected={selected_address_id}>
                {address.street}, {address.city}, {address.state}, {address.country}
              </option>
              )
            })
          }
        </select>
      </div>

      {/* Cart Items */}
      <table className="table">
        <thead>
          <tr>
            <th>Product</th>
            <th>Quantity</th>
            <th>Price</th>
          </tr>
        </thead>
        <tbody>
          {cartItems?.map(item => (
            <tr key={item.item.id}>
              <td>{item.item.name}</td>
              <td>
                <button onClick={() => removeFromCart(item.item.id)}>-</button>
                {item.count}
                <button onClick={() => addToCart(item.item.id, item.item)}>+</button>
              </td>
              <td>{item.item.price}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <button className="btn btn-success m-3" onClick={handleCompletePayment}>
        پرداخت
      </button>

      {/* Add New Address Form */}
      <div>
        <h2>Add New Address</h2>
        <form>
          <label htmlFor="country">Country:</label>
          <input
            type="text"
            id="country"
            name="country"
            value={newAddressForm.country}
            onChange={(e) => setNewAddressForm({ ...newAddressForm, country: e.target.value })}
          />

          <label htmlFor="state">State:</label>
          <input
            type="text"
            id="state"
            name="state"
            value={newAddressForm.state}
            onChange={(e) => setNewAddressForm({ ...newAddressForm, state: e.target.value })}
          />

          <label htmlFor="city">City:</label>
          <input
            type="text"
            id="city"
            name="city"
            value={newAddressForm.city}
            onChange={(e) => setNewAddressForm({ ...newAddressForm, city: e.target.value })}
          />

          <label htmlFor="street">Street:</label>
          <input
            type="text"
            id="street"
            name="street"
            value={newAddressForm.street}
            onChange={(e) => setNewAddressForm({ ...newAddressForm, street: e.target.value })}
          />

          <label htmlFor="postal_code">Postal Code:</label>
          <input
            type="text"
            id="postal_code"
            name="postal_code"
            value={newAddressForm.postal_code}
            onChange={(e) => setNewAddressForm({ ...newAddressForm, postal_code: e.target.value })}
          />

          <label htmlFor="is_default">Default Address:</label>
          <input
            type="checkbox"
            id="is_default"
            name="is_default"
            checked={newAddressForm.is_default}
            onChange={(e) => setNewAddressForm({ ...newAddressForm, is_default: e.target.checked })}
          />
          <button type="button" onClick={handleAddAddress}>Add Address</button>
        </form>
      </div>
    </React.Fragment>
  );
}

export default Invoice;
