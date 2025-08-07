"""
Portfolio Manager - Main Streamlit Application
"""
import streamlit as st
import logging
from config import Config
from components.sidebar import create_sidebar
from database.database import db_manager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def configure_page():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title=Config.PAGE_TITLE,
        page_icon=Config.PAGE_ICON,
        layout=Config.LAYOUT,
        initial_sidebar_state="expanded"
    )

def initialize_session_state():
    """Initialize session state variables"""
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'Dashboard'
    
    if 'db_manager' not in st.session_state:
        st.session_state.db_manager = db_manager

def load_page(page_name):
    """Load the selected page"""
    try:
        if page_name == 'Dashboard':
            st.title("📊 Portfolio Dashboard")
            st.info("Dashboard functionality will be implemented in Phase 2")
            st.write("This will show:")
            st.write("- Portfolio overview")
            st.write("- Asset allocation by bucket")
            st.write("- Recent transactions")
            st.write("- Performance summary")
            
        elif page_name == 'Portfolio':
            from modules.portfolio import show_portfolio_page
            show_portfolio_page()
            
        elif page_name == 'Reports':
            st.title("📈 Reports & Analytics")
            st.info("Reports functionality will be implemented in Phase 3")
            st.write("This will show:")
            st.write("- Performance analysis")
            st.write("- Asset allocation reports")
            st.write("- Transaction history")
            st.write("- Tax reports")
            
        elif page_name == 'Data Import':
            st.title("📁 Data Import")
            st.info("Bulk data import functionality will be implemented in Phase 3")
            st.write("This will allow:")
            st.write("- CSV import of transactions")
            st.write("- Broker statement processing")
            st.write("- Data validation and cleanup")
            
        else:
            st.error(f"Page '{page_name}' not found")
            
    except Exception as e:
        st.error(f"Error loading page '{page_name}': {str(e)}")
        logging.error(f"Error loading page '{page_name}': {e}")

def main():
    """Main application entry point"""
    try:
        # Configure page
        configure_page()
        
        # Initialize session state
        initialize_session_state()
        
        # Create sidebar navigation
        selected_page = create_sidebar()
        
        # Update current page in session state
        st.session_state.current_page = selected_page
        
        # Load the selected page
        load_page(selected_page)
        
    except Exception as e:
        st.error("An unexpected error occurred. Please check the logs for details.")
        logging.error(f"Application error: {e}")

if __name__ == "__main__":
    main()