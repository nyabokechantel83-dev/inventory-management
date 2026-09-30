import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import APIClient from "../api/APIClient";

function Products() {
    const navigate = useNavigate();

    const [products, setProducts] = useState([]);
    const [error, setError] = useState("");
    const [editingId, setEditingId] = useState(null);

    const [form, setForm] = useState({
        name: "",
        price: "",
        category: "",
        stock: ""
    });

    const loadProducts = async () => {
        try {
            const data = await APIClient.get("/products");
            setProducts(data);
        } catch (error) {
            setError("Could not load products");
        }
    };

    useEffect(() => {
        loadProducts();
    }, []);

    const handleChange = (e) => {
        setForm({
            ...form,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");

        const productData = {
            name: form.name,
            price: Number(form.price),
            category: form.category,
            stock: Number(form.stock)
        };

        try {
            if (editingId) {
                const updatedProduct = await APIClient.patch(
                    `/products/${editingId}`,
                    productData
                );

                setProducts(
                    products.map((product) =>
                        product.id === editingId
                            ? updatedProduct
                            : product
                    )
                );

                setEditingId(null);
            } else {
                const newProduct = await APIClient.post(
                    "/products",
                    productData
                );

                setProducts([...products, newProduct]);
            }

            setForm({
                name: "",
                price: "",
                category: "",
                stock: ""
            });
        } catch (error) {
            setError("Could not save product");
        }
    };

    const handleEdit = (product) => {
        setEditingId(product.id);

        setForm({
            name: product.name,
            price: product.price,
            category: product.category,
            stock: product.stock
        });
    };

    const handleDelete = async (id) => {
        try {
            await APIClient.delete(`/products/${id}`);

            setProducts(
                products.filter((product) => product.id !== id)
            );
        } catch (error) {
            setError("Could not delete product");
        }
    };

    const handleLogout = async () => {
        try {
            await APIClient.post("/logout");
            navigate("/signin");
        } catch (error) {
            setError("Could not logout");
        }
    };

    return (
        <div className="min-h-screen bg-gray-100 p-8">
            <div className="max-w-5xl mx-auto">

                <div className="flex justify-between items-center mb-8">
                    <h1 className="text-3xl font-bold">
                        Inventory Management
                    </h1>

                    <button
                        onClick={handleLogout}
                        className="bg-gray-800 text-white px-5 py-3 rounded-lg hover:bg-gray-900"
                    >
                        Logout
                    </button>
                </div>

                {error && (
                    <p className="bg-red-100 text-red-600 p-4 rounded-lg mb-6">
                        {error}
                    </p>
                )}

                <div className="bg-white rounded-xl shadow p-6 mb-8">
                    <h2 className="text-xl font-semibold mb-5">
                        {editingId ? "Edit Product" : "Add Product"}
                    </h2>

                    <form
                        onSubmit={handleSubmit}
                        className="grid grid-cols-1 md:grid-cols-2 gap-4"
                    >
                        <input
                            type="text"
                            name="name"
                            value={form.name}
                            onChange={handleChange}
                            placeholder="Product name"
                            className="border border-gray-300 rounded-lg px-4 py-3"
                            required
                        />

                        <input
                            type="number"
                            name="price"
                            value={form.price}
                            onChange={handleChange}
                            placeholder="Price"
                            min="1"
                            className="border border-gray-300 rounded-lg px-4 py-3"
                            required
                        />

                        <input
                            type="text"
                            name="category"
                            value={form.category}
                            onChange={handleChange}
                            placeholder="Category"
                            className="border border-gray-300 rounded-lg px-4 py-3"
                            required
                        />

                        <input
                            type="number"
                            name="stock"
                            value={form.stock}
                            onChange={handleChange}
                            placeholder="Stock"
                            min="0"
                            className="border border-gray-300 rounded-lg px-4 py-3"
                            required
                        />

                        <button
                            type="submit"
                            className="bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700"
                        >
                            {editingId ? "Update Product" : "Add Product"}
                        </button>

                        {editingId && (
                            <button
                                type="button"
                                onClick={() => {
                                    setEditingId(null);
                                    setForm({
                                        name: "",
                                        price: "",
                                        category: "",
                                        stock: ""
                                    });
                                }}
                                className="bg-gray-500 text-white py-3 rounded-lg font-semibold hover:bg-gray-600"
                            >
                                Cancel
                            </button>
                        )}
                    </form>
                </div>

                <div className="bg-white rounded-xl shadow">
                    <div className="p-6 border-b">
                        <h2 className="text-xl font-semibold">
                            Products
                        </h2>
                    </div>

                    {products.length === 0 && (
                        <p className="p-6 text-gray-500">
                            No products found.
                        </p>
                    )}

                    {products.map((product) => (
                        <div
                            key={product.id}
                            className="p-6 border-b flex justify-between items-center"
                        >
                            <div>
                                <h3 className="text-lg font-semibold">
                                    {product.name}
                                </h3>

                                <p className="text-gray-500">
                                    KSh {product.price}
                                </p>

                                <p className="text-gray-500">
                                    Category: {product.category}
                                </p>

                                <p className="text-gray-500">
                                    Stock: {product.stock}
                                </p>

                                <p className="text-gray-500">
                                    Added by user: {product.user_id}
                                </p>
                            </div>

                            <div className="flex gap-3">
                                <button
                                    onClick={() => handleEdit(product)}
                                    className="bg-yellow-500 text-white px-4 py-2 rounded-lg hover:bg-yellow-600"
                                >
                                    Edit
                                </button>

                                <button
                                    onClick={() => handleDelete(product.id)}
                                    className="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700"
                                >
                                    Delete
                                </button>
                            </div>
                        </div>
                    ))}
                </div>

            </div>
        </div>
    );
}

export default Products;