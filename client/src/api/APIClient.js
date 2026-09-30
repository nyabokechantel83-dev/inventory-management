const BASE_URL = import.meta.env.VITE_BASE_API_URL;

const APIClient = {
    __headers() {
        return {
            "Content-Type": "application/json"
        };
    },

    async get(path) {
        const response = await fetch(`${BASE_URL}${path}`, {
            method: "GET",
            headers: this.__headers(),
            credentials: "include"
        });

        if (!response.ok) {
            throw new Error(response.statusText);
        }

        return await response.json();
    },

    async post(path, payload) {
        const response = await fetch(`${BASE_URL}${path}`, {
            method: "POST",
            body: JSON.stringify(payload),
            headers: this.__headers(),
            credentials: "include"
        });

        if (!response.ok) {
            throw new Error(response.statusText);
        }

        return await response.json();
    },

    async patch(path, payload) {
        const response = await fetch(`${BASE_URL}${path}`, {
            method: "PATCH",
            body: JSON.stringify(payload),
            headers: this.__headers(),
            credentials: "include"
        });

        if (!response.ok) {
            throw new Error(response.statusText);
        }

        return await response.json();
    },

    async delete(path) {
        const response = await fetch(`${BASE_URL}${path}`, {
            method: "DELETE",
            headers: this.__headers(),
            credentials: "include"
        });

        if (!response.ok) {
            throw new Error(response.statusText);
        }

        return await response.json();
    }
};

export default APIClient;