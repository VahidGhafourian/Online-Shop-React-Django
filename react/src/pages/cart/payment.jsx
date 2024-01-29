import React, { useEffect, useState } from "react";
import axios from 'axios';
import { useContext } from "react"
import { useAuth } from "../../context/AuthContext";
import { ShopContext } from "../../context/shopContext";

const Payment = () => {
  const { accessToken } = useAuth();
  const { invoice } = useContext(ShopContext);
  const [paymentUrl, setPaymentUrl] = useState(null);

  useEffect(() => {
    const fetchPaymentUrl = async () => {
      try {
        const response = await axios.post(
          'http://127.0.0.1:8000/api/payment/',
          { transaction_id: invoice.transaction_id },
          {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('authToken')}`,
              'Content-Type': 'application/json',
            },
          }
        );

        setPaymentUrl(response.data.payment_url);
      } catch (error) {
        console.error('Error fetching payment URL:', error);
      }
    };

    fetchPaymentUrl();
  }, [invoice.transaction_id]);

    // window.location.href = 'https://sandbox.zarinpal.com/pg/StartPay/' + response.data.payment_url;

    return (
    <React.Fragment>
      <h1>Your Invoice</h1>
      {paymentUrl ? (
        <div>
          <p>
            User goes to the bank payment page, then comes back here, and sees the payment result and code.
          </p>
          <a href={`https://api.zarinpal.com/pg/StartPay/${paymentUrl}`} target="_blank" rel="noopener noreferrer">
            Proceed to Payment
          </a>
        </div>
      ) : (
        <p>Loading payment information...</p>
      )}

    </React.Fragment>
  )
}

export default Payment;
