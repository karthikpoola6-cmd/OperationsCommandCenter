import { useState, useEffect } from "react";
import {
  Box, Typography, TextField, MenuItem, Grid,
  Table, TableBody, TableCell, TableContainer, TableHead, TableRow,
  Paper, Chip,
} from "@mui/material";

import { fetchShipments } from "../services/api";

const STATUS_COLORS = {
  delivered: "success",
  in_transit: "info",
  delayed: "error",
  pending: "default",
  failed: "error",
};

export default function ShipmentsPage() {
  const [shipments, setShipments] = useState([]);
  const [statusFilter, setStatusFilter] = useState("");

  const load = async () => {
    const params = {};
    if (statusFilter) params.status = statusFilter;
    const res = await fetchShipments(params);
    setShipments(res.data);
  };

  useEffect(() => { load(); }, [statusFilter]);

  return (
    <Box>
      <Typography variant="h5" sx={{ fontWeight: 700, mb: 2 }}>Shipment Tracking</Typography>

      <Grid container spacing={2} sx={{ mb: 2 }}>
        <Grid size={{ xs: 6, sm: 3 }}>
          <TextField select fullWidth size="small" label="Status" value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}>
            <MenuItem value="">All</MenuItem>
            <MenuItem value="pending">Pending</MenuItem>
            <MenuItem value="in_transit">In Transit</MenuItem>
            <MenuItem value="delayed">Delayed</MenuItem>
            <MenuItem value="delivered">Delivered</MenuItem>
            <MenuItem value="failed">Failed</MenuItem>
          </TextField>
        </Grid>
      </Grid>

      <TableContainer component={Paper} sx={{ maxHeight: 600 }}>
        <Table stickyHeader size="small">
          <TableHead>
            <TableRow>
              <TableCell>Order ID</TableCell>
              <TableCell>Origin</TableCell>
              <TableCell>Destination</TableCell>
              <TableCell>Carrier</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Priority</TableCell>
              <TableCell>Expected</TableCell>
              <TableCell>Actual</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {shipments.map((s) => (
              <TableRow key={s.id} hover>
                <TableCell sx={{ fontWeight: 600 }}>{s.order_id}</TableCell>
                <TableCell>{s.origin}</TableCell>
                <TableCell>{s.destination}</TableCell>
                <TableCell>{s.carrier || "—"}</TableCell>
                <TableCell>
                  <Chip label={s.status} color={STATUS_COLORS[s.status] || "default"} size="small" />
                </TableCell>
                <TableCell>
                  <Chip
                    label={s.priority}
                    size="small"
                    variant="outlined"
                    color={s.priority === "critical" ? "error" : s.priority === "high" ? "warning" : "default"}
                  />
                </TableCell>
                <TableCell>{new Date(s.expected_delivery).toLocaleDateString()}</TableCell>
                <TableCell>{s.actual_delivery ? new Date(s.actual_delivery).toLocaleDateString() : "—"}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
}
