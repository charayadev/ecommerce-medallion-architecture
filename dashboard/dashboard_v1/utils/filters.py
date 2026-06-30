import streamlit as st

def multiselect_filter(df, col_name, label):
    """Helper for generating multi-select boxes."""
    options = df[col_name].dropna().unique().tolist()
    selected = st.sidebar.multiselect(label, options, default=options)
    return selected

def apply_filters(df):
    """Renders sidebar filters and returns the filtered dataframe."""
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135692.png", width=100)
    st.sidebar.title("Filters")
    
    selected_regions = multiselect_filter(df, "Region", "Select Region(s)")
    selected_categories = multiselect_filter(df, "Product Category", "Select Category")
    selected_payments = multiselect_filter(df, "Payment Method", "Select Payment Method")
    selected_months = multiselect_filter(df, "Month_Name", "Select Month(s)")

    filtered_df = df[
        (df["Region"].isin(selected_regions)) &
        (df["Product Category"].isin(selected_categories)) &
        (df["Payment Method"].isin(selected_payments)) &
        (df["Month_Name"].isin(selected_months))
    ]
    return filtered_df