import React, { useContext } from "react";
import { ShopContext } from "../../context/shopContext";
import Product from "../shop/product";

const Cart =() => {
    const {cartItems} = useContext(ShopContext)
    console.log(cartItems);
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
        </React.Fragment>
    )
}

export default Cart;
