import { useEffect, useState } from "react";
import { Navigate } from "react-router-dom";
import APIClient from "../api/APIClient";

function ProtectedRoute({ children }) {
    const [authenticated, setAuthenticated] = useState(null);

    useEffect(() => {
        const checkAuthentication = async () => {
            try {
                await APIClient.get("/me");
                setAuthenticated(true);
            } catch (error) {
                setAuthenticated(false);
            }
        };

        checkAuthentication();
    }, []);

    if (authenticated === null) {
        return <div>Loading...</div>;
    }

    if (!authenticated) {
        return <Navigate to="/signin" />;
    }

    return children;
}

export default ProtectedRoute;