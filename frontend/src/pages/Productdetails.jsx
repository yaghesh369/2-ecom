import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { useCart } from "../context/CartContext";

function Productdetails() {
  const { id } = useParams();
  const BASEURL = import.meta.env.VITE_DJANGO_BASE_URL;

  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isAdding, setIsAdding] = useState(false);
  const { addToCart } = useCart();

  useEffect(() => {
    fetch(`${BASEURL}/api/products/${id}/`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch product");
        }
        return response.json();
      })
      .then((data) => {
        setProduct(data);
        setLoading(false);
      })
      .catch((error) => {
        setError(error);
        setLoading(false);
      });
  }, [id, BASEURL]);

  const handleAddToCart = async () => {
    setIsAdding(true);
    try {
      await addToCart(product.id);
    } finally {
      setIsAdding(false);
    }
  };

  const getImageUrl = (imagePath) => {
    if (!imagePath) return '';
    if (imagePath.startsWith('http')) {
      return imagePath;
    }
    return `${BASEURL}${imagePath}`;
  };

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error.message}</p>;
  if (!product) return <p>No product found</p>;

  return (
    <div className="min-h-screen bg-gray-100 flex justify-center items-center py-10">
      <div className="bg-white shadow-lg rounded-2xl p-8 max-w-3xl w-full">
        <div className="flex flex-col md:flex-row gap-8">
          <img
            src={getImageUrl(product.image)}
            alt={product.name}
            className="w-full md:w-1/2 h-auto object-cover rounded-lg"
          />
          <div className="flex-1">
            <h1 className="text-3xl font-bold text-gray-800 mb-2">{product.name}</h1>
            <p className="text-gray-600 mb-4">{product.description}</p>
            <p className="text-2xl font-semibold text-green-600 mb-6">${product.price}</p>
            <button 
              onClick={handleAddToCart}
              disabled={isAdding}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition disabled:bg-gray-400 disabled:cursor-not-allowed"
            >
              {isAdding ? "Adding..." : "Add to Cart 🛒"}
            </button>
             {/* Home Button */}
            <div className="mt-4">
              <a
                href="/"
                className="text-blue-600 hover:underline"
              >
                &larr; Back to Home
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Productdetails;
