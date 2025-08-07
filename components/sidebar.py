"""
Sidebar navigation component
"""
import streamlit as st
from config import Config

def create_sidebar():
    """Create and return the sidebar navigation"""
    
    with st.sidebar:
        st.title("📈 Portfolio Manager")
        st.markdown("---")
        
        # Navigation buttons
        modules = {
            "📊 Dashboard": "Dashboard",
            "💼 Portfolio": "Portfolio", 
            "📈 Reports": "Reports",
            "📁 Data Import": "Data Import"
        }
        
        selected_page = None
        
        for display_name, page_name in modules.items():
            if st.button(
                display_name, 
                key=f"nav_{page_name}",
                use_container_width=True,
                type="primary" if st.session_state.get('current_page') == page_name else "secondary"
            ):
                selected_page = page_name
        
        # If no button was clicked, use current page or default
        if selected_page is None:
            selected_page = st.session_state.get('current_page', 'Dashboard')
        
        st.markdown("---")
        
        # System info
        st.subheader("⚙️ System Info")
        
        # Database status
        try:
            from database.database import db_manager
            if db_manager.engine:
                st.success("🟢 Database Connected")
                st.caption(f"Path: {Config.DATABASE_PATH}")
            else:
                st.error("🔴 Database Disconnected")
        except Exception as e:
            st.error("🔴 Database Error")
            st.caption(str(e))
        
        # Configuration info
        st.caption(f"Date Format: {Config.DATE_FORMAT_DISPLAY}")
        st.caption(f"Default Currency: {Config.DEFAULT_CURRENCY}")
        
        st.markdown("---")
        st.caption("Portfolio Manager v1.0")
        
    return selected_page