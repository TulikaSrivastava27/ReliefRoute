# 🚑 ReliefRoute — Smart Disaster Resource Allocation Simulator

**ReliefRoute** is a Python-based, interactive decision-support prototype that demonstrates how limited disaster-relief supplies can be distributed across multiple affected areas.

The application lets users enter estimated needs and available stock for **food packets, drinking water, and medical kits**, choose an allocation strategy, and review the resulting allocations and shortages.

## 🌐 Live Project

[Open ReliefRoute](https://reliefroute-iysuddxplt9u4jkushtais.streamlit.app/)

## ✨ Features

- **Editable affected-area data:** Add or update area names, affected population, urgency, and estimated resource needs.
- **Adjustable resource stock:** Set the available quantities of food, water, and medical kits.
- **Two allocation strategies:**
  - **Priority-Weighted Greedy:** Uses urgency and affected population to calculate priority weights.
  - **Proportional Fair-Share:** Distributes available stock in proportion to each area's requested quantity.
- **Allocation summary:** View supplied quantities and overall demand coverage.
- **Shortage analysis:** See how much food, water, and medical support remains unmet in each area.
- **Interactive charts:** Compare allocated resources and unmet demand across areas.
- **CSV export:** Download the generated allocation report.

## 🧰 Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic and calculations |
| Streamlit | Interactive web dashboard |
| Pandas | Data handling and result tables |
| NumPy | Numerical allocation calculations |
| Plotly | Interactive charts |
| CSV | Exporting allocation reports |

## ⚙️ Run Locally

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd <repository-folder>
```

### 2. Create a virtual environment (optional)

```bash
python -m venv venv
```

Activate it:

**Windows**
```bash
venv\\Scripts\\activate
```

**macOS / Linux**
```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the application

```bash
streamlit run app.py
```

The application will open in your browser.

## 🧭 How to Use

1. Open the app and review the sample affected areas.
2. Set the available food, water, and medical-kit stock in the sidebar.
3. Edit the affected areas, population, urgency, and estimated needs in the table.
4. Select an allocation strategy.
5. Click **Generate Allocation Plan**.
6. Review the allocation table, summary metrics, charts, and remaining shortages.
7. Download the results using the CSV export button.

## 🧠 How the Allocation Logic Works

### Priority-Weighted Greedy

Each area receives a priority score based on its urgency and affected population:

```text
Priority Weight = Urgency × (1 + People Affected / Maximum People Affected)
```

Available stock is shared according to these weights. The allocation process respects each area's estimated demand and repeats while stock and unmet demand remain.

### Proportional Fair-Share

Available stock is distributed in proportion to each area's requested quantity, subject to the area's demand limit.

For both strategies, allocations are converted to whole units. Remaining units are assigned using the largest fractional remainders.

## 📁 Project Structure

```text
ReliefRoute/
│
├── app.py
├── requirements.txt
└── README.md
```

## ⚠️ Limitations

- The project uses sample and user-entered simulated data.
- It does not connect to live disaster information.
- It does not provide GIS-based mapping or validated relief-vehicle routing.
- The allocation methods are simplified educational heuristics, not proven optimal or fair models.
- The application is intended for academic demonstration and planning exercises only.

**Important:** ReliefRoute is not a real emergency-response system. Its outputs should not be used to make operational disaster-management decisions.

## 🚀 Future Scope

Possible future improvements include:

- Integration with verified, real-time disaster data.
- GIS-based mapping of affected areas.
- Relief vehicle route optimisation.
- More detailed priority scoring.
- Per-resource demand-coverage metrics.
- Additional allocation algorithms and testing for fairness and efficiency.

## 👩‍💻 Developer

**Tulika Srivastava**  
B.Tech — Information Technology

---

*ReliefRoute — Intelligent Disaster Relief Resource Allocation and Decision Support System.*
