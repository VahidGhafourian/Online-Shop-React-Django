import { Link } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faShoppingCart } from "@fortawesome/free-solid-svg-icons";
import { useContext, useEffect, useState } from "react";
import { ShopContext } from "../context/shopContext";
import './nav.css';
import { useAuth } from "../context/AuthContext";

const Nav = () => {
    const { cartItems } = useContext(ShopContext);
    const { getUserInfo, isLoggedIn } = useAuth()
    const [loggedIn, setLoggedIn] = useState(isLoggedIn);
    const [user, setUser] = useState(null);
    useEffect(() => {
        setLoggedIn(isLoggedIn); // Update the local state when isLoggedIn changes
    }, [isLoggedIn]);

    const itemCount = cartItems?.reduce((prev, current) => {
        return prev + current.count;
    }, 0);
    useEffect(() => {
        const fetchData = async () => {
            try {
              const authToken = localStorage.getItem('authToken');
              const response = await getUserInfo(authToken);
              console.log(response);
                if (response != null) {
                    response.then(result => {
                        console.log(result);
                    })
                    // setUser(response);
                } else {
                    // Handle the case where response is null or undefined
                    console.error("User information not available.");
                    setUser(null);
                }
            } catch (error) {
              console.error("Error fetching user information:", error);
              setUser(null);
            }
          };

          fetchData();
    }, [loggedIn, ])


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

                    {user ? (
                        // If user is logged in
                        <>
                            <li className="nav-item">
                                <Link to="/profile" className="nav-link">حساب</Link>
                            </li>
                            <li className="nav-item">
                                <Link to="/logout" className="nav-link">خروج</Link>
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
