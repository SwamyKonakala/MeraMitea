import pandas as pd
import streamlit as st
import plotly.express as px
import os

# Page configuration
st.set_page_config(
    page_title="MERA MITWA Multi-Role Portal & Analytics Dashboard",
    page_icon="🚗",
    layout="wide"
)

DEFAULT_FILE = "1st OCT.xlsx"
UPLOADED_FILE = "uploaded_latest_data.xlsx"

BONUS_DEFAULT_FILE = "Bonus Points(1).xlsx"
BONUS_UPLOADED_FILE = "uploaded_bonus_data.xlsx"

LOGO_FILE = "app_logo.jpg"

@st.cache_data
def load_data(file_path, file_mod_time):
    try:
        if os.path.exists(file_path):
            df = pd.read_excel(file_path, sheet_name="Export")
            return df
    except Exception as e:
        st.error(f"Error reading member file: {e}")
    return None

@st.cache_data
def load_bonus_data(file_path, file_mod_time):
    try:
        if os.path.exists(file_path):
            xls = pd.ExcelFile(file_path)
            sheet = xls.sheet_names[0]
            df = pd.read_excel(file_path, sheet_name=sheet)
            return df
    except Exception as e:
        st.error(f"Error reading bonus file: {e}")
    return None

active_file = UPLOADED_FILE if os.path.exists(UPLOADED_FILE) else DEFAULT_FILE
file_mod_time = os.path.getmtime(active_file) if os.path.exists(active_file) else 0
df = load_data(active_file, file_mod_time)

active_bonus_file = BONUS_UPLOADED_FILE if os.path.exists(BONUS_UPLOADED_FILE) else BONUS_DEFAULT_FILE
bonus_mod_time = os.path.getmtime(active_bonus_file) if os.path.exists(active_bonus_file) else 0
bonus_df = load_bonus_data(active_bonus_file, bonus_mod_time)

if df is None or df.empty:
    df = pd.DataFrame()

if bonus_df is None:
    bonus_df = pd.DataFrame()

if 'users_db' not in st.session_state:
    st.session_state['users_db'] = {
        "admin": ["mitwa2026", "Admin", "All"],
        "east_mgr": ["east123", "Area", "EAST"],
        "rjy_mgr": ["rjy123", "Area", "RJY"],
        "sklm_mgr": ["sklm123", "Area", "SKLM"],
        "vsp1_mgr": ["vsp1123", "Area", "VSP1"],
        "vsp2_mgr": ["vsp2123", "Area", "VSP2"],
        "vzm_mgr": ["vzm123", "Area", "VZM"],
        "west_mgr": ["west123", "Area", "WEST"],
        "M00022760": ["pass123", "Member", "M00022760"]
    }

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'current_user' not in st.session_state:
    st.session_state['current_user'] = None
if 'current_role' not in st.session_state:
    st.session_state['current_role'] = None
if 'user_scope' not in st.session_state:
    st.session_state['user_scope'] = None

if os.path.exists(LOGO_FILE):
    st.sidebar.image(LOGO_FILE, use_column_width=True)

st.sidebar.title("🔐 MERA MITWA Portal")

if st.sidebar.button("🔄 Refresh Data / Clear Cache"):
    st.cache_data.clear()
    st.sidebar.success("Cache cleared & data reloaded!")
    st.rerun()

st.sidebar.markdown("---")

if not st.session_state['authenticated']:
    st.sidebar.subheader("Please Login")
    login_user = st.sidebar.text_input("Username / MITWA ID / Mobile")
    login_pass = st.sidebar.text_input("Password", type="password")
    
    if st.sidebar.button("Login"):
        users = st.session_state['users_db']
        if login_user in users and users[login_user][0] == login_pass:
            st.session_state['authenticated'] = True
            st.session_state['current_user'] = login_user
            st.session_state['current_role'] = users[login_user][1]
            st.session_state['user_scope'] = users[login_user][2]
            st.sidebar.success("Logged in successfully!")
            st.rerun()
        else:
            st.sidebar.error("Invalid username or password.")
else:
    st.sidebar.success(f"Logged in as: **{st.session_state['current_user']}** ({st.session_state['current_role']})")
    if st.sidebar.button("Logout"):
        st.session_state['authenticated'] = False
        st.session_state['current_user'] = None
        st.session_state['current_role'] = None
        st.session_state['user_scope'] = None
        st.rerun()

def highlight_inactive(row):
    status_col = '30Is MITWA Active'
    if status_col in row and str(row[status_col]).strip().lower() == 'inactive':
        return ['color: #d9534f; font-weight: bold; background-color: #f2dede'] * len(row)
    return [''] * len(row)

if not st.session_state['authenticated']:
    st.title("🚗 MERA MITWA Member Performance Portal")
    st.info("Please log in using your assigned credentials from the sidebar to view your dashboard.")
    
    if not df.empty:
        st.markdown("### 📊 Program Overview Summary")
        tot_m = len(df)
        act_m = len(df[df['30Is MITWA Active'] == 'Active']) if '30Is MITWA Active' in df.columns else 0
        inact_m = len(df[df['30Is MITWA Active'] == 'Inactive']) if '30Is MITWA Active' in df.columns else 0
        act_pct = (act_m / tot_m) * 100 if tot_m > 0 else 0
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Members", f"{tot_m:,}")
        col2.metric("Active Members", f"{act_m:,}")
        col3.metric("Inactive Members", f"{inact_m:,}")
        col4.metric("Active Percentage", f"{act_pct:.1f}%")

else:
    role = st.session_state['current_role']
    scope = st.session_state['user_scope']

    if role == "Admin":
        st.title("🛠️ Admin Dashboard & Data Management")
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Global Analytics", "🎁 Bonus Schemes", "📤 Upload & Refresh", "🔑 Passwords"])
        
        with tab1:
            st.subheader("Global Performance Metrics Across All Areas")
            if not df.empty:
                tot = len(df)
                act = len(df[df['30Is MITWA Active'] == 'Active'])
                inact = len(df[df['30Is MITWA Active'] == 'Inactive'])
                act_rate = (act / tot) * 100 if tot > 0 else 0
                
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Total Members", f"{tot:,}")
                c2.metric("Active Members", f"{act:,}")
                c3.metric("Inactive Members", f"{inact:,}")
                c4.metric("Active Percentage", f"{act_rate:.1f}%")
                
                st.markdown("---")
                st.subheader("🔍 Universal Search")
                search_term = st.text_input("Search Members & Parts", "")
                view_df = df.copy()
                if search_term:
                    q = search_term.lower()
                    view_df = view_df[
                        view_df['Name'].astype(str).str.lower().str.contains(q, na=False) |
                        view_df['MITWA ID'].astype(str).str.lower().str.contains(q, na=False) |
                        view_df['Mobile Number'].astype(str).str.lower().str.contains(q, na=False) |
                        view_df['Shop Name'].astype(str).str.lower().str.contains(q, na=False) |
                        view_df['Area'].astype(str).str.lower().str.contains(q, na=False) |
                        view_df['30Is MITWA Active'].astype(str).str.lower().str.contains(q, na=False)
                    ]
                st.dataframe(view_df.style.apply(highlight_inactive, axis=1), use_container_width=True)

        with tab2:
            st.subheader("🎁 Bonus Points Catalog")
            if not bonus_df.empty:
                st.dataframe(bonus_df, use_container_width=True)

        with tab3:
            st.subheader("📤 Data Upload")
            uploaded_file = st.file_uploader("Member Excel File", type=["xlsx", "xls"])
            if uploaded_file is not None:
                with open(UPLOADED_FILE, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.cache_data.clear()
                st.success("Uploaded successfully!")
                st.rerun()

        with tab4:
            st.subheader("Password Manager")
            users = st.session_state['users_db']
            sel = st.selectbox("Select User", options=list(users.keys()))
            npw = st.text_input("New Password", type="password")
            if st.button("Update"):
                users[sel][0] = npw
                st.success("Updated successfully!")

    elif role == "Area":
        st.title(f"📍 Area Manager Dashboard — {scope}")
        area_df = df[df['Area'] == scope].copy() if 'Area' in df.columns else pd.DataFrame()
        st.dataframe(area_df.style.apply(highlight_inactive, axis=1), use_container_width=True)

    elif role == "Member":
        st.title("👨‍🔧 Member Dashboard")
        m_rec = df[df['MITWA ID'] == scope] if 'MITWA ID' in df.columns else pd.DataFrame()
        if not m_rec.empty:
            st.json(m_rec.iloc[0].to_dict())
