import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="8-Rule Stock Analyzer", layout="centered")

st.title("📈 8-Rule Stock Analyzer")
st.write("Enter a US Ticker to run the 1-10 Scale Analysis")

ticker_input = st.text_input("Enter Ticker (e.g. PLTR, MSFT, NVDA)", "PLTR").upper()

if ticker_input:
    stock = yf.Ticker(ticker_input)
    info = stock.info
    
    # --- AUTOMATED DATA FETCHING ---
    try:
        rev_growth = info.get('revenueGrowth', 0) * 100
        pe_ratio = info.get('forwardPE', 0)
        pb_ratio = info.get('priceToBook', 0)
        sector = info.get('sector', 'Unknown')
        current_price = info.get('currentPrice', 0)
        
        st.subheader(f"Data for {ticker_input} ({sector})")
        col1, col2, col3 = st.columns(3)
        col1.metric("Rev Growth", f"{rev_growth:.1f}%")
        col2.metric("P/E Ratio", f"{pe_ratio:.2f}")
        col3.metric("P/B Ratio", f"{pb_ratio:.2f}")

        st.divider()
        st.write("### Rate the 8 Filters")

        # --- SCORING SYSTEM ---
        # Rule 1 & 6 are auto-calculated for suggestions
        score = 0
        
        # Rule 1: Revenue Growth
        r1 = st.checkbox(f"Filter 1: Revenue Growth (>15% is {rev_growth:.1f}%)", value=(rev_growth > 15))
        if r1: score += 1.25

        # Rule 2: Moat/Competitive Position
        r2 = st.checkbox("Filter 2: Strong Moat (Network effects/Switching costs)")
        if r2: score += 1.25

        # Rule 3: Leadership Quality
        r3 = st.checkbox("Filter 3: Leadership (Executing/Insider Buying)")
        if r3: score += 1.25

        # Rule 4: Market Timing
        r4 = st.checkbox("Filter 4: Market Timing (Catalyst exists NOW)")
        if r4: score += 1.25

        # Rule 5: Risk Assessment
        r5 = st.checkbox("Filter 5: Risks Quantified & Acceptable")
        if r5: score += 1.25

        # Rule 6: Valuation (P/E & P/B vs Peers)
        st.info(f"Compare: {ticker_input} P/E is {pe_ratio:.1f}. (Standard S&P 500 avg is ~20-25)")
        r6 = st.checkbox("Filter 6: Valuation is Fair/Underpriced")
        if r6: score += 1.25
        
        # Rule 7 & 8: Open slots for your remaining criteria or extra weight
        r7 = st.checkbox("Filter 7: Financial Health (Cash > Debt)")
        if r7: score += 1.25
        
        r8 = st.checkbox("Filter 8: Profitability (Increasing Margins)")
        if r8: score += 1.25

        st.divider()
        
        # --- FINAL VERDICT ---
        final_score = score
        st.header(f"Total Score: {final_score}/10")
        
        if final_score >= 7:
            st.success("🔥 VERDICT: BUY")
        elif final_score >= 5:
            st.warning("⚖️ VERDICT: HOLD")
        else:
            st.error("🚫 VERDICT: SELL")

    except Exception as e:
        st.error(f"Could not find data for {ticker_input}. Check the ticker symbol.")
