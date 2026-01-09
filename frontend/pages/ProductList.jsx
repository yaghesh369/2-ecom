import { use, useEffect, useState } from "react";
import ProductCard from "../components/ProductCard";

function ProductList() {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const BASEURL= import.meta.env.VITE_DJANGO_BASE_URL

    useEffect(() => {
        fetch(`${BASEURL}/api/products/`)
        .then ((response)=>{
            if (!response.ok){
                throw new Error("failed to fetch products")
            }
            return response.json()
        })
        .then ( (data)=>{

            setProducts(data)
            setLoading(false)

        })
        .catch ((error)=>{
            setError(error)
            setLoading(false)
        })


    },[])
    if (loading){
        return <p>Loading...</p>
    }
    if (error){
        return <p>{error.message}</p>
    }
    return (
        <div className="min-h-screen bg-gray-100">
            <h1 className="text-3xl font-bold underline text-center py-6 bg-white shadow-md">
                Product List
            </h1>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 p-6">
                {products.length > 0 ? (
                    products.map((product) => (
                        <ProductCard key={product.id} product={product} />
                    ))
                ) : (
                    <p className=" col-span-full text-center text-gray-600">No products found.</p>
                )}

            </div>


        </div>
    )
    
}
export default ProductList