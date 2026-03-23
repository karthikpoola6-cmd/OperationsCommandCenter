import { useState } from "react";
import { Box, AppBar, Toolbar, Typography, Tabs, Tab, Container } from "@mui/material";
import DashboardIcon from "@mui/icons-material/Dashboard";
import WarningAmberIcon from "@mui/icons-material/WarningAmber";
import LocalShippingIcon from "@mui/icons-material/LocalShipping";
import NotificationsIcon from "@mui/icons-material/Notifications";

import Dashboard from "./pages/Dashboard";
import IncidentsPage from "./pages/IncidentsPage";
import ShipmentsPage from "./pages/ShipmentsPage";
import AlertsPage from "./pages/AlertsPage";

const TABS = [
  { label: "Dashboard", icon: <DashboardIcon /> },
  { label: "Incidents", icon: <WarningAmberIcon /> },
  { label: "Shipments", icon: <LocalShippingIcon /> },
  { label: "Alerts", icon: <NotificationsIcon /> },
];

export default function App() {
  const [tab, setTab] = useState(0);

  return (
    <Box sx={{ minHeight: "100vh" }}>
      <AppBar position="static" color="transparent" elevation={0}
        sx={{ borderBottom: "1px solid rgba(255,255,255,0.08)" }}>
        <Toolbar>
          <Typography variant="h6" sx={{ fontWeight: 700, flexGrow: 1, letterSpacing: -0.5 }}>
            Operations Command Center
          </Typography>
          <Tabs value={tab} onChange={(_, v) => setTab(v)} textColor="primary" indicatorColor="primary">
            {TABS.map((t) => (
              <Tab key={t.label} label={t.label} icon={t.icon} iconPosition="start"
                sx={{ textTransform: "none", minHeight: 48 }} />
            ))}
          </Tabs>
        </Toolbar>
      </AppBar>

      <Container maxWidth="xl" sx={{ py: 3 }}>
        {tab === 0 && <Dashboard />}
        {tab === 1 && <IncidentsPage />}
        {tab === 2 && <ShipmentsPage />}
        {tab === 3 && <AlertsPage />}
      </Container>
    </Box>
  );
}
