"""
Portfolio page with Securities, Transactions, Accounts, and Configuration tabs
"""
import streamlit as st
import pandas as pd
import logging
from datetime import datetime
from database.models import Account, Owner, Institution, AccountType
from database.database import db_manager
from config import Config

logger = logging.getLogger(__name__)

def show_portfolio_page():
    st.title("💼 Portfolio")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "🏦 Accounts", 
        "📈 Securities", 
        "🧾 Transactions", 
        "⚙️ Configuration"
    ])
    
    with tab1:
        show_accounts_tab()        
    
    with tab2:
        show_securities_tab()
   
    with tab3:
        show_transactions_tab()
    
    with tab4:
        show_configuration_tab()

def show_securities_tab():
#    st.subheader("Securities Management")
    st.info("Securities functionality will be implemented in Phase 2")

def show_transactions_tab():
#    st.subheader("Transaction Management")
    st.info("Transaction functionality will be implemented in Phase 2")

def show_accounts_tab():
#    st.subheader("Account Management")
       
    display_accounts_table()
    
    with st.expander("➕ Add New Account", expanded=False):
        add_account_form()    
    st.markdown("---")
    csv_import_export_section()

def show_configuration_tab():
    st.subheader("System Configuration")
    st.info("Configuration functionality will be implemented in Phase 2")

def add_account_form():
    try:
        session = db_manager.get_session()
        
        owners = session.query(Owner).all()
        account_types = session.query(AccountType).all()
        
        with st.form("add_account_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                owner_options = {owner.owner_name: owner.owner_id for owner in owners}
                selected_owner = st.selectbox("Owner*", options=list(owner_options.keys()))
                
                institution_name = st.text_input("Institution*")
            
            with col2:
                account_number = st.text_input("Account Number", placeholder="Optional")
                account_type_options = {at.type_name: at.account_type_id for at in account_types}
                selected_account_type = st.selectbox("Account Type*", options=list(account_type_options.keys()))
            
            submitted = st.form_submit_button("Add Account", type="primary")
            
            if submitted:
                if selected_owner and institution_name and selected_account_type:
                    try:
                        institution = get_or_create_institution(session, institution_name)
                        new_account = Account(
                            account_number=account_number if account_number else None,
                            owner_id=owner_options[selected_owner],
                            institution_id=institution.institution_id,
                            account_type_id=account_type_options[selected_account_type]
                        )
                        session.add(new_account)
                        session.commit()
                        st.success("Account added successfully!")
                        st.rerun()
                        
                    except Exception as e:
                        session.rollback()
                        st.error(f"Error adding account: {str(e)}")
                        logger.error(f"Error adding account: {e}")
                else:
                    st.error("Please fill in all required fields (marked with *)")
    
    except Exception as e:
        st.error(f"Error loading form data: {str(e)}")
        logger.error(f"Error loading add account form: {e}")
    finally:
        session.close()

def display_accounts_table():
    """Display accounts in a simple table"""
    try:
        session = db_manager.get_session()
        
        accounts_query = (
            session.query(
                Owner.owner_name,
                Institution.institution_name,
                AccountType.type_name
            )
            .select_from(Account)
            .join(Owner, Account.owner_id == Owner.owner_id)
            .join(Institution, Account.institution_id == Institution.institution_id)
            .join(AccountType, Account.account_type_id == AccountType.account_type_id)
            .all()
        )
        
        if not accounts_query:
            st.info("No accounts found. Add your first account above.")
            return
        
        df = pd.DataFrame(accounts_query, columns=['Owner', 'Institution', 'Account Type'])
        df['Balance'] = None  # Placeholder until calculation from transactions
        
        st.subheader(f"🏦 Accounts ({len(df)})")
        st.dataframe(df, use_container_width=True)
    
    except Exception as e:
        st.error(f"Error loading accounts: {str(e)}")
        logger.error(f"Error displaying accounts table: {e}")
    finally:
        session.close()

def csv_import_export_section():
    st.subheader("📁 CSV Import/Export")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📤 Export Accounts**")
        if st.button("Download Accounts CSV", type="secondary"):
            export_accounts_csv()
    
    with col2:
        st.markdown("**📥 Import Accounts**")
        uploaded_file = st.file_uploader(
            "Upload Accounts CSV",
            type=['csv'],
            help="CSV format: OwnerName,InstitutionName,AccountTypeName"
        )
        
        if uploaded_file is not None:
            import_accounts_csv(uploaded_file)

def export_accounts_csv():
    try:
        session = db_manager.get_session()
        
        accounts_query = (
            session.query(
                Owner.owner_name,
                Institution.institution_name,
                AccountType.type_name
            )
            .select_from(Account)
            .join(Owner, Account.owner_id == Owner.owner_id)
            .join(Institution, Account.institution_id == Institution.institution_id)
            .join(AccountType, Account.account_type_id == AccountType.account_type_id)
            .all()
        )
        
        if not accounts_query:
            st.warning("No accounts to export")
            return
        
        df = pd.DataFrame(accounts_query, columns=['OwnerName', 'InstitutionName', 'AccountTypeName'])
        csv_data = df.to_csv(index=False)
        
        st.download_button(
            label="📥 Download accounts.csv",
            data=csv_data,
            file_name=f"accounts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
        
        st.success(f"Prepared {len(df)} accounts for download")
        
    except Exception as e:
        st.error(f"Error exporting accounts: {str(e)}")
        logger.error(f"Error exporting accounts CSV: {e}")
    finally:
        session.close()

def import_accounts_csv(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file)
        required_columns = ['OwnerName', 'InstitutionName', 'AccountTypeName']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            st.error(f"Missing required columns: {', '.join(missing_columns)}")
            return
        
        st.subheader("Preview Import Data")
        st.dataframe(df)
        
        if st.button("Confirm Import", type="primary"):
            session = db_manager.get_session()
            success_count, error_count = 0, 0
            errors = []
            
            for idx, row in df.iterrows():
                try:
                    owner = get_or_create_owner(session, row['OwnerName'])
                    institution = get_or_create_institution(session, row['InstitutionName'])
                    account_type = get_or_create_account_type(session, row['AccountTypeName'])
                    
                    account = Account(
                        owner_id=owner.owner_id,
                        institution_id=institution.institution_id,
                        account_type_id=account_type.account_type_id
                    )
                    session.add(account)
                    success_count += 1
                    
                except Exception as e:
                    error_count += 1
                    errors.append(f"Row {idx + 1}: {str(e)}")
                    continue
            
            try:
                session.commit()
                st.success(f"Imported {success_count} accounts successfully!")
                if error_count > 0:
                    st.warning(f"{error_count} accounts failed to import:")
                    for error in errors:
                        st.write(f"• {error}")
                st.rerun()
            except Exception as e:
                session.rollback()
                st.error(f"Failed to save accounts: {str(e)}")
    
    except Exception as e:
        st.error(f"Error importing CSV: {str(e)}")
        logger.error(f"Error importing accounts CSV: {e}")

def get_or_create_owner(session, owner_name):
    owner = session.query(Owner).filter(Owner.owner_name == owner_name).first()
    if not owner:
        owner = Owner(owner_name=owner_name)
        session.add(owner)
        session.flush()
    return owner

def get_or_create_institution(session, institution_name):
    institution = session.query(Institution).filter(Institution.institution_name == institution_name).first()
    if not institution:
        institution = Institution(institution_name=institution_name)
        session.add(institution)
        session.flush()
    return institution

def get_or_create_account_type(session, type_name):
    account_type = session.query(AccountType).filter(AccountType.type_name == type_name).first()
    if not account_type:
        account_type = AccountType(type_name=type_name)
        session.add(account_type)
        session.flush()
    return account_type
