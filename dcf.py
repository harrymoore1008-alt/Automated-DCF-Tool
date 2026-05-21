"""
DCF Valuation Tool
==================
Automated Discounted Cash Flow valuation using live financial data.
Author: Harry Moore
GitHub: harrymoore1008-alt
"""

import yfinance as yf
import pandas as pd
import numpy as np

# ── USER INPUTS ───────────────────────────────────────────────────────────────
TICKER          = "NVDA"   # Stock ticker
REVENUE_GROWTH  = [0.35, 0.28, 0.22, 0.18, 0.15]  # Revenue growth rates Y1-Y5
EBIT_MARGIN     = 0.55     # Assumed steady-state EBIT margin
TAX_RATE        = 0.13     # Effective tax rate
CAPEX_PCT       = 0.03     # CapEx as % of revenue
DA_PCT          = 0.04     # D&A as % of revenue
NWC_PCT         = 0.02     # Change in NWC as % of revenue
WACC            = 0.10     # Weighted Average Cost of Capital
TERMINAL_GROWTH = 0.03     # Terminal growth rate
# ─────────────────────────────────────────────────────────────────────────────


def fetch_data(ticker):
    """Pull live financials from Yahoo Finance."""
    print(f"\n📡 Fetching live data for {ticker}...")
    stock = yf.Ticker(ticker)
    info  = stock.info

    revenue     = info.get("totalRevenue")
    shares      = info.get("sharesOutstanding")
    net_debt    = (info.get("totalDebt", 0) or 0) - (info.get("totalCash", 0) or 0)
    price       = info.get("currentPrice") or info.get("regularMarketPrice")
    name        = info.get("longName", ticker)

    if not revenue or not shares:
        raise ValueError("Could not fetch financials. Check ticker symbol.")

    print(f"✅ {name}")
    print(f"   Revenue:        ${revenue/1e9:.1f}B")
    print(f"   Current Price:  ${price:.2f}")
    print(f"   Shares Out:     {shares/1e9:.2f}B")

    return revenue, shares, net_debt, price, name


def project_fcf(base_revenue):
    """Project Free Cash Flows over 5 years."""
    fcfs    = []
    revenue = base_revenue

    for g in REVENUE_GROWTH:
        revenue  = revenue * (1 + g)
        ebit     = revenue * EBIT_MARGIN
        nopat    = ebit * (1 - TAX_RATE)
        da       = revenue * DA_PCT
        capex    = revenue * CAPEX_PCT
        nwc      = revenue * NWC_PCT
        fcf      = nopat + da - capex - nwc
        fcfs.append(fcf)

    return fcfs


def discount_fcfs(fcfs):
    """Discount FCFs back to present value."""
    pvs = [fcf / (1 + WACC) ** (i + 1) for i, fcf in enumerate(fcfs)]
    return pvs


def terminal_value(fcfs):
    """Calculate terminal value using Gordon Growth Model."""
    final_fcf = fcfs[-1] * (1 + TERMINAL_GROWTH)
    tv        = final_fcf / (WACC - TERMINAL_GROWTH)
    pv_tv     = tv / (1 + WACC) ** len(fcfs)
    return tv, pv_tv


def intrinsic_value(pvs, pv_tv, net_debt, shares):
    """Calculate per-share intrinsic value."""
    enterprise_value = sum(pvs) + pv_tv
    equity_value     = enterprise_value - net_debt
    per_share        = equity_value / shares
    return enterprise_value, equity_value, per_share


def sensitivity_table(base_revenue, net_debt, shares):
    """Build WACC vs Terminal Growth sensitivity table."""
    waccs   = [0.08, 0.09, 0.10, 0.11, 0.12]
    tgrs    = [0.02, 0.025, 0.03, 0.035, 0.04]

    print("\n📊 SENSITIVITY ANALYSIS — Implied Share Price ($)")
    print(f"   {'':>8}", end="")
    print("  TGR →", end="")
    for tgr in tgrs:
        print(f"  {tgr*100:.1f}%", end="")
    print()

    fcfs = project_fcf(base_revenue)

    for w in waccs:
        print(f"   WACC {w*100:.0f}%  |", end="")
        for tgr in tgrs:
            tv        = fcfs[-1] * (1 + tgr) / (w - tgr)
            pv_tv     = tv / (1 + w) ** len(fcfs)
            pvs       = [fcf / (1 + w) ** (i + 1) for i, fcf in enumerate(fcfs)]
            ev        = sum(pvs) + pv_tv
            eq        = ev - net_debt
            price     = eq / shares
            print(f"  ${price:>6.0f}", end="")
        print()


def run():
    print("=" * 55)
    print("        DCF VALUATION TOOL  |  Harry Moore")
    print("=" * 55)

    revenue, shares, net_debt, market_price, name = fetch_data(TICKER)

    fcfs  = project_fcf(revenue)
    pvs   = discount_fcfs(fcfs)
    tv, pv_tv = terminal_value(fcfs)
    ev, eq, price_per_share = intrinsic_value(pvs, pv_tv, net_debt, shares)

    updown = ((price_per_share / market_price) - 1) * 100
    arrow  = "📈" if updown > 0 else "📉"

    print("\n─── DCF OUTPUT ───────────────────────────────────────")
    print(f"   Company:              {name}")
    print(f"   Enterprise Value:     ${ev/1e9:.1f}B")
    print(f"   Equity Value:         ${eq/1e9:.1f}B")
    print(f"   Intrinsic Value/Share: ${price_per_share:.2f}")
    print(f"   Current Price:        ${market_price:.2f}")
    print(f"   Implied Upside/Down:  {updown:+.1f}%  {arrow}")
    print("──────────────────────────────────────────────────────")

    # FCF table
    print("\n─── PROJECTED FREE CASH FLOWS ────────────────────────")
    print(f"   {'Year':<6} {'FCF ($B)':>10}  {'PV ($B)':>10}")
    for i, (fcf, pv) in enumerate(zip(fcfs, pvs), 1):
        print(f"   Y{i:<5} {fcf/1e9:>10.2f}  {pv/1e9:>10.2f}")
    print(f"   {'TV':<6} {tv/1e9:>10.1f}  {pv_tv/1e9:>10.1f}")
    print("──────────────────────────────────────────────────────")

    sensitivity_table(revenue, net_debt, shares)

    print("\n✅ Done. Adjust assumptions at the top of dcf.py to stress-test.")
    print("=" * 55)


if __name__ == "__main__":
    run()
