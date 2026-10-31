# ReliefRoute — Smart Disaster Resource Allocation Simulator

A Streamlit-based academic prototype that demonstrates allocation of limited food, water, and medical supplies across simulated disaster-affected areas.

## Run locally
1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Create/activate a virtual environment (optional but recommended).
4. Install dependencies:
   `pip install -r requirements.txt`
5. Run:
   `streamlit run app.py`

## Demo workflow
1. Run the app and review the sample affected areas.
2. Change the available stock in the sidebar.
3. Edit area population, urgency, and demand values.
4. Click **Generate Allocation Plan**.
5. Compare allocated quantities and unmet demand.
6. Download the CSV report.

## Algorithm
- Priority-weighted greedy: distributes stock using urgency and affected-population weights, respecting each area's demand cap.
- Proportional fair-share: distributes stock in proportion to demand, also respecting demand caps.

## Important limitation
This is a simulated educational decision-support prototype, not a real emergency response system. Its inputs, assumptions, and allocation heuristic have not been validated for operational disaster management.
