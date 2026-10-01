import pandas as pd
import streamlit as st

# Page configuration for mobile responsiveness
st.set_page_config(
    page_title="Mera Mitwa", page_icon="🤝", layout="centered", initial_sidebar_state="expanded"
)

# Initialize session state for mock database / data storage
if "members_df" not in st.session_state:
    # Default mock member data
    st.session_state.members_df = pd.DataFrame(
        {
            "Member_ID": ["M001", "M002", "M003", "M004", "M005"],
            "Name": [
                "Rahul Sharma",
                "Priya Patel",
                "Amit Kumar",
                "Sneha Gupta",
                "Vikram Singh",
            ],
            "Area": ["North", "South", "North", "East", "South"],
            "Status": ["Active", "Inactive", "Active", "Active", "Inactive"],
        }
    )

if "schemes_df" not in st.session_state:
    # Default mock scheme data
    st.session_state.schemes_df = pd.DataFrame(
        {
            "Scheme_ID": ["S01", "S02", "S03"],
            "Scheme_Name": ["Mitwa Health", "Mitwa Education", "Mitwa Welfare"],
            "Area": ["North", "South", "East"],
            "Status": ["Active", "Active", "Inactive"],
        }
    )

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = None
    st.session_state.area = None


# Helper function to style inactive rows in bold red
def highlight_inactive(row):
    if str(row["Status"]).strip().lower() == "inactive":
        return ["font-weight: bold; color: red;"] * len(row)
    return [""] * len(row)


# --- LOGIN SCREEN ---
if not st.session_state.logged_in:
    # Try loading logo if available
    try:
        st.image("logo.png", width=120)
    except Exception:
        pass

    st.title("🤝 Mera Mitwa Login")
    st.markdown("Please sign in to access your dashboard.")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_btn = st.form_submit_button("Login")

        if submit_btn:
            if username == "admin" and password == "admin123":
                st.session_state.logged_in = True
                st.session_state.role = "Admin"
                st.session_state.username = "admin"
                st.success("Login Successful!")
                st.rerun()
            elif username.startswith("msr") and password == "admin123":
                st.session_state.logged_in = True
                st.session_state.role = "MSR"
                st.session_state.username = username
                # Assign mock areas based on username for demo
                st.session_state.area = (
                    "North" if "1" in username else "South"
                )
                st.success("Login Successful!")
                st.rerun()
            else:
                st.error("Invalid Username or Password. Try admin / admin123")

else:
    # --- LOGOUT & SIDEBAR ---
    with st.sidebar:
        try:
            st.image("logo.png", width=100)
        except Exception:
            pass

        st.write(f"**User:** {st.session_state.username}")
        st.write(f"**Role:** {st.session_state.role}")
        if st.session_state.role == "MSR":
            st.write(f"**Assigned Area:** {st.session_state.area}")

        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.role = None
            st.session_state.username = None
            st.session_state.area = None
            st.rerun()

    # --- DASHBOARD LOGIC ---
    st.title("📊 Mera Mitwa Dashboard")

    # Data Refresh Button
    if st.button("🔄 Refresh Data"):
        st.success("Data refreshed successfully!")

    # Role: ADMIN
    if st.session_state.role == "Admin":
        st.subheader("Admin Control Panel & File Uploads")

        col_u1, col_u2 = st.columns(2)
        with col_u1:
            member_file = st.file_uploader(
                "Upload Member Data (CSV/XLSX)", type=["csv", "xlsx"]
            )
            if member_file is not None:
                try:
                    if member_file.name.endswith(".csv"):
                        st.session_state.members_df = pd.read_csv(member_file)
                    else:
                        st.session_state.members_df = pd.read_excel(
                            member_file
                        )
                    st.success("Member data updated successfully!")
                except Exception as e:
                    st.error(f"Error reading file: {e}")

        with col_u2:
            scheme_file = st.file_uploader(
                "Upload Scheme File (CSV/XLSX)", type=["csv", "xlsx"]
            )
            if scheme_file is not None:
                try:
                    if scheme_file.name.endswith(".csv"):
                        st.session_state.schemes_df = pd.read_csv(scheme_file)
                    else:
                        st.session_state.schemes_df = pd.read_excel(
                            scheme_file
                        )
                    st.success("Scheme data imported successfully!")
                except Exception as e:
                    st.error(f"Error reading file: {e}")

        st.markdown("---")

        # Global Metrics
        df_m = st.session_state.members_df
        total_m = len(df_m)
        active_m = len(
            df_m[df_m["Status"].astype(str).str.lower() == "active"]
        )
        inactive_m = len(
            df_m[df_m["Status"].astype(str).str.lower() == "inactive"]
        )
        active_pct = (active_m / total_m * 100) if total_m > 0 else 0

        st.markdown("### 📈 All-Area Member Summary Metrics")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Members", total_m)
        m2.metric("Active Members", active_m)
        m3.metric("Inactive Members", inactive_m)
        m4.metric("Active %", f"{active_pct:.1f}%")

        st.markdown("---")

        # Universal Filters for Admin
        st.markdown("### 🔍 Universal Filters")
        areas = ["All"] + list(df_m["Area"].dropna().unique())
        selected_area = st.selectbox("Filter by Area", areas)

        filtered_members = df_m
        if selected_area != "All":
            filtered_members = df_m[df_m["Area"] == selected_area]

        st.markdown("### 👥 Member Records Management")
        st.dataframe(
            filtered_members.style.apply(highlight_inactive, axis=1),
            use_container_width=True,
        )

        st.markdown("### 📁 Scheme Records Management")
        df_s = st.session_state.schemes_df
        filtered_schemes = df_s
        if selected_area != "All" and "Area" in df_s.columns:
            filtered_schemes = df_s[df_s["Area"] == selected_area]
        st.dataframe(filtered_schemes, use_container_width=True)

    # Role: MSR
    elif st.session_state.role == "MSR":
        assigned_area = st.session_state.area
        st.subheader(f"📍 MSR Portal - Area: {assigned_area}")

        df_m = st.session_state.members_df
        # Filter for MSR's specific area
        area_members = df_m[df_m["Area"] == assigned_area]

        total_m = len(area_members)
        active_m = len(
            area_members[
                area_members["Status"].astype(str).str.lower() == "active"
            ]
        )
        inactive_m = len(
            area_members[
                area_members["Status"].astype(str).str.lower() == "inactive"
            ]
        )
        active_pct = (active_m / total_m * 100) if total_m > 0 else 0

        st.markdown(f"### 📈 {assigned_area} Area Dashboard Metrics")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Members", total_m)
        m2.metric("Active Members", active_m)
        m3.metric("Inactive Members", inactive_m)
        m4.metric("Active %", f"{active_pct:.1f}%")

        st.markdown("---")
        st.markdown("### 👥 Area Member Records")
        st.dataframe(
            area_members.style.apply(highlight_inactive, axis=1),
            use_container_width=True,
        )

        st.markdown("### 📁 Area Scheme Records")
        df_s = st.session_state.schemes_df
        if "Area" in df_s.columns:
            area_schemes = df_s[df_s["Area"] == assigned_area]
        else:
            area_schemes = df_s
        st.dataframe(area_schemes, use_container_width=True)
