import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import ProductList from "./pages/ProductList";
import Productdetails from "./pages/Productdetails";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<ProductList />} />
        <Route path="/product/:id" element={<Productdetails />} />
      </Routes>
    </Router>
  );
}

export default App;
