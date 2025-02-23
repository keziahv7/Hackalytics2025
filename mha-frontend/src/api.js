const API_URL = "http://127.0.0.1:5000"; // Update if deployed

export const signup = async (email, password) => {
  const response = await fetch(`${API_URL}/signup`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  return response.json();
};

export const login = async (email, password) => {
  const response = await fetch(`${API_URL}/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  return response.json();
};

export const storeEntry = async (token, text) => {
  const response = await fetch(`${API_URL}/store_entry`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ token, text }),
  });
  return response.json();
};

export const getEntries = async (token) => {
  const response = await fetch(`${API_URL}/get_entries`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ token }),
  });
  return response.json();
};
