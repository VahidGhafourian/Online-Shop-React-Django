import React from 'react';
import useSWR from 'swr';
import Product from './product'
import { Products } from './fake_product';
import Slideshow from '../../components/slideshow';

const fetcher = (...args) => fetch(...args).then((res) => res.json());

const Shop =() => {
  const {
    data: products,
    error,
    isValidating,
  } = useSWR('http://localhost:8000/api/products/', fetcher);

    // Handles error and loading state
  if (error) return <div className='failed'>failed to load</div>;
  if (isValidating) return <div className="Loading">Loading...</div>;

  return (
    <React.Fragment>
      <Slideshow />
      <h1>
          محصولات
      </h1>
      <div className='row'>
          {products.products.map((product) => {
          // {Products.map((product) => {
              return (<Product key={product.id} data={product} />)
          })}
      </div>
    </React.Fragment>
  )
}

export default Shop;
