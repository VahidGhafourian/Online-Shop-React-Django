
import './App.css';
import 'bootstrap/dist/css/bootstrap.rtl.min.css'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Shop from './pages/shop/shop';
import Cart from './pages/cart/cart';
import Nav from './components/nav';
import Footer from './components/footer';
import Welcome from './components/welcome';
import {ShopContextProvider} from './context/shopContext'
import Login from './pages/authentication/login';
import OTP from './pages/authentication/otp';
import CreateProfile from './pages/authentication/createProfile';
import { AuthProvider } from './context/AuthContext';

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
            <Route path='/login' element={<Login />} />
            <Route path='/otp' element={<OTP />} />
            <Route path='/createProfile' element={<CreateProfile />} />
          </Routes>
          <Footer />
        </Router>
      </ShopContextProvider>
      </AuthProvider>
    </div>
  );
}

export default App;
