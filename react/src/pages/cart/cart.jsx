import React, { useContext } from "react";
import { ShopContext } from "../../context/shopContext";
import Product from "../shop/product";
import { Link } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

const Cart =() => {
    const {cartItems, resetCart} = useContext(ShopContext)
    const { isLoggedIn } = useAuth();
    return (
        <React.Fragment>
        <h1>
            Your cart Items
        </h1>
        <div className="row" >
            {
                cartItems?.map((item)=>{
                    if (item.count>0)
                        return <Product key={item.id} data={item.item}></Product>
                })
            }
        </div>
        <button className="btn btn-warning m-3" onClick={resetCart} >خالی کردن سبد خرید</button>
        <Link to={isLoggedIn ? '/invoice' : '/login'} className="btn btn-warning m-3" >تکمیل خرید</Link>
        </React.Fragment>
    )
}

export default Cart;
