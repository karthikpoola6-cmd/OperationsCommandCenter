-- ============================================================
-- Operations Command Center — Seed Data
-- Simulates a supply chain / IT operations environment
-- ============================================================

-- Shipments (mix of on-time, delayed, in-transit)
INSERT INTO shipments (order_id, origin, destination, carrier, status, priority, expected_delivery, actual_delivery, created_at) VALUES
('ORD-1001', 'Dallas, TX',     'Los Angeles, CA',  'FedEx',       'delivered', 'high',     '2026-03-15 14:00:00', '2026-03-15 12:30:00', '2026-03-12 08:00:00'),
('ORD-1002', 'Houston, TX',    'Chicago, IL',      'UPS',         'delivered', 'normal',   '2026-03-16 10:00:00', '2026-03-17 16:00:00', '2026-03-13 09:00:00'),
('ORD-1003', 'Austin, TX',     'New York, NY',     'DHL',         'delayed',   'high',     '2026-03-14 08:00:00', NULL,                  '2026-03-11 07:00:00'),
('ORD-1004', 'San Antonio, TX','Miami, FL',        'FedEx',       'in_transit','normal',   '2026-03-25 12:00:00', NULL,                  '2026-03-20 10:00:00'),
('ORD-1005', 'Dallas, TX',     'Seattle, WA',      'USPS',        'delayed',   'critical', '2026-03-13 06:00:00', NULL,                  '2026-03-10 06:00:00'),
('ORD-1006', 'El Paso, TX',    'Denver, CO',       'UPS',         'delivered', 'normal',   '2026-03-18 15:00:00', '2026-03-18 13:00:00', '2026-03-15 11:00:00'),
('ORD-1007', 'Houston, TX',    'Atlanta, GA',      'FedEx',       'in_transit','high',     '2026-03-24 09:00:00', NULL,                  '2026-03-21 08:00:00'),
('ORD-1008', 'Dallas, TX',     'Phoenix, AZ',      'DHL',         'delayed',   'normal',   '2026-03-17 10:00:00', NULL,                  '2026-03-14 09:00:00'),
('ORD-1009', 'Austin, TX',     'Portland, OR',     'UPS',         'pending',   'normal',   '2026-03-26 14:00:00', NULL,                  '2026-03-22 07:00:00'),
('ORD-1010', 'Houston, TX',    'Boston, MA',       'FedEx',       'delivered', 'high',     '2026-03-19 11:00:00', '2026-03-19 09:00:00', '2026-03-16 10:00:00'),
('ORD-1011', 'Dallas, TX',     'Minneapolis, MN',  'USPS',        'in_transit','normal',   '2026-03-25 08:00:00', NULL,                  '2026-03-22 06:00:00'),
('ORD-1012', 'San Antonio, TX','Detroit, MI',      'UPS',         'delayed',   'high',     '2026-03-16 07:00:00', NULL,                  '2026-03-13 05:00:00'),
('ORD-1013', 'Austin, TX',     'Charlotte, NC',    'FedEx',       'delivered', 'normal',   '2026-03-20 16:00:00', '2026-03-20 14:00:00', '2026-03-17 12:00:00'),
('ORD-1014', 'Houston, TX',    'Las Vegas, NV',    'DHL',         'in_transit','critical', '2026-03-24 18:00:00', NULL,                  '2026-03-21 15:00:00'),
('ORD-1015', 'El Paso, TX',    'Salt Lake City, UT','UPS',        'pending',   'normal',   '2026-03-27 10:00:00', NULL,                  '2026-03-23 08:00:00');

-- Incidents
INSERT INTO incidents (title, incident_type, description, severity, status, assigned_team, shipment_id, created_at, resolved_at) VALUES
('Shipment Delay: Order ORD-1003',    'shipment_delay', 'Shipment from Austin to New York is 9+ days overdue. Carrier DHL reports customs hold.', 'critical', 'investigating', 'Logistics Operations', 3,  '2026-03-15 10:00:00', NULL),
('Shipment Delay: Order ORD-1005',    'shipment_delay', 'Critical priority shipment to Seattle delayed 10+ days. Weather disruption reported.', 'critical', 'open',          'Logistics Operations', 5,  '2026-03-14 08:00:00', NULL),
('Shipment Delay: Order ORD-1008',    'shipment_delay', 'Shipment to Phoenix delayed 6+ days. Carrier DHL backlog in regional hub.', 'high',     'open',          'Logistics Operations', 8,  '2026-03-18 11:00:00', NULL),
('Shipment Delay: Order ORD-1012',    'shipment_delay', 'High priority shipment to Detroit delayed 7+ days. UPS reports vehicle breakdown.', 'high', 'investigating', 'Logistics Operations', 12, '2026-03-17 09:00:00', NULL),
('Warehouse System Outage',           'system_outage',  'Dallas warehouse management system unresponsive. Affecting order processing.', 'critical', 'investigating', 'IT Operations',        NULL, '2026-03-22 03:00:00', NULL),
('Late Delivery: Order ORD-1002',     'shipment_delay', 'Shipment to Chicago delivered 30 hours late. Customer complaint received.', 'medium',  'resolved',      'Customer Service',     2,  '2026-03-17 18:00:00', '2026-03-18 10:00:00'),
('Power BI Dashboard Loading Failure','system_outage',  'Operations dashboard failing to load for Southwest region. Data refresh stalled.', 'medium', 'resolved', 'IT Operations', NULL, '2026-03-20 14:00:00', '2026-03-20 16:30:00'),
('Carrier API Integration Error',     'system_outage',  'FedEx tracking API returning 503 errors intermittently since 06:00.', 'high',    'open',          'Engineering',          NULL, '2026-03-23 06:00:00', NULL),
('SLA Breach: Multiple Southwest Shipments', 'sla_breach', 'Three shipments in Southwest corridor exceeded 48-hour SLA window.', 'critical', 'open', 'Logistics Operations', NULL, '2026-03-21 12:00:00', NULL),
('Inventory Mismatch Alert',          'data_quality',   'Physical inventory count for Dallas warehouse differs from system by 12%.', 'high', 'investigating', 'Warehouse Operations', NULL, '2026-03-22 09:00:00', NULL);

-- Alerts
INSERT INTO alerts (alert_type, message, severity, incident_id, acknowledged, created_at) VALUES
('shipment_delay', 'Shipment delay detected: Order #ORD-1003 — Expected delivery exceeded by 216+ hours', 'critical', 1, 0, '2026-03-15 10:00:00'),
('shipment_delay', 'CRITICAL: Order #ORD-1005 to Seattle — 240+ hours overdue, priority: critical', 'critical', 2, 0, '2026-03-14 08:00:00'),
('shipment_delay', 'Shipment delay detected: Order #ORD-1008 — Expected delivery exceeded by 144+ hours', 'high', 3, 0, '2026-03-18 11:00:00'),
('shipment_delay', 'Shipment delay detected: Order #ORD-1012 — Expected delivery exceeded by 168+ hours', 'high', 4, 1, '2026-03-17 09:00:00'),
('system_outage',  'CRITICAL: Dallas warehouse system unresponsive — order processing halted', 'critical', 5, 0, '2026-03-22 03:00:00'),
('sla_breach',     'SLA Breach: Incident #2 open for 216+ hours (target: 24h)', 'critical', 2, 0, '2026-03-23 08:00:00'),
('sla_breach',     'SLA Breach: Incident #1 open for 192+ hours (target: 24h)', 'critical', 1, 0, '2026-03-23 08:00:00'),
('system_outage',  'FedEx API integration error — tracking data unavailable', 'high', 8, 0, '2026-03-23 06:00:00'),
('data_quality',   'Inventory mismatch: Dallas warehouse — 12% variance detected', 'high', 10, 0, '2026-03-22 09:00:00'),
('shipment_delay', 'Late delivery confirmed: Order #ORD-1002 — 30h late, customer complaint filed', 'medium', 6, 1, '2026-03-17 18:00:00'),
('system_outage',  'Power BI dashboard refresh stalled — Southwest region data unavailable', 'medium', 7, 1, '2026-03-20 14:00:00'),
('sla_breach',     'SLA Breach: Incident #9 — Southwest corridor shipments exceed 48h window', 'critical', 9, 0, '2026-03-21 12:00:00');

-- Operations Metrics (time-series KPI data)
INSERT INTO operations_metrics (metric_name, metric_value, unit, region, recorded_at) VALUES
('on_time_delivery_rate',  78.5,  'percent', 'Southwest', '2026-03-23 00:00:00'),
('on_time_delivery_rate',  91.2,  'percent', 'Northeast', '2026-03-23 00:00:00'),
('on_time_delivery_rate',  85.0,  'percent', 'Midwest',   '2026-03-23 00:00:00'),
('on_time_delivery_rate',  82.3,  'percent', 'Southeast', '2026-03-23 00:00:00'),
('on_time_delivery_rate',  88.7,  'percent', 'West',      '2026-03-23 00:00:00'),
('avg_resolution_time',    18.5,  'hours',   'Southwest', '2026-03-23 00:00:00'),
('avg_resolution_time',    8.2,   'hours',   'Northeast', '2026-03-23 00:00:00'),
('avg_resolution_time',    12.0,  'hours',   'Midwest',   '2026-03-23 00:00:00'),
('avg_resolution_time',    14.3,  'hours',   'Southeast', '2026-03-23 00:00:00'),
('avg_resolution_time',    10.1,  'hours',   'West',      '2026-03-23 00:00:00'),
('active_incidents',       5.0,   'count',   'All',       '2026-03-23 00:00:00'),
('shipment_volume',        342.0, 'count',   'Southwest', '2026-03-23 00:00:00'),
('shipment_volume',        287.0, 'count',   'Northeast', '2026-03-23 00:00:00'),
('shipment_volume',        195.0, 'count',   'Midwest',   '2026-03-23 00:00:00'),
('shipment_volume',        228.0, 'count',   'Southeast', '2026-03-23 00:00:00'),
('shipment_volume',        310.0, 'count',   'West',      '2026-03-23 00:00:00'),
('customer_complaints',    7.0,   'count',   'All',       '2026-03-23 00:00:00'),
('on_time_delivery_rate',  80.1,  'percent', 'Southwest', '2026-03-22 00:00:00'),
('on_time_delivery_rate',  89.8,  'percent', 'Northeast', '2026-03-22 00:00:00'),
('on_time_delivery_rate',  83.5,  'percent', 'Midwest',   '2026-03-22 00:00:00'),
('avg_resolution_time',    20.1,  'hours',   'Southwest', '2026-03-22 00:00:00'),
('avg_resolution_time',    9.5,   'hours',   'Northeast', '2026-03-22 00:00:00'),
('active_incidents',       7.0,   'count',   'All',       '2026-03-22 00:00:00'),
('on_time_delivery_rate',  76.3,  'percent', 'Southwest', '2026-03-21 00:00:00'),
('on_time_delivery_rate',  90.5,  'percent', 'Northeast', '2026-03-21 00:00:00'),
('avg_resolution_time',    22.4,  'hours',   'Southwest', '2026-03-21 00:00:00'),
('active_incidents',       8.0,   'count',   'All',       '2026-03-21 00:00:00'),
('on_time_delivery_rate',  74.8,  'percent', 'Southwest', '2026-03-20 00:00:00'),
('on_time_delivery_rate',  88.0,  'percent', 'Northeast', '2026-03-20 00:00:00'),
('active_incidents',       6.0,   'count',   'All',       '2026-03-20 00:00:00');
