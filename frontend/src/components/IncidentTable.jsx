import {
  Table, TableBody, TableCell, TableContainer, TableHead, TableRow,
  Paper, Chip, IconButton, Tooltip,
} from "@mui/material";
import AutoFixHighIcon from "@mui/icons-material/AutoFixHigh";

const SEVERITY_COLORS = {
  critical: "error",
  high: "warning",
  medium: "info",
  low: "default",
};

const STATUS_COLORS = {
  open: "error",
  investigating: "warning",
  resolved: "success",
  closed: "default",
};

export default function IncidentTable({ incidents, onGenerateSummary }) {
  if (!incidents?.length) {
    return <Paper sx={{ p: 3, textAlign: "center" }}>No incidents found</Paper>;
  }

  return (
    <TableContainer component={Paper} sx={{ maxHeight: 500 }}>
      <Table stickyHeader size="small">
        <TableHead>
          <TableRow>
            <TableCell>ID</TableCell>
            <TableCell>Title</TableCell>
            <TableCell>Type</TableCell>
            <TableCell>Severity</TableCell>
            <TableCell>Status</TableCell>
            <TableCell>Team</TableCell>
            <TableCell>Created</TableCell>
            <TableCell>AI</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {incidents.map((inc) => (
            <TableRow key={inc.id} hover>
              <TableCell>#{inc.id}</TableCell>
              <TableCell sx={{ maxWidth: 260, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                {inc.title}
              </TableCell>
              <TableCell>{inc.incident_type}</TableCell>
              <TableCell>
                <Chip label={inc.severity} color={SEVERITY_COLORS[inc.severity] || "default"} size="small" />
              </TableCell>
              <TableCell>
                <Chip label={inc.status} color={STATUS_COLORS[inc.status] || "default"} size="small" variant="outlined" />
              </TableCell>
              <TableCell>{inc.assigned_team || "—"}</TableCell>
              <TableCell>{new Date(inc.created_at).toLocaleDateString()}</TableCell>
              <TableCell>
                {onGenerateSummary && (
                  <Tooltip title="Generate AI Summary">
                    <IconButton size="small" onClick={() => onGenerateSummary(inc.id)}>
                      <AutoFixHighIcon fontSize="small" />
                    </IconButton>
                  </Tooltip>
                )}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}
