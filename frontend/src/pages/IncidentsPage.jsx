import { useState, useEffect } from "react";
import {
  Box, Typography, TextField, MenuItem, Grid, Paper, Button, Dialog,
  DialogTitle, DialogContent, DialogActions, Chip,
} from "@mui/material";

import IncidentTable from "../components/IncidentTable";
import { fetchIncidents, createIncident, updateIncident, generateAISummary, fetchIncident } from "../services/api";

export default function IncidentsPage() {
  const [incidents, setIncidents] = useState([]);
  const [statusFilter, setStatusFilter] = useState("");
  const [severityFilter, setSeverityFilter] = useState("");
  const [detailOpen, setDetailOpen] = useState(false);
  const [selectedIncident, setSelectedIncident] = useState(null);
  const [createOpen, setCreateOpen] = useState(false);
  const [newIncident, setNewIncident] = useState({
    title: "", incident_type: "shipment_delay", severity: "medium", description: "", assigned_team: "",
  });

  const load = async () => {
    const params = {};
    if (statusFilter) params.status = statusFilter;
    if (severityFilter) params.severity = severityFilter;
    const res = await fetchIncidents(params);
    setIncidents(res.data);
  };

  useEffect(() => { load(); }, [statusFilter, severityFilter]);

  const handleCreate = async () => {
    await createIncident(newIncident);
    setCreateOpen(false);
    setNewIncident({ title: "", incident_type: "shipment_delay", severity: "medium", description: "", assigned_team: "" });
    load();
  };

  const handleAISummary = async (id) => {
    await generateAISummary(id);
    const res = await fetchIncident(id);
    setSelectedIncident(res.data);
    setDetailOpen(true);
  };

  return (
    <Box>
      <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center", mb: 2 }}>
        <Typography variant="h5" sx={{ fontWeight: 700 }}>Incident Management</Typography>
        <Button variant="contained" onClick={() => setCreateOpen(true)}>Create Incident</Button>
      </Box>

      <Grid container spacing={2} sx={{ mb: 2 }}>
        <Grid size={{ xs: 6, sm: 3 }}>
          <TextField select fullWidth size="small" label="Status" value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}>
            <MenuItem value="">All</MenuItem>
            <MenuItem value="open">Open</MenuItem>
            <MenuItem value="investigating">Investigating</MenuItem>
            <MenuItem value="resolved">Resolved</MenuItem>
            <MenuItem value="closed">Closed</MenuItem>
          </TextField>
        </Grid>
        <Grid size={{ xs: 6, sm: 3 }}>
          <TextField select fullWidth size="small" label="Severity" value={severityFilter}
            onChange={(e) => setSeverityFilter(e.target.value)}>
            <MenuItem value="">All</MenuItem>
            <MenuItem value="critical">Critical</MenuItem>
            <MenuItem value="high">High</MenuItem>
            <MenuItem value="medium">Medium</MenuItem>
            <MenuItem value="low">Low</MenuItem>
          </TextField>
        </Grid>
      </Grid>

      <IncidentTable incidents={incidents} onGenerateSummary={handleAISummary} />

      {/* Create Incident Dialog */}
      <Dialog open={createOpen} onClose={() => setCreateOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Create Incident</DialogTitle>
        <DialogContent sx={{ display: "flex", flexDirection: "column", gap: 2, pt: 2 }}>
          <TextField label="Title" fullWidth value={newIncident.title}
            onChange={(e) => setNewIncident({ ...newIncident, title: e.target.value })} />
          <TextField select label="Type" fullWidth value={newIncident.incident_type}
            onChange={(e) => setNewIncident({ ...newIncident, incident_type: e.target.value })}>
            <MenuItem value="shipment_delay">Shipment Delay</MenuItem>
            <MenuItem value="system_outage">System Outage</MenuItem>
            <MenuItem value="sla_breach">SLA Breach</MenuItem>
            <MenuItem value="data_quality">Data Quality</MenuItem>
          </TextField>
          <TextField select label="Severity" fullWidth value={newIncident.severity}
            onChange={(e) => setNewIncident({ ...newIncident, severity: e.target.value })}>
            <MenuItem value="low">Low</MenuItem>
            <MenuItem value="medium">Medium</MenuItem>
            <MenuItem value="high">High</MenuItem>
            <MenuItem value="critical">Critical</MenuItem>
          </TextField>
          <TextField label="Description" fullWidth multiline rows={3} value={newIncident.description}
            onChange={(e) => setNewIncident({ ...newIncident, description: e.target.value })} />
          <TextField label="Assigned Team" fullWidth value={newIncident.assigned_team}
            onChange={(e) => setNewIncident({ ...newIncident, assigned_team: e.target.value })} />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setCreateOpen(false)}>Cancel</Button>
          <Button variant="contained" onClick={handleCreate} disabled={!newIncident.title}>Create</Button>
        </DialogActions>
      </Dialog>

      {/* Incident Detail Dialog */}
      <Dialog open={detailOpen} onClose={() => setDetailOpen(false)} maxWidth="md" fullWidth>
        <DialogTitle>
          Incident #{selectedIncident?.id}: {selectedIncident?.title}
        </DialogTitle>
        <DialogContent>
          {selectedIncident && (
            <Box sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
              <Box sx={{ display: "flex", gap: 1 }}>
                <Chip label={selectedIncident.severity} color={selectedIncident.severity === "critical" ? "error" : "warning"} />
                <Chip label={selectedIncident.status} variant="outlined" />
                <Chip label={selectedIncident.incident_type} variant="outlined" />
              </Box>
              <Typography variant="body2">{selectedIncident.description}</Typography>
              {selectedIncident.ai_summary && (
                <Paper sx={{ p: 2, bgcolor: "rgba(96,165,250,0.08)", border: "1px solid rgba(96,165,250,0.2)" }}>
                  <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 1 }}>AI Analysis</Typography>
                  <Typography variant="body2" sx={{ whiteSpace: "pre-wrap" }}>
                    {selectedIncident.ai_summary}
                  </Typography>
                </Paper>
              )}
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDetailOpen(false)}>Close</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
