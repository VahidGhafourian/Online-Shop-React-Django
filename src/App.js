
import './App.css';
import 'bootstrap/dist/css/bootstrap.rtl.min.css'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Shop from './pages/shop/shop';
import Cart from './pages/cart/cart';
import Nav from './components/nav';
import Footer from './components/footer';
import Welcome from './components/welcome';
import {ShopContextProvider} from './context/shopContext'

function App() {
  return (
    <div className="App">
      <ShopContextProvider>
        <Router>
          <Nav />
          <Welcome />
          <Routes>
            <Route path='/' element={<Shop />} />
            <Route path='/cart' element={<Cart />} />
          </Routes>
          <Footer />
        </Router>
      </ShopContextProvider>
    </div>
  );
}

export default App;
