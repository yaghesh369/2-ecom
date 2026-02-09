import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useCart } from "../context/CartContext";

function Checkoutpage() {
    const BASEURL = import.meta.env.VITE_DJANGO_BASE_URL;
    const navigate = useNavigate();
    const { clearCart } = useCart();
    const [form, setForm] = useState({
        name: "",
        address: "",
        phone: "",
        payment_method: "COD"
    });
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState(null);
    const handlechange = (e) => {
        setForm({
            ...form,
            [e.target.name]: e.target.value
        });
        };
    const handlesubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setMessage("");
        try {
            const res = await fetch(`${BASEURL}/api/orders/create/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(form),
            });
            const data = await res.json();
            if (res.ok) {
                setMessage("Order placed successfully!");
                fetch(`${BASEURL}/api/cart/`);
                clearCart();
                setTimeout(() => {
                    navigate("/");
                }, 2000);
            } else {
                setMessage(data.error || "Failed to place order.");
            }
        }
        catch (error) {
            setMessage("An error occurred. Please try again.");
        }

    }

    return (
        <div className="min-h-screen bg-gray-100 flex justify-center items-center py-6">
            <div className="bg-white shadow-lg rounded-2xl p-8 max-w-md w-full">
                <h2>Checkout</h2>
                <form onSubmit={handlesubmit} className="space-y-4">
                    <input type="text" placeholder="Full Name" name="name" className="w-full p-2 border rounded-lg" 
                    value={form.name} onChange={handlechange}
                    required/>
                    <textarea placeholder="Full Address" name="address" className="w-full p-2 border rounded-lg" 
                    value={form.address} onChange={handlechange}
                    required></textarea>
                    <input type="tel" name="phone" placeholder="Phone Number" className="w-full p-2 border rounded-lg" 
                    value={form.phone} onChange={handlechange}
                    required/>
                    <select name="payment_method" className="w-full p-2 border rounded-lg" 
                    value={form.payment_method} onChange={handlechange}>
                        <option value="COD">Cash on Delivery</option>
                        <option value="Online">Online Payment</option>
                    </select>
                    <button type="submit" className="w-full bg-blue-600 text-white p-2 rounded-lg" disabled={loading}>
                        {loading ? "Processing..." : "Place Order"}
                    </button>
                    {message && <p className="text-center mt-4">{message}</p>}
                </form>

            </div>
        </div>

    )
}
export default Checkoutpage;