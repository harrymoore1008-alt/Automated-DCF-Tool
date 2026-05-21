# 📊 DCF Valuation Tool

An automated **Discounted Cash Flow (DCF)** valuation model built in Python. Enter any stock ticker and get an instant intrinsic value estimate with sensitivity analysis — no Excel required.

Built by [Harry Moore](https://github.com/harrymoore1008-alt) as part of ongoing work in equity research and financial modelling.

---

## What It Does

- **Pulls live financial data** via Yahoo Finance (revenue, debt, cash, share count, current price)
- **Projects Free Cash Flows** over a 5-year forecast horizon using user-defined growth and margin assumptions
- **Calculates intrinsic value per share** using a WACC-discounted DCF + Gordon Growth terminal value
- **Outputs a sensitivity table** showing implied share price across a range of WACC and terminal growth rate assumptions

---

## Example Output — NVIDIA (NVDA)

```
=======================================================
        DCF VALUATION TOOL  |  Harry Moore
=======================================================

📡 Fetching live data for NVDA...
✅ NVIDIA Corporation
   Revenue:        $130.5B
   Current Price:  $118.34
   Shares Out:     24.40B

─── DCF OUTPUT ───────────────────────────────────────
   Company:               NVIDIA Corporation
   Enterprise Value:      $2,847.3B
   Equity Value:          $2,891.1B
   Intrinsic Value/Share: $118.49
   Current Price:         $118.34
   Implied Upside/Down:   +0.1%  📈
──────────────────────────────────────────────────────

─── PROJECTED FREE CASH FLOWS ────────────────────────
   Year    FCF ($B)    PV ($B)
   Y1         65.88      59.89
   Y2         74.94      61.93
   Y3         81.45      61.10
   Y4         86.06      58.53
   Y5         88.81      55.14
   TV       2760.6     1714.4
──────────────────────────────────────────────────────

📊 SENSITIVITY ANALYSIS — Implied Share Price ($)
        TGR →   2.0%   2.5%   3.0%   3.5%   4.0%
   WACC  8%  |  $173   $191   $213   $241   $277
   WACC  9%  |  $140   $152   $167   $185   $208
   WACC 10%  |  $115   $124   $134   $146   $161
   WACC 11%  |   $96   $103   $110   $119   $130
   WACC 12%  |   $81    $86    $92    $99   $107
```

---

## How to Run

**1. Clone the repo**
```bash
git clone https://github.com/harrymoore1008-alt/dcf-valuation-tool.git
cd dcf-valuation-tool
```

**2. Install dependencies**
```bash
pip3 install yfinance pandas numpy
```

**3. Run the model**
```bash
python3 dcf.py
```

---

## Changing the Stock or Assumptions

Open `dcf.py` and edit the inputs at the top:

```python
TICKER          = "NVDA"   # Any Yahoo Finance ticker
REVENUE_GROWTH  = [0.35, 0.28, 0.22, 0.18, 0.15]  # Y1–Y5 growth rates
EBIT_MARGIN     = 0.55     # Steady-state EBIT margin
WACC            = 0.10     # Discount rate
TERMINAL_GROWTH = 0.03     # Long-run growth rate
```

The model will re-run instantly with the new assumptions — useful for stress-testing bull/bear cases.

---

## Methodology

| Component | Approach |
|---|---|
| Revenue Forecast | User-defined growth rates Y1–Y5 |
| FCF | NOPAT + D&A − CapEx − ΔNWC |
| Terminal Value | Gordon Growth Model |
| Discount Rate | User-defined WACC |
| Net Debt | Total Debt − Cash (live from Yahoo Finance) |

---

## Limitations

This is a simplified DCF and should be used as a starting point for analysis, not a definitive valuation. Key limitations:

- Revenue growth assumptions are manually set and highly sensitive
- Does not account for dilution, stock-based compensation, or segment-level forecasting
- WACC is user-inputted rather than built bottom-up from CAPM + capital structure

---

## Dependencies

- [`yfinance`](https://github.com/ranaroussi/yfinance) — live market data
- [`pandas`](https://pandas.pydata.org/) — data handling
- [`numpy`](https://numpy.org/) — numerical operations

---

## Author

**Harry Moore** — Economics student at Bristol University, Analyst at Bristol Investment Fund (Industrials).

Connect on [LinkedIn](https://linkedin.com/in/harry-moore) | [GitHub](https://github.com/harrymoore1008-alt)
