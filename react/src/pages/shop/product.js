import { useContext, useState } from "react";
import { ShopContext } from "../../context/shopContext";
import './product.css'

const Product = (probs) => {
    // const {id, available, created, description, name, category, image, price, updated} = probs.data
    const {id, available, created, description, name, category, image, price, updated} = probs.data
    const {cartItems, addToCart, removeFromCart} = useContext(ShopContext)

    const isInCart = cartItems?.some((item)=> item.id === id)

    return (
        <div className="col-3">
            <img src={image}  />
            <h5>{name}</h5>
            <p>price: {price}T</p>
            <button className="btn btn-info btn-sm" onClick={() => {addToCart(id, probs.data)}} >+</button>
            <span className="mx-1">{cartItems?.filter((row)=> row.id===id)[0]?.count}</span>
            {isInCart && <button className="btn btn-info btn-sm" onClick={() => {removeFromCart(id)}} >-</button>}
        </div>
    )
}

export default Product;
