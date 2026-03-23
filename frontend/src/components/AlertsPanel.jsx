import {
  List, ListItem, ListItemText, ListItemIcon, Chip, IconButton, Paper, Typography, Box,
} from "@mui/material";
import NotificationsIcon from "@mui/icons-material/Notifications";
import CheckIcon from "@mui/icons-material/Check";

const SEVERITY_COLORS = {
  critical: "error",
  high: "warning",
  medium: "info",
  low: "default",
};

export default function AlertsPanel({ alerts, onAcknowledge }) {
  const unacked = alerts?.filter((a) => !a.acknowledged) || [];

  return (
    <Paper sx={{ p: 2, maxHeight: 400, overflow: "auto" }}>
      <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 1 }}>
        Active Alerts ({unacked.length})
      </Typography>
      {unacked.length === 0 ? (
        <Typography variant="body2" color="text.secondary">
          No active alerts
        </Typography>
      ) : (
        <List dense>
          {unacked.map((alert) => (
            <ListItem
              key={alert.id}
              secondaryAction={
                onAcknowledge && (
                  <IconButton edge="end" size="small" onClick={() => onAcknowledge(alert.id)}>
                    <CheckIcon fontSize="small" />
                  </IconButton>
                )
              }
              sx={{ borderLeft: 3, borderColor: alert.severity === "critical" ? "error.main" : "warning.main", mb: 0.5, borderRadius: 1, bgcolor: "rgba(255,255,255,0.02)" }}
            >
              <ListItemIcon sx={{ minWidth: 36 }}>
                <NotificationsIcon fontSize="small" color={SEVERITY_COLORS[alert.severity] || "inherit"} />
              </ListItemIcon>
              <ListItemText
                primary={alert.message}
                secondary={new Date(alert.created_at).toLocaleString()}
                primaryTypographyProps={{ variant: "body2" }}
              />
              <Chip label={alert.severity} color={SEVERITY_COLORS[alert.severity]} size="small" sx={{ ml: 1 }} />
            </ListItem>
          ))}
        </List>
      )}
    </Paper>
  );
}
