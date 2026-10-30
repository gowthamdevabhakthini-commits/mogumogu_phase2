# `mogumogu` — Qiskit Fall Fest 2026 (Phase 2 Hackathon)

[![Qiskit](https://img.shields.io/badge/Qiskit-1.4%2B-blueviolet.svg)](https://qiskit.org/)
[![Track](https://img.shields.io/badge/Track-Quantum%20Optimization-blue.svg)](#)
[![Problem Statement](https://img.shields.io/badge/PS--O3-0%2F1%20Knapsack%20Problem-green.svg)](#)
[![Status](https://img.shields.io/badge/Phase%202-Complete%20%26%20Pre--Rendered-brightgreen.svg)](#)

Official Phase 2 submission for Team **`mogumogu`** in the **Quantum Optimization Track** of the Qiskit Fall Fest 2026 Hackathon.

---

## 1. Executive Summary & Key Results

Our project implements a full-stack **Algorithm $\leftrightarrow$ Hardware Co-Design Framework** to solve the NP-hard 0/1 Knapsack Problem (**PS-O3**). We mapped the constrained optimization problem into a 9-qubit Quadratic Unconstrained Binary Optimization (QUBO) Hamiltonian utilizing 5 item qubits and 4 binary slack qubits ($s_0, s_1, s_2, s_3$) with a locked penalty multiplier $P = 5.0$.

To overcome heavy two-qubit CNOT gate noise and SWAP routing overhead on NISQ hardware, we engineered a custom 9-qubit topology (**Processor D**) that eliminates routing SWAP gates entirely for bipartite item-slack interactions while maintaining a maximum vertex degree of $\le 4$.

```
+-----------------------------------------------------------------------------------------------------------------+
|                                    HARDWARE CO-DESIGN BENCHMARK SUMMARY                                         |
+---------------+-----------+------------+-------+-------+------------+-----------------+-----------------+-------+
| Processor     | Condition | Executable | Depth | CX    | SWAP Gates | $P_{feasible}$  | $P_{opt}$       | $V^*$ |
+---------------+-----------+------------+-------+-------+------------+-----------------+-----------------+-------+
| Processor A   | Ideal     | False      | --    | --    | --         | --              | --              | 26    |
| Processor B   | Ideal     | True       | 60    | 32    | 2          | 95.89%          | 8.76%           | 26    |
| Processor B   | Noisy     | True       | 60    | 32    | 2          | 95.60%          | 9.10%           | 26    |
| Processor D   | Ideal     | True       | 41    | 26    | 0          | 95.89%          | 8.76%           | 26    |
| Processor D   | Noisy     | True       | 41    | 26    | 0          | 95.89%          | 9.11%           | 26    |
+---------------+-----------+------------+-------+-------+------------+-----------------+-----------------+-------+
| Baseline      | Uniform   | N/A        | 0     | 0     | 0          | 87.50%          | 3.125%          | 26    |
+---------------+-----------+------------+-------+-------+------------+-----------------+-----------------+-------+
| IMPACT        | Proc D vs B            | -31.7%| -18.8%| -100.0%    | +8.39% over rnd | 3x over rnd     | Exact |
+---------------+------------------------+-------+-------+------------+-----------------+-----------------+-------+
```

---

## 2. Eligibility Gate Compliance Checklist

| Gate | Requirement | Status | Verification Detail |
| :---: | :--- | :---: | :--- |
| **G1** | Repository URL submitted before official 24-hour deadline | **PASSED** | Staged and pushed to remote `main` branch. |
| **G2** | Exactly one problem statement (PS-O3) addressed and named in README | **PASSED** | PS-O3 (0/1 Knapsack Problem) addressed exclusively. |
| **G3** | `main.ipynb` executes top-to-bottom and reproduces Processor B results | **PASSED** | Notebook pre-rendered in-place; executes within $< 5$ minutes. |
| **G4** | `results/tables/results.csv` (kit format) and `report.md` present | **PASSED** | All required CSV tables and 6-page report present. |

---

## 3. Team Roster & Affiliations

* **Meghana Sai** (Team Lead) — SRM University-AP
* **Gowtham Devabhakthini** — Indian Institute of Information Technology, Sri City
* **Pallavi Bachina** — SRM University-AP
* **Radhika** — SRM University-AP
* **Pavan Sai** — SRM University-AP
* **Likith** — SRM University-AP

---

## 4. Repository Directory Layout

```text
mogumogu_phase2/
├── README.md                 # Team roster, gate status, summary results
├── main.ipynb                # Primary pre-rendered executable notebook
├── main_phase2.py            # Master automated benchmarking pipeline
├── requirements.txt          # Pinned dependency specifications
├── qff_phase2.py             # Official organizer starter pack module (Unchanged)
├── data/
│   └── instance.json         # Locked PS-O3 dataset copy
├── processors/
│   ├── processor_A.json      # Locked 5-qubit topology
│   ├── processor_B.json      # Locked 9-qubit heavy-hex topology
│   └── processor_D.json      # Custom 9-qubit frozen topology (Max degree <= 4)
├── src/
│   ├── problem_phase2.py     # 9-qubit QUBO formulation & QAOA circuit builder
│   └── bell_phase2.py        # Objective 1 Bell-state verification module
├── results/
│   ├── tables/
│   │   ├── results.csv       # Master hardware benchmark table (Kit format)
│   │   ├── bell.csv          # Bell-state correlation & fidelity metrics
│   │   └── algorithm_comparison.csv # Classical vs Quantum comparative benchmarks
│   └── figures/
│       └── landscape_processor_D.png # 20x20 Noisy energy landscape plot
└── report.md                 # Technical Analysis Report (Objective 5)
```

---

## 5. Quickstart & Reproducibility Guide

Follow these steps to reproduce all benchmark tables and figures from a clean terminal environment:

### Step 1: Activate Virtual Environment & Install Dependencies
```bash
# Using the official hackathon environment or a clean venv
source ~/QFF/.qff2026-venv/bin/activate

# Install pinned dependencies
pip install -r requirements.txt
```

### Step 2: Execute Master Pipeline
```bash
python main_phase2.py
```
This executes:
1. **Objective 1:** Bell-state verification across distance-1 and distance-4 physical pairs on Processor D ($XX$, $YY$, $ZZ$ bases, ideal & noisy).
2. **Objective 2 & 3:** 5-seed COBYLA parameter optimization ($\gamma^* = 2.9909, \beta^* = 0.6701$), capacity rule enforcement for Processor A, and full hardware transpilation benchmarks for Processors B and D.
3. **Landscape Rendering:** $20 \times 20$ energy landscape grid evaluation on Processor D Noisy (1,024 shots per grid point).

### Step 3: Run Executable Notebook Top-to-Bottom
```bash
jupyter nbconvert --execute --to notebook --inplace main.ipynb
```

---

## 6. Official Problem Instance Specifications (PS-O3)

* **Item Values ($V$):** $[10, 4, 7, 5, 8]$
* **Item Weights ($W$):** $[5, 3, 4, 2, 6]$
* **Maximum Capacity ($C$):** $15$ weight units
* **Slack Variable Encoding:** $s = s_0 + 2s_1 + 4s_2 + 8s_3 \in [0, 15]$ on qubits $q_5, q_6, q_7, q_8$
* **Penalty Weight:** $P = 5.0$
* **Exact Classical Optimum ($V^*$):** $V^* = 26$ (Selecting items 1, 2, 3, and 4 $\implies$ Item bitstring `11110`, Total Weight $= 14 \le 15$)

---

## 7. AI Tool Disclosure

In accordance with official hackathon rules, AI tools (Gemini) were used strictly as a coding assistant for script syntax verification and markdown formatting. All algorithm formulations, QUBO mathematical derivations, hardware topology graph designs, and technical interpretations were independently developed and verified by team members.