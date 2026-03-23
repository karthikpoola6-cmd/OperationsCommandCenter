import axios from "axios";

const API = axios.create({
  baseURL: "/api",
});

// ── KPIs ──────────────────────────────────────────
export const fetchKPIs = () => API.get("/metrics/kpi");

// ── Incidents ─────────────────────────────────────
export const fetchIncidents = (params) => API.get("/incidents", { params });
export const fetchIncident = (id) => API.get(`/incidents/${id}`);
export const createIncident = (data) => API.post("/incidents", data);
export const updateIncident = (id, data) => API.patch(`/incidents/${id}`, data);
export const fetchIncidentTrend = (days = 30) =>
  API.get("/incidents/trend", { params: { days } });

// ── Alerts ────────────────────────────────────────
export const fetchAlerts = (params) => API.get("/alerts", { params });
export const acknowledgeAlert = (id) => API.patch(`/alerts/${id}/acknowledge`);

// ── Shipments ─────────────────────────────────────
export const fetchShipments = (params) => API.get("/shipments", { params });
export const fetchShipment = (id) => API.get(`/shipments/${id}`);

// ── Metrics ───────────────────────────────────────
export const fetchMetrics = (params) => API.get("/metrics", { params });
export const fetchDelaysByRegion = () => API.get("/metrics/delays-by-region");

// ── Detection ─────────────────────────────────────
export const runDetection = () => API.post("/detect/run");
export const generateAISummary = (incidentId) =>
  API.post(`/detect/incidents/${incidentId}/ai-summary`);

export default API;
