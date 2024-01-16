import { useAuth } from "../../context/AuthContext";
import { useNavigate } from 'react-router-dom';

const Logout = () => {
    const navigate = useNavigate();
    console.log('logging out');
    const { logout } = useAuth();
    logout();
    navigate('/');
}

export default Logout;
