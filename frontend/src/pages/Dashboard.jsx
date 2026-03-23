import { useState, useEffect } from "react";
import { Box, Grid, Typography, Button, CircularProgress } from "@mui/material";
import PlayArrowIcon from "@mui/icons-material/PlayArrow";

import KPICards from "../components/KPICards";
import AlertsPanel from "../components/AlertsPanel";
import IncidentTable from "../components/IncidentTable";
import { IncidentTrendChart, DelaysByRegionChart, SeverityPieChart } from "../components/Charts";
import {
  fetchKPIs, fetchIncidents, fetchAlerts, fetchIncidentTrend,
  fetchDelaysByRegion, runDetection, acknowledgeAlert, generateAISummary,
} from "../services/api";

export default function Dashboard() {
  const [kpis, setKpis] = useState(null);
  const [incidents, setIncidents] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [trend, setTrend] = useState([]);
  const [delays, setDelays] = useState([]);
  const [loading, setLoading] = useState(true);

  const loadAll = async () => {
    setLoading(true);
    try {
      const [kRes, iRes, aRes, tRes, dRes] = await Promise.all([
        fetchKPIs(),
        fetchIncidents({ limit: 20 }),
        fetchAlerts({ limit: 30 }),
        fetchIncidentTrend(30),
        fetchDelaysByRegion(),
      ]);
      setKpis(kRes.data);
      setIncidents(iRes.data);
      setAlerts(aRes.data);
      setTrend(tRes.data);
      setDelays(dRes.data);
    } catch (err) {
      console.error("Failed to load dashboard data:", err);
    }
    setLoading(false);
  };

  useEffect(() => { loadAll(); }, []);

  const handleRunDetection = async () => {
    await runDetection();
    loadAll();
  };

  const handleAcknowledge = async (alertId) => {
    await acknowledgeAlert(alertId);
    loadAll();
  };

  const handleAISummary = async (incidentId) => {
    await generateAISummary(incidentId);
    loadAll();
  };

  if (loading) {
    return (
      <Box sx={{ display: "flex", justifyContent: "center", py: 10 }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center", mb: 3 }}>
        <Typography variant="h5" sx={{ fontWeight: 700 }}>
          Operational Overview
        </Typography>
        <Button variant="contained" startIcon={<PlayArrowIcon />} onClick={handleRunDetection}>
          Run Anomaly Scan
        </Button>
      </Box>

      <KPICards kpis={kpis} />

      <Grid container spacing={2} sx={{ mt: 2 }}>
        <Grid size={{ xs: 12, md: 8 }}>
          <IncidentTrendChart data={trend} />
        </Grid>
        <Grid size={{ xs: 12, md: 4 }}>
          <SeverityPieChart incidents={incidents} />
        </Grid>
      </Grid>

      <Grid container spacing={2} sx={{ mt: 1 }}>
        <Grid size={{ xs: 12, md: 7 }}>
          <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 1 }}>
            Recent Incidents
          </Typography>
          <IncidentTable incidents={incidents} onGenerateSummary={handleAISummary} />
        </Grid>
        <Grid size={{ xs: 12, md: 5 }}>
          <Box sx={{ mb: 2 }}>
            <AlertsPanel alerts={alerts} onAcknowledge={handleAcknowledge} />
          </Box>
          <DelaysByRegionChart data={delays} />
        </Grid>
      </Grid>
    </Box>
  );
}
