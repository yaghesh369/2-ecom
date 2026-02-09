import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import ProductList from "./pages/ProductList";
import Productdetails from "./pages/Productdetails";
import Navbar from "./components/Navbar";
import CartPage from "./pages/CartPage";
import Checkoutpage from "./pages/Checkoutpage";

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<ProductList />} />
        <Route path="/product/:id" element={<Productdetails />} />
        <Route path="/cart" element={<CartPage />} />
        <Route path="/checkout" element={<Checkoutpage />} />
      </Routes>
    </Router>
  );
}

export default App;
