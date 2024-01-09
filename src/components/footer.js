import { Link } from "react-router-dom";
import './footer.css'

const Footer =() => {
    return (
        <footer className="footer bg-dark text-light">
        <div className="container">
            <div className="row">
            <div className="col-lg-6">
                <p>© 2024 فروشگاه ظهور قهوه</p>
            </div>
            <div className="col-lg-6">
                <ul className="footer-nav">
                <li className="footer-item">
                    <Link to="/about" className="footer-link">درباره ما</Link>
                </li>
                <li className="footer-item">
                    <Link to="/contact" className="footer-link">تماس با ما</Link>
                </li>
                </ul>
            </div>
            </div>
        </div>
        </footer>


    )
}

export default Footer;
