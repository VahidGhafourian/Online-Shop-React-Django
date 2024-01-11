import React from 'react';
import useSWR from 'swr';
import Product from './product'

const fetcher = (...args) => fetch(...args).then((res) => res.json());

const Shop =() => {
    const {
        data: products,
        error,
        isValidating,
    } = useSWR('http://localhost:8000', fetcher);

      // Handles error and loading state
    if (error) return <div className='failed'>failed to load</div>;
    if (isValidating) return <div className="Loading">Loading...</div>;
    
    return (
        <React.Fragment>
            <h1>
                Shop
            </h1>
            <div className='row'>
                {products.products.map((product) => {
                    return (<Product key={product.id} data={product} />)
                })}
            </div>
        </React.Fragment>
    )
}

export default Shop;
