import { Card, CardContent, Typography, Grid, Box } from "@mui/material";
import ErrorIcon from "@mui/icons-material/Error";
import WarningIcon from "@mui/icons-material/Warning";
import LocalShippingIcon from "@mui/icons-material/LocalShipping";
import NotificationsActiveIcon from "@mui/icons-material/NotificationsActive";
import AccessTimeIcon from "@mui/icons-material/AccessTime";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";

const CARDS = [
  { key: "open_incidents", label: "Open Incidents", icon: ErrorIcon, color: "#ef4444" },
  { key: "critical_incidents", label: "Critical", icon: WarningIcon, color: "#f59e0b" },
  { key: "active_alerts", label: "Active Alerts", icon: NotificationsActiveIcon, color: "#f472b6" },
  { key: "delayed_shipments", label: "Delayed Shipments", icon: LocalShippingIcon, color: "#fb923c" },
  { key: "avg_resolution_hours", label: "Avg Resolution (hrs)", icon: AccessTimeIcon, color: "#60a5fa" },
  { key: "sla_compliance_pct", label: "SLA Compliance", icon: CheckCircleIcon, color: "#22c55e", suffix: "%" },
];

export default function KPICards({ kpis }) {
  if (!kpis) return null;

  return (
    <Grid container spacing={2}>
      {CARDS.map(({ key, label, icon: Icon, color, suffix }) => (
        <Grid size={{ xs: 6, sm: 4, md: 2 }} key={key}>
          <Card sx={{ bgcolor: "background.paper", border: `1px solid ${color}22` }}>
            <CardContent sx={{ textAlign: "center", py: 2 }}>
              <Icon sx={{ fontSize: 28, color, mb: 0.5 }} />
              <Typography variant="h4" sx={{ fontWeight: 700, color }}>
                {kpis[key] != null ? `${kpis[key]}${suffix || ""}` : "—"}
              </Typography>
              <Typography variant="caption" color="text.secondary">
                {label}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      ))}
    </Grid>
  );
}
