
import React from 'react';
import { Fade } from 'react-slideshow-image';
import 'react-slideshow-image/dist/styles.css'
import { Products } from '../pages/shop/fake_product';

const divStyle = {
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  backgroundSize: 'cover',
  height: '600px'
}

const Slideshow = () => {

  return (
    <div className="slide-container">
      <Fade >
        {Products.map((product, index) => (
          <div style={{ ...divStyle}} key={index}>
            <img style={{ width: '100%' }} src={product.image} />
          </div>
        ))}
      </Fade>
    </div>
  )
}

export default Slideshow;


// ============================ Slide
// import React, { useRef } from 'react';
// import { Slide } from 'react-slideshow-image';
// import 'react-slideshow-image/dist/styles.css';
// import { Products } from '../pages/shop/fake_product';

// const spanStyle = {
//     padding: '20px',
//     background: '#efefef',
//     color: '#000000'
//   }

//   const divStyle = {
//     display: 'flex',
//     alignItems: 'center',
//     justifyContent: 'center',
//     backgroundSize: 'cover',
//     height: '400px'
//   }
// const Slideshow = () => {
//   const slideRef = useRef(null);

//   const handlePrev = () => {
//     if (slideRef.current) {
//       slideRef.current.goBack();
//     }
//   };

//   const handleNext = () => {
//     if (slideRef.current) {
//       slideRef.current.goNext();
//     }
//   };

//   return (
//     <div className="slide-container">
//       <Slide ref={slideRef}>
//         {Products.map((product, index) => (
//           <div key={index}>
//             <div style={{ ...divStyle, backgroundImage: `url(${product.image})`, position: 'relative' }}>
//               <span style={spanStyle}>{product.name}</span>
//             </div>
//           </div>
//         ))}
//       </Slide>
//       <div style={{ position: 'absolute', top: '50%', left: '10px', transform: 'translateY(-50%)', cursor: 'pointer' }} onClick={handlePrev}>
//         {'<'}
//       </div>
//       <div style={{ position: 'absolute', top: '50%', right: '10px', transform: 'translateY(-50%)', cursor: 'pointer' }} onClick={handleNext}>
//         {'>'}
//       </div>
//     </div>
//   );
// };

// export default Slideshow;
