import { createContext, useEffect, useState } from "react";

export const ShopContext = createContext(null);

export const ShopContextProvider = (probs)=>{
    const [cartItems, setCartItems] = useState()

    useEffect(() => {
      const data = localStorage.getItem("coffee_cart")
      setCartItems(!!JSON.parse(data) ? JSON.parse(data) : [])

    }, [])

    useEffect(() => {
      if(cartItems !== undefined)
        localStorage.setItem("coffee_cart", JSON.stringify(cartItems))
    }, [cartItems])


    const addToCart = (itemId, item) => {
        if( ! cartItems?.find((item)=>item.id===itemId))
            setCartItems([...cartItems, {id: itemId, count: 1, item: item}])
        else
            setCartItems(cartItems.map((item) => {
                if(item.id===itemId)
                    return {...item, count: item.count+1}
                else return item
            }))
    }

    const removeFromCart = (itemId) => {
        setCartItems(cartItems.map((i)=>{
            if (i.id===itemId)
                return {...i, count: i.count===0 ? 0 : i.count - 1}
            else return i
        }))
    }

    const contextValue = {cartItems, addToCart,removeFromCart }

    return <ShopContext.Provider value={contextValue}>{probs.children}</ShopContext.Provider>
}
