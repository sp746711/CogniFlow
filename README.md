<div align="center">

<img src="frontend/public/cogniflow_banner.png" alt="CogniFlow Banner" width="100%" style="border-radius: 8px;" />

<br/><br/>

# ⚡ COGNIFLOW

### **Intelligent Workflow Telemetry & Developer Productivity Analytics**

*Transforming raw developer activity streams into deep flow insights, interruption diagnostics, and team friction analysis.*

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.3-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-5.4-646CFF?style=for-the-badge&logo=vite&logoColor=white)](https://vitejs.dev/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supported-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![SQLite](https://img.shields.io/badge/SQLite-Auto--Fallback-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Pytest](https://img.shields.io/badge/Tests-33%20Passed-brightgreen?style=for-the-badge&logo=pytest&logoColor=white)](https://docs.pytest.org/)

---

</div>

## 📌 Executive Overview

Modern engineering organizations generate vast quantities of activity data across IDEs, communication tools, issue trackers, and code repositories. However, raw activity metrics—such as commit counts or ticket velocity—fail to capture the true driver of engineering excellence: **uninterrupted cognitive flow**. Frequent context-switching, uncoordinated messaging, and micro-interruptions silently degrade developer focus, extend recovery times, and introduce burnout across engineering teams.

**CogniFlow** is an enterprise-grade telemetry and analytics platform designed to monitor, model, and optimize developer flow states. By capturing multi-channel activity events across **IDEs**, **Slack**, **Jira**, and **GitHub**, CogniFlow processes raw temporal events into structured metrics: **Focus Time**, **Flow Sessions**, **Interruption Frequency**, **Context-Switching Drag**, and **Recovery Delay**.

At the core of CogniFlow is a sophisticated analytical pipeline that correlates event boundaries to calculate a proprietary **Flow Score (0–100)**. The platform features both a high-throughput **FastAPI backend** (with dual PostgreSQL/SQLite persistence and Alembic migrations) and a modern **React 18 / Vite 5 dashboard** (equipped with Recharts analytics, Framer Motion transitions, and interactive telemetry simulation controls).

---

## ✨ Key Capabilities

CogniFlow provides comprehensive visibility into individual and team-level engineering dynamics through five unified pillars:

### 📊 1. Workflow & Flow Intelligence
* **Flow Session Detection**: Identifies sustained focus windows based on IDE activity thresholds and event continuity.
* **Focus Time Quantification**: Accurately tracks accumulated deep work hours versus fragmented work periods.
* **Interruption Diagnostics**: Classifies incoming disruptions from communication platforms (e.g., direct messages, channel noise) and measures their direct impact on active coding sessions.
* **Context-Switching Analytics**: Measures rapid transitions between disparate tasks, projects, or application contexts to identify focus fragmentation.
* **Recovery Time Modeling**: Calculates the precise delay required for a developer to regain deep concentration after a disruption.
* **Proprietary Flow Score**: Computes an aggregate productivity health score (0–100) dynamically tailored to work patterns.

### 👥 2. Developer & Team Telemetry
* **Developer Profiles**: Detailed individual metrics highlighting focus ratio, interruption vulnerability, and active working hours.
* **Team Aggregation**: Group-level productivity dynamics, comparative team benchmarks, and workload distribution metrics.
* **Live Activity Feed**: Real-time streaming feed of multi-source developer events across tools.
* **Comparative Insights**: Identifies systemic team friction points, such as meeting-heavy time windows or high-interrupt channels.

### 📈 3. Visual Reporting & Interactive Dashboard
* **Executive Summary Dashboard**: High-level KPIs, focus trends, and top friction indicators for engineering leaders.
* **17 Specialized UI Views**: Dedicated routes for Live Monitoring, Flow Analytics, Interruptions, Context Switching, Recovery Times, Developer Summaries, Team Benchmarks, and Daily Reports.
* **Chronological Event Timeline**: Granular filterable event logs with source tags (IDE, Slack, Jira, GitHub).
* **Automated Daily Reports**: Digest snapshots summarizing total focused time, flow duration averages, and recovery overhead for any selected date.

### ⚡ 4. Simulation Engine & Pipeline Orchestrator
* **Multi-Source Event Simulator**: Built-in generator simulating real-world engineering workdays with realistic activity distributions.
* **EventProcessor Pipeline**: Automated backend ingestion pipeline that parses raw events, calculates session boundaries, and persists derived metrics to SQL storage.
* **Interactive Run Modal**: Execute on-demand simulation scenarios directly from the UI or via REST API.

### ⚙️ 5. Enterprise Infrastructure & Reliability
* **Dual Database Engine**: Seamless support for production-grade PostgreSQL (`postgresql+psycopg`) with automatic fallback to zero-config local SQLite (`cogniflow_dev.db`).
* **Alembic Database Migrations**: Version-controlled SQL schema management.
* **Automated Data Seeding**: Self-healing data initialization on server startup or via CLI command.
* **33-Test Suite**: Comprehensive unit and integration coverage with Pytest and HTTPX.

---

## 🏗️ System Architecture

CogniFlow is architected with a strict separation between the data ingestion/analytics backend and the interactive visual client.

```mermaid
flowchart TB
    subgraph UI_Layer["Frontend — React 18 + Vite 5"]
        UI["Dashboard & Pages UI"]
        CHARTS["Recharts Visualizations"]
        CLIENT["Axios API Client"]
        ROUTER["React Router DOM (17 Routes)"]
        
        UI --> ROUTER
        ROUTER --> CHARTS
        ROUTER --> CLIENT
    end

    subgraph API_Layer["Backend — FastAPI App"]
        REST["REST API Controllers"]
        DEPS["Dependency Injection (get_db)"]
        
        REST --> DEPS
    end

    subgraph Engine_Layer["Analytics & Simulation Pipeline"]
        SIM["SimulationRunner"]
        PROC["EventProcessor Pipeline"]
        
        subgraph Analyzers["Analytics Service Layer"]
            FA["FlowAnalyzer"]
            IA["InterruptionAnalyzer"]
            CSA["ContextSwitchAnalyzer"]
            RA["RecoveryAnalyzer"]
            SC["ScoreCalculator"]
            DS["DashboardService"]
        end

        SIM --> PROC
        PROC --> Analyzers
    end

    subgraph DB_Layer["Persistence Layer"]
        ORM["SQLAlchemy 2.0 ORM"]
        MIG["Alembic Migrations"]
        PG[("PostgreSQL\n(Production)")]
        SQLITE[("SQLite Fallback\n(cogniflow_dev.db)")]

        ORM --> PG
        ORM --> SQLITE
        MIG --> ORM
    end

    CLIENT == "HTTP / JSON API (/api)" ==> REST
    REST --> Analyzers
    Analyzers --> ORM
```

### 🔄 Data Ingestion & Metric Derivation Flow

```mermaid
sequenceDiagram
    autonumber
    participant Sim as Activity Simulator
    participant DB as SQL Database
    participant Proc as EventProcessor
    participant Analyzers as Analytics Services
    participant API as FastAPI Endpoints
    participant UI as React Dashboard

    Sim->>DB: 1. Generate & Persist Raw Events (IDE, Slack, Jira, GitHub)
    Proc->>DB: 2. Query Raw Temporal Event Streams
    Proc->>Analyzers: 3. Pass Event Sequences to Analyzers
    Analyzers->>Analyzers: 4. Compute Flow Sessions, Interruptions, Switches, & Recovery
    Analyzers->>Analyzers: 5. Calculate Overall Flow Score (0-100)
    Analyzers->>DB: 6. Persist Derived Metrics & Aggregations
    UI->>API: 7. GET /api/dashboard & /api/flow
    API->>DB: 8. Read Persisted Analytics & Summaries
    API-->>UI: 9. JSON Response (Metrics, Trends, Timelines)
    UI-->>UI: 10. Render Interactive Recharts & KPI Cards
```

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Backend Framework** | [FastAPI](https://fastapi.tiangolo.com/) `0.115+` | High-performance asynchronous REST API framework |
| **Language** | [Python](https://www.python.org/) `3.11+` | Core analytics processing and simulation engine |
| **ORM & Database** | [SQLAlchemy](https://www.sqlalchemy.org/) `2.0+` | Unified database abstraction for PostgreSQL & SQLite |
| **DB Drivers** | [psycopg3](https://www.psycopg.org/psycopg3/) `3.2+` | Binary driver for production PostgreSQL connections |
| **Migrations** | [Alembic](https://alembic.sqlalchemy.org/) `1.13+` | Version-controlled database schema migrations |
| **Data Validation** | [Pydantic](https://docs.pydantic.dev/) `2.7+` | Strict request/response payload schemas |
| **Server** | [Uvicorn](https://www.uvicorn.org/) `0.30+` | ASGI web server for production and development |
| **Frontend Framework**| [React](https://react.dev/) `18.3` | Component-driven user interface |
| **Build Tool** | [Vite](https://vitejs.dev/) `5.4` | Next-generation frontend tooling & dev server |
| **Routing** | [React Router DOM](https://reactrouter.com/) `6.27` | Client-side page navigation (17 routes) |
| **Data Visualization**| [Recharts](https://recharts.org/) `2.13` | Interactive composable charts (Bar, Line, Area, Pie) |
| **Animations** | [Framer Motion](https://www.framer.com/motion/) `13.2` | Fluid micro-interactions and modal transitions |
| **Icons** | [Lucide React](https://lucide.dev/) `0.454` | Premium icon set for SaaS dashboards |
| **HTTP Client** | [Axios](https://axios-http.com/) `1.7` | Standardized API requesting with base URL config |
| **Orchestration** | [Concurrently](https://github.com/open-cli-tools/concurrently) `8.2` | Single-command concurrent startup for BE & FE |
| **Testing** | [Pytest](https://docs.pytest.org/) `8.0+` & `httpx` | Full backend unit and API integration testing (33 tests) |

---

## 🚀 Quick Start Guide

CogniFlow is designed for instant onboarding. You can launch both the FastAPI backend and React frontend concurrently with a single command.

### Prerequisites

Ensure you have the following installed on your machine:
* **Node.js**: v18.0.0 or higher
* **Python**: v3.11 or higher (`python3` / `python`)
* **Git**

---

### Option A: One-Command Startup (Recommended)

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/animesh6532/CogniFlow.git
   cd CogniFlow
   ```

2. **Install Node Dependencies & Start Application**:
   ```bash
   npm install
   npm run dev
   ```

   *This command will:*
   * Automatically spawn the **FastAPI Backend** at `http://127.0.0.1:8000`
   * Automatically spawn the **Vite React Frontend** at `http://127.0.0.1:5173`
   * Auto-initialize the local SQLite database (`cogniflow_dev.db`) and seed demo teams, developers, and tasks if PostgreSQL is not running.

---

### Option B: Step-by-Step Manual Setup

#### 1. Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv

# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment variables template
cp .env.example .env

# Run backend API server
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

#### 2. Frontend Setup

In a separate terminal window:

```bash
cd frontend

# Install npm packages
npm install

# Copy environment template
cp .env.example .env

# Launch Vite development server
npm run dev
```

Open your browser and navigate to **`http://127.0.0.1:5173`**.

---

## 🗄️ Database Configuration & Seeding

CogniFlow supports zero-friction dual-database architecture:

### 1. PostgreSQL (Production Setup)
To use PostgreSQL, set your connection string in `backend/.env`:
```env
DATABASE_URL=postgresql+psycopg://postgres:your_password@localhost:5432/cogniflow
```
Run Alembic schema migrations:
```bash
cd backend
alembic upgrade head
```

### 2. SQLite (Automatic Development Fallback)
If `DATABASE_URL` is omitted or PostgreSQL is unreachable, CogniFlow automatically connects to an embedded SQLite database (`backend/cogniflow_dev.db`).

### 3. Manual Database Seeding
You can manually re-seed the initial teams, developers, and Jira tasks at any time from the root directory:
```bash
npm run seed
```

---

## 📡 REST API Reference

The FastAPI backend exposes a comprehensive set of RESTful endpoints under the `/api` prefix. Interactive OpenAPI documentation is automatically available at `http://127.0.0.1:8000/docs`.

### System & Health

| Method | Path | Description |
|---|---|---|
| `GET` | `/` | Returns API metadata, version, and database dialect. |
| `GET` | `/health` | System health check reporting DB connectivity status. |

### Analytics & Workflow Diagnostics

| Method | Path | Description |
|---|---|---|
| `GET` | `/api/dashboard` | Returns system-wide executive dashboard KPIs and flow summaries. |
| `GET` | `/api/dashboard/developer/{developer_id}` | Aggregated productivity metrics for a specific developer. |
| `GET` | `/api/flow` | Focus session metrics, average flow duration, and total flow hours. |
| `GET` | `/api/interruptions` | Interruption breakdown by source, frequency, and duration impact. |
| `GET` | `/api/context-switching` | Context-switch metrics, switch rate per hour, and focus fragmentation. |
| `GET` | `/api/recovery` | Recovery time statistics after interruptions. |
| `GET` | `/api/reports/daily` | Generated daily report digest for any target date (`?report_date=YYYY-MM-DD`). |

### Telemetry Entities & Simulation

| Method | Path | Description |
|---|---|---|
| `GET` | `/api/teams` | List all engineering teams. |
| `GET` | `/api/teams/{team_id}` | Fetch team details including member profiles and aggregated metrics. |
| `GET` | `/api/developers` | List all tracked developers. |
| `GET` | `/api/developers/{developer_id}` | Detailed developer profile, active tasks, and flow score history. |
| `GET` | `/api/tasks` | List simulated Jira issues, feature tasks, and bugs. |
| `GET` | `/api/tasks/{task_id}` | Retrieve individual task details. |
| `GET` | `/api/events` | Paginated raw activity feed across IDE, Slack, Jira, and GitHub. |
| `GET` | `/api/events/{event_id}` | Retrieve single event metadata. |
| `POST` | `/api/simulation/run` | Triggers a full-day activity simulation and runs the `EventProcessor`. |

---

## 🧮 Productivity Metrics & Flow Score Engine

CogniFlow measures developer experience using quantitative behavioral models:

* **Focused Time ($T_{focus}$)**: Accumulated duration of continuous IDE activity with event intervals under the focus gap threshold ($\le 15 \text{ min}$).
* **Flow Session ($S_{flow}$)**: A contiguous block of focused work lasting at least 25 minutes without external disruptions.
* **Interruption ($I$)**: An incoming communication or external context break that halts an active flow session.
* **Context Switch ($C_{switch}$)**: A rapid transition between unrelated projects, tasks, or application domains.
* **Recovery Time ($T_{rec}$)**: The measured latency between the end of an interruption and the initiation of the next flow session.

### Proprietary Flow Score Formula

The **Flow Score ($FS \in [0, 100]$)** synthesizes these workflow signals into a single unified indicator:

$$FS = \min\left(100, \max\left(0, w_1 \cdot \text{FocusRatio} + w_2 \cdot \text{FlowSessionDensity} - w_3 \cdot \text{InterruptionPenalty} - w_4 \cdot \text{RecoveryOverhead}\right)\right)$$

Where:
* $\text{FocusRatio}$ represents total focus time over active workday hours.
* $\text{InterruptionPenalty}$ scales with high-severity interruptions during active sessions.
* $\text{RecoveryOverhead}$ penalizes prolonged focus resumption delays.

---

## 📂 Project Structure

```text
CogniFlow/
├── backend/
│   ├── alembic/                      # Database migration scripts & environment
│   │   ├── versions/                 # Alembic revision files
│   │   └── env.py                    # Alembic migration environment config
│   ├── app/
│   │   ├── api/                      # REST API routing layer
│   │   │   ├── routes/               # Modular endpoint controllers
│   │   │   │   ├── context_switching.py
│   │   │   │   ├── dashboard.py
│   │   │   │   ├── developers.py
│   │   │   │   ├── events.py
│   │   │   │   ├── flow.py
│   │   │   │   ├── interruptions.py
│   │   │   │   ├── recovery.py
│   │   │   │   ├── reports.py
│   │   │   │   ├── simulation.py
│   │   │   │   ├── tasks.py
│   │   │   │   └── teams.py
│   │   │   └── dependencies.py       # FastAPI DB session dependency injection
│   │   ├── core/                     # Application configuration & database setup
│   │   │   ├── config.py             # Pydantic Settings & env configuration
│   │   │   └── database.py           # SQLAlchemy engine setup & dual DB handling
│   │   ├── models/                   # SQLAlchemy ORM models
│   │   │   ├── context_switch.py
│   │   │   ├── developer.py
│   │   │   ├── event.py
│   │   │   ├── flow_session.py
│   │   │   ├── interruption.py
│   │   │   ├── metric.py
│   │   │   ├── task.py
│   │   │   └── team.py
│   │   ├── schemas/                  # Pydantic data validation schemas
│   │   ├── seed/                     # Automatic data seeding scripts
│   │   │   ├── seed_developers.py
│   │   │   ├── seed_tasks.py
│   │   │   └── seed_teams.py
│   │   ├── services/                 # Analytics processing engine
│   │   │   ├── context_switch_analyzer.py
│   │   │   ├── dashboard_service.py
│   │   │   ├── event_processor.py    # Main orchestration pipeline
│   │   │   ├── flow_analyzer.py
│   │   │   ├── interruption_analyzer.py
│   │   │   ├── recovery_analyzer.py
│   │   │   └── score_calculator.py   # Flow Score (0-100) engine
│   │   ├── simulator/                # Multi-source developer activity simulator
│   │   │   ├── activity_generator.py
│   │   │   ├── communication_generator.py
│   │   │   ├── developer_profiles.py
│   │   │   └── runner.py             # Simulation execution runner
│   │   └── main.py                   # FastAPI app entry point & CORS configuration
│   ├── tests/                        # Backend test suite (Pytest + HTTPX)
│   │   ├── test_context_switching.py
│   │   ├── test_dashboard.py
│   │   ├── test_developers.py
│   │   ├── test_events.py
│   │   ├── test_flow.py
│   │   ├── test_health.py
│   │   ├── test_interruptions.py
│   │   ├── test_recovery.py
│   │   ├── test_simulation.py
│   │   └── test_teams.py
│   ├── .env.example                  # Backend environment template
│   ├── alembic.ini                   # Alembic configuration
│   └── requirements.txt              # Python dependencies manifest
│
├── frontend/
│   ├── src/
│   │   ├── components/               # UI design components
│   │   │   ├── common/               # StatCard, GlassCard, StatusBadge, SectionHeader
│   │   │   ├── layout/               # Sidebar, Header, FloatingNavbar, Layout
│   │   │   ├── simulation/           # RunSimulationModal
│   │   │   └── ui/                   # EmptyState, ErrorBoundary, LoadingSpinner
│   │   ├── pages/                    # 17 Main Page Views
│   │   │   ├── ContextSwitching.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── DeveloperDetail.jsx
│   │   │   ├── Developers.jsx
│   │   │   ├── FlowAnalytics.jsx
│   │   │   ├── InterruptionAnalytics.jsx
│   │   │   ├── Landing.jsx
│   │   │   ├── LiveMonitor.jsx
│   │   │   ├── RecoveryAnalytics.jsx
│   │   │   ├── Reports.jsx
│   │   │   ├── Simulation.jsx
│   │   │   ├── TeamDetail.jsx
│   │   │   ├── Teams.jsx
│   │   │   └── Timeline.jsx
│   │   ├── routes/                   # AppRoutes.jsx client-side router
│   │   ├── services/                 # Axios API integration clients
│   │   ├── main.jsx                  # React DOM root entry point
│   │   └── App.jsx                   # Primary container component
│   ├── index.html                    # HTML5 entry page
│   ├── package.json                  # React dependencies & scripts
│   └── vite.config.js                # Vite build configuration & server proxy
│
├── package.json                      # Root scripts & concurrently launcher
├── .gitignore                        # Git exclusion rules
└── README.md                         # Enterprise project documentation
```

---

## 🧪 Testing & Quality Assurance

CogniFlow includes a complete backend testing suite built with `pytest` and `httpx`. The suite exercises health endpoints, entity listings, simulation runs, event processors, and analytics analyzers against an isolated SQLite test database.

### Running Backend Tests

Navigate to the `backend` directory and execute `pytest`:

```bash
cd backend
pytest
```

**Expected Test Output**:
```text
============================= test session starts =============================
platform win32 -- Python 3.13.5, pytest-9.0.3, pluggy-1.6.0
rootdir: D:\Infotact_Solutions\CogniFlow\backend
plugins: anyio-4.9.0, asyncio-1.4.0, cov-7.1.0

tests\test_context_switching.py ...                                      [  9%]
tests\test_dashboard.py ....                                             [ 21%]
tests\test_developers.py .....                                           [ 36%]
tests\test_events.py ....                                                [ 48%]
tests\test_flow.py ...                                                   [ 57%]
tests\test_health.py ..                                                  [ 63%]
tests\test_interruptions.py ...                                          [ 72%]
tests\test_recovery.py ...                                               [ 81%]
tests\test_simulation.py ...                                             [ 90%]
tests\test_teams.py ...                                                  [100%]

============================= 33 passed in 8.57s ==============================
```

### Running Frontend Build Check

To verify that the frontend compiles cleanly without bundle or import errors:

```bash
cd frontend
npm run build
```

---

## 📄 License

This project is open-source and released under the **[MIT License](LICENSE)**.

---

<div align="center">

**CogniFlow — Engineering Visibility Through Workflow Telemetry**

*Built for software engineers, tech leads, and product teams striving for continuous focus.*

</div>
