"""
Streamlit frontend for Investment Platform
Connects to Django REST API endpoints
"""
import streamlit as st
import requests
import json
from datetime import datetime

# Configuration
API_BASE_URL = "http://localhost:8000/api"
st.set_page_config(page_title="Investment Platform", page_icon="💼", layout="wide")

# ============================================================================
# Session State & Auth Helpers
# ============================================================================

def init_session_state():
    if "token" not in st.session_state:
        st.session_state.token = None
    if "user" not in st.session_state:
        st.session_state.user = None

def set_auth_token(token, user_data):
    st.session_state.token = token
    st.session_state.user = user_data

def clear_auth():
    st.session_state.token = None
    st.session_state.user = None
    st.rerun()

def get_headers():
    if st.session_state.token:
        return {"Authorization": f"Token {st.session_state.token}"}
    return {}

# ============================================================================
# API Helpers
# ============================================================================

def api_call(endpoint, method="GET", data=None, headers=None):
    """Make an API call and handle errors"""
    if headers is None:
        headers = get_headers()
    
    url = f"{API_BASE_URL}{endpoint}"
    try:
        if method == "GET":
            resp = requests.get(url, headers=headers)
        elif method == "POST":
            resp = requests.post(url, json=data, headers=headers)
        elif method == "PUT":
            resp = requests.put(url, json=data, headers=headers)
        
        if resp.status_code == 401:
            st.error("Unauthorized. Please log in again.")
            clear_auth()
            return None
        
        if resp.status_code >= 400:
            st.error(f"Error {resp.status_code}: {resp.text[:200]}")
            return None
        
        return resp.json()
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to backend. Is Django running on http://localhost:8000?")
        return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

# ============================================================================
# Pages
# ============================================================================

def page_login():
    st.title("💼 Investment Platform")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.subheader("Login")
        
        email = st.text_input("Email Address", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("🔓 Login", use_container_width=True):
            if not email or not password:
                st.error("Please enter email and password")
                return
            
            # Use the token_login endpoint (doesn't create Django session)
            resp = api_call(
                "/users/token_login/",
                method="POST",
                data={"email": email, "password": password},
                headers={}
            )
            
            if resp:
                token = resp.get("token")
                user = resp.get("user")
                if token and user:
                    set_auth_token(token, user)
                    st.success(f"✅ Welcome, {user.get('first_name', user.get('email'))}!")
                    st.rerun()
                else:
                    st.error("Login failed: invalid response")
        
        st.markdown("---")
        st.info("💡 **Demo Credentials**\n\n- Email: `user@example.com`\n- Password: `TestUser!123`")

def page_dashboard():
    st.title("📊 Dashboard")
    
    user_data = api_call("/users/me/")
    if not user_data:
        return
    
    # Update session user
    st.session_state.user = user_data
    
    # Header with user info and logout
    col1, col2 = st.columns([4, 1])
    with col1:
        st.write(f"**Welcome, {user_data.get('first_name', '')} {user_data.get('last_name', '')}**")
        st.write(f"Email: `{user_data.get('email')}`")
    with col2:
        if st.button("🚪 Logout"):
            clear_auth()
    
    st.markdown("---")
    
    # Balance cards
    balance = float(user_data.get("balance", 0))
    total_invested = float(user_data.get("total_invested", 0))
    total_earnings = float(user_data.get("total_earnings", 0))
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💰 Current Balance", f"${balance:,.2f}")
    with col2:
        st.metric("📈 Total Invested", f"${total_invested:,.2f}")
    with col3:
        st.metric("💵 Total Earnings", f"${total_earnings:,.2f}")
    
    st.markdown("---")
    
    # Recent activity
    st.subheader("📋 Recent Activity")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Active Investments**")
        invs = api_call("/investments/my-investments/active_investments/")
        if invs:
            if isinstance(invs, list) and len(invs) > 0:
                for inv in invs[:3]:
                    st.write(f"- {inv.get('plan_name', 'Plan')}: ${inv.get('amount', 0)} @ {inv.get('roi', 0)}%")
            else:
                st.info("No active investments yet")
        else:
            st.info("No active investments yet")
    
    with col2:
        st.write("**Recent Deposits**")
        deps = api_call("/deposits/")
        if deps:
            if isinstance(deps, dict) and "results" in deps:
                for dep in deps["results"][:3]:
                    st.write(f"- {dep.get('cryptocurrency', 'N/A')}: ${dep.get('amount', 0)} ({dep.get('status', 'pending')})")
            elif isinstance(deps, list) and len(deps) > 0:
                for dep in deps[:3]:
                    st.write(f"- {dep.get('cryptocurrency', 'N/A')}: ${dep.get('amount', 0)} ({dep.get('status', 'pending')})")
            else:
                st.info("No deposits yet")
        else:
            st.info("No deposits yet")

def page_investments():
    st.title("📈 Investment Plans")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    with col2:
        pass
    
    st.markdown("---")
    
    # Get available plans
    plans_resp = api_call("/investments/plans/", headers={})  # Public endpoint
    if not plans_resp:
        return
    
    plans = plans_resp.get("results", plans_resp) if isinstance(plans_resp, dict) else plans_resp
    
    if not plans:
        st.info("No investment plans available")
        return
    
    # Get user's current balance
    user_data = api_call("/users/me/")
    balance = float(user_data.get("balance", 0)) if user_data else 0
    
    st.write(f"**Your Balance:** `${balance:,.2f}`")
    st.markdown("---")
    
    # Display plans
    for plan in plans:
        with st.container(border=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"### {plan.get('name', 'Plan').title()}")
                st.write(f"**ROI:** {plan.get('roi_percentage', 0)}%")
            with col2:
                st.write(f"**Duration:** {plan.get('duration_days', 0)} days")
                st.write(f"**Min:** ${plan.get('minimum_investment', 0):,.2f}")
            with col3:
                st.write(f"**Max:** ${plan.get('maximum_investment', 'N/A')}")
            
            col1, col2 = st.columns([2, 1])
            with col1:
                amount = st.number_input(
                    f"Investment amount ({plan.get('name', 'Plan')})",
                    min_value=float(plan.get('minimum_investment', 0)),
                    value=float(plan.get('minimum_investment', 0)),
                    key=f"inv_amount_{plan.get('id')}"
                )
            with col2:
                if st.button("💳 Invest", key=f"invest_btn_{plan.get('id')}", use_container_width=True):
                    if amount > balance:
                        st.error(f"Insufficient balance. You have ${balance:,.2f}")
                    else:
                        resp = api_call(
                            "/investments/my-investments/subscribe/",
                            method="POST",
                            data={"plan": plan.get("id"), "amount": amount}
                        )
                        if resp:
                            st.success(f"✅ Invested ${amount:,.2f} in {plan.get('name')}!")
                            st.rerun()

def page_deposits():
    st.title("💸 Deposits")
    
    st.markdown("---")
    st.subheader("📝 Submit New Deposit")
    
    # Get wallets
    wallets_resp = api_call("/deposits/wallets/", headers={})
    if not wallets_resp:
        return
    
    wallets = wallets_resp.get("results", wallets_resp) if isinstance(wallets_resp, dict) else wallets_resp
    
    if not wallets:
        st.info("No wallets available")
        return
    
    wallet_options = {w.get("cryptocurrency"): w for w in wallets}
    
    with st.form("deposit_form"):
        crypto = st.selectbox("Cryptocurrency", list(wallet_options.keys()))
        amount = st.number_input("Amount", min_value=0.0, step=0.001)
        proof_type = st.selectbox("Proof Type", ["transaction_hash", "note"])
        proof_content = st.text_area("Proof (transaction hash or note)")
        
        if st.form_submit_button("📤 Submit Deposit", use_container_width=True):
            if not crypto or amount <= 0 or not proof_content:
                st.error("Please fill all fields")
            else:
                resp = api_call(
                    "/deposits/",
                    method="POST",
                    data={
                        "cryptocurrency": crypto,
                        "amount": amount,
                        "proof_type": proof_type,
                        "proof_content": proof_content
                    }
                )
                if resp:
                    st.success(f"✅ Deposit submitted! Awaiting admin approval.")
                    st.rerun()
    
    # Show wallet address for selected crypto
    if wallets:
        selected_wallet = wallet_options.get(crypto)
        if selected_wallet:
            st.info(f"📍 **Send {crypto} to:**\n\n`{selected_wallet.get('wallet_address')}`")
    
    st.markdown("---")
    st.subheader("📜 Deposit History")
    
    deposits = api_call("/deposits/")
    if deposits:
        deposits_list = deposits.get("results", deposits) if isinstance(deposits, dict) else deposits
        if deposits_list:
            for dep in deposits_list:
                with st.container(border=True):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(f"**{dep.get('cryptocurrency', 'N/A')}**")
                        st.write(f"${dep.get('amount', 0)}")
                    with col2:
                        st.write(f"Status: `{dep.get('status', 'pending')}`")
                        st.write(f"Date: {dep.get('created_at', 'N/A')[:10]}")
                    with col3:
                        st.write("")
        else:
            st.info("No deposits yet")
    else:
        st.info("No deposits yet")

def page_withdrawals():
    st.title("🏦 Withdrawals")
    
    # Get user balance
    user_data = api_call("/users/me/")
    if not user_data:
        return
    
    balance = float(user_data.get("balance", 0))
    st.write(f"**Available Balance:** `${balance:,.2f}`")
    
    st.markdown("---")
    st.subheader("📝 Request Withdrawal")
    
    with st.form("withdrawal_form"):
        crypto = st.selectbox("Cryptocurrency", ["BTC", "ETH"])
        amount = st.number_input("Amount", min_value=0.0, max_value=balance, step=0.001)
        wallet_address = st.text_input("Your wallet address")
        
        if st.form_submit_button("💳 Request Withdrawal", use_container_width=True):
            if not crypto or amount <= 0 or not wallet_address:
                st.error("Please fill all fields")
            elif amount > balance:
                st.error(f"Insufficient balance. You have ${balance:,.2f}")
            else:
                resp = api_call(
                    "/withdrawals/",
                    method="POST",
                    data={
                        "cryptocurrency": crypto,
                        "amount": amount,
                        "wallet_address": wallet_address
                    }
                )
                if resp:
                    st.success(f"✅ Withdrawal request submitted! You'll receive ${amount} {crypto} soon.")
                    st.rerun()
    
    st.markdown("---")
    st.subheader("📜 Withdrawal History")
    
    withdrawals = api_call("/withdrawals/")
    if withdrawals:
        withdrawals_list = withdrawals.get("results", withdrawals) if isinstance(withdrawals, dict) else withdrawals
        if withdrawals_list:
            for wd in withdrawals_list:
                with st.container(border=True):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(f"**{wd.get('cryptocurrency', 'N/A')}**")
                        st.write(f"${wd.get('amount', 0)}")
                    with col2:
                        st.write(f"Status: `{wd.get('status', 'pending')}`")
                        st.write(f"Date: {wd.get('created_at', 'N/A')[:10]}")
                    with col3:
                        st.write(f"To: `{wd.get('wallet_address', 'N/A')[:20]}...`")
        else:
            st.info("No withdrawals yet")
    else:
        st.info("No withdrawals yet")

# ============================================================================
# Main App
# ============================================================================

def main():
    init_session_state()
    
    # Check if logged in
    if not st.session_state.token:
        page_login()
    else:
        # Sidebar navigation
        st.sidebar.title("💼 Navigation")
        page = st.sidebar.radio(
            "Go to",
            ["Dashboard", "Investments", "Deposits", "Withdrawals"]
        )
        
        # Show user in sidebar
        if st.session_state.user:
            st.sidebar.markdown("---")
            st.sidebar.write(f"**{st.session_state.user.get('email')}**")
            if st.sidebar.button("🚪 Logout"):
                clear_auth()
        
        # Route to page
        if page == "Dashboard":
            page_dashboard()
        elif page == "Investments":
            page_investments()
        elif page == "Deposits":
            page_deposits()
        elif page == "Withdrawals":
            page_withdrawals()

if __name__ == "__main__":
    main()
