import { Link } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faShoppingCart } from "@fortawesome/free-solid-svg-icons";
import { useContext, useEffect, useState } from "react";
import { ShopContext } from "../context/shopContext";
import './nav.css';
import { useAuth } from '../context/AuthContext';

const Nav = () => {
    const { cartItems } = useContext(ShopContext);
    const { isLoggedIn, logout } = useAuth();

    const itemCount = cartItems?.reduce((prev, current) => {
        return prev + current.count;
    }, 0);


    return (
        <div className="navbar navbar-dark bg-dark navbar-expand-lg">
            <div className="container">

                <ul className="navbar-nav">
                    <li className="nav-item">
                        <Link to="/cart" className="nav-link">
                            سبد خرید
                            <FontAwesomeIcon icon={faShoppingCart} />
                            {itemCount > 0 && <span className="cart-item-count">{itemCount}</span>}
                        </Link>
                    </li>

                    {isLoggedIn ? (
                        // If user is logged in
                        <>
                            <li className="nav-item">
                                <Link to="/profile" className="nav-link">حساب</Link>
                            </li>
                            <li className="nav-item">
                                <button className="nav-link" onClick={logout}>خروج</button>
                            </li>
                        </>
                    ) : (
                        // If user is not logged in
                        <>
                            <li className="nav-item">
                                <Link to="/login" className="nav-link">ورود</Link>
                            </li>
                        </>
                    )}

                    <li className="nav-item">
                        <Link to="/" className="nav-link">صفحه اصلی</Link>
                    </li>
                </ul>
                <a className="navbar-brand">فروشگاه ظهور قهوه</a>
            </div>
        </div>
    );
};

export default Nav;
