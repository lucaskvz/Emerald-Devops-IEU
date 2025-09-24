import axios from "axios";

const API_URL = "http://127.0.0.1:8000"; 
// Later we can replace this with: process.env.REACT_APP_API_URL

// Emeralds
export const listEmeralds = () => axios.get(`${API_URL}/emeralds/`);
export const createEmerald = (payload) => axios.post(`${API_URL}/emeralds/`, payload);
export const updateEmerald = (id, payload) => axios.put(`${API_URL}/emeralds/${id}`, payload);
export const deleteEmerald = (id) => axios.delete(`${API_URL}/emeralds/${id}`);

// Counterparties 
// Counterparties 
export const listCounterparties = () => axios.get(`${API_URL}/counterparties/`);
export const createCounterparty = (payload) => axios.post(`${API_URL}/counterparties/`, payload);
export const updateCounterparty = (id, payload) => axios.put(`${API_URL}/counterparties/${id}`, payload);
export const deleteCounterparty = (id) => axios.delete(`${API_URL}/counterparties/${id}`);

// Trades (for later)
export const listTrades = () => axios.get(`${API_URL}/trades/`);
export const createTrade = (payload) => axios.post(`${API_URL}/trades/`, payload);
export const updateTrade = (id, payload) => axios.put(`${API_URL}/trades/${id}`, payload);
export const deleteTrade = (id) => axios.delete(`${API_URL}/trades/${id}`);
