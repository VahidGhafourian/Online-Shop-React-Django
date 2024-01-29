
import './App.css';
import 'bootstrap/dist/css/bootstrap.rtl.min.css'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Shop from './pages/shop/shop';
import Cart from './pages/cart/cart';
import Nav from './components/nav';
import Footer from './components/footer';
import Welcome from './components/welcome';
import {ShopContextProvider} from './context/shopContext'
import OTP from './pages/authentication/otp';
import { AuthProvider } from './context/AuthContext';
import Login from './pages/authentication/login';
import Invoice from './pages/cart/invoice';
import Payment from './pages/cart/payment';
import Profile from './pages/authentication/profile';

function App() {
  return (
    <div className="App">
    <AuthProvider>
      <ShopContextProvider>
        <Router>
          <Nav />
          <Welcome />
          <Routes>
            <Route path='/' element={<Shop />} />
            <Route path='/cart' element={<Cart />} />
            <Route path='/invoice' element={<Invoice />} />
            <Route path='/login' element={<Login />} />
            <Route path='/payment' element={<Payment />} />
            <Route path='/profile' element={<Profile />} />
            <Route path='/otp/:phoneNumber' element={<OTP />} />
          </Routes>
          <Footer />
        </Router>
      </ShopContextProvider>
      </AuthProvider>
    </div>
  );
}

export default App;
