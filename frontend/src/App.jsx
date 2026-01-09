import { use, useEffect, useState } from "react";

function App(){
  const [products, setproducts] = useState([])
  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/products/")
      .then(response => response.json())
      .then(data => setproducts(data))
      .catch(error => console.log(error))
  }, [])
  return (
    <div className="min-h-screen bg-gray-100 p-4 ">
      <h1 className="text-3xl font-bold underline">
        products list
      </h1>
      <div className="container mx-auto p-4">
        {products.map(product => (
          <div key={product.id} className="bg-white p-4 mb-4">
            <h2>{product.name}</h2>
            <p>{product.description}</p>
            <p>{product.price}</p>
          </div>
        ))}

      </div>

    </div>
  )
    
}

export default App