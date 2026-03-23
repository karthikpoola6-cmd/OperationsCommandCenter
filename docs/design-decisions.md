# Design Decisions

**Why FastAPI?**
Python works well for data processing and has good support for async operations. FastAPI also generates API docs automatically at `/docs`.

**Why Power BI alongside React?**
The React dashboard handles real-time interaction (creating incidents, acknowledging alerts). Power BI handles the analytics side — DAX measures, slicers, and the kind of executive-level reporting that operations managers expect.

**Why simulated data?**
Real client data can't be shared publicly. The sample data uses realistic patterns — multiple carriers, varying delay lengths, different severity levels, regional metrics — so the dashboards and detection logic behave the same way they would with production data.

**Why rule-based AI fallback?**
The system should work without an API key. The fallback generates structured root-cause analysis based on incident type, so the feature is usable even without Claude API access.

**Why dark theme?**
Operations centers and NOCs use dark interfaces to reduce eye strain during long monitoring shifts.
