import { useState, useEffect } from "react";
import {
  Box, Typography, ToggleButton, ToggleButtonGroup,
  Table, TableBody, TableCell, TableContainer, TableHead, TableRow,
  Paper, Chip, IconButton, Tooltip,
} from "@mui/material";
import CheckIcon from "@mui/icons-material/Check";

import { fetchAlerts, acknowledgeAlert } from "../services/api";

const SEVERITY_COLORS = {
  critical: "error",
  high: "warning",
  medium: "info",
  low: "default",
};

export default function AlertsPage() {
  const [alerts, setAlerts] = useState([]);
  const [filter, setFilter] = useState("active");

  const load = async () => {
    const params = {};
    if (filter === "active") params.acknowledged = false;
    if (filter === "acknowledged") params.acknowledged = true;
    const res = await fetchAlerts(params);
    setAlerts(res.data);
  };

  useEffect(() => { load(); }, [filter]);

  const handleAcknowledge = async (id) => {
    await acknowledgeAlert(id);
    load();
  };

  return (
    <Box>
      <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center", mb: 2 }}>
        <Typography variant="h5" sx={{ fontWeight: 700 }}>Alerts</Typography>
        <ToggleButtonGroup size="small" value={filter} exclusive onChange={(_, v) => v && setFilter(v)}>
          <ToggleButton value="active">Active</ToggleButton>
          <ToggleButton value="acknowledged">Acknowledged</ToggleButton>
          <ToggleButton value="all">All</ToggleButton>
        </ToggleButtonGroup>
      </Box>

      <TableContainer component={Paper} sx={{ maxHeight: 600 }}>
        <Table stickyHeader size="small">
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Type</TableCell>
              <TableCell>Message</TableCell>
              <TableCell>Severity</TableCell>
              <TableCell>Incident</TableCell>
              <TableCell>Time</TableCell>
              <TableCell>Action</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {alerts.map((a) => (
              <TableRow key={a.id} hover sx={{ opacity: a.acknowledged ? 0.5 : 1 }}>
                <TableCell>#{a.id}</TableCell>
                <TableCell>{a.alert_type}</TableCell>
                <TableCell sx={{ maxWidth: 400, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                  {a.message}
                </TableCell>
                <TableCell>
                  <Chip label={a.severity} color={SEVERITY_COLORS[a.severity]} size="small" />
                </TableCell>
                <TableCell>{a.incident_id ? `#${a.incident_id}` : "—"}</TableCell>
                <TableCell>{new Date(a.created_at).toLocaleString()}</TableCell>
                <TableCell>
                  {!a.acknowledged && (
                    <Tooltip title="Acknowledge">
                      <IconButton size="small" color="success" onClick={() => handleAcknowledge(a.id)}>
                        <CheckIcon fontSize="small" />
                      </IconButton>
                    </Tooltip>
                  )}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
}
