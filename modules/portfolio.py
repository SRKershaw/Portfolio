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
    """Display the main portfolio page with tabs"""
    st.title("💼 Portfolio Management")
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🏛️ Securities", 
        "💰 Transactions", 
        "🏦 Accounts", 
        "⚙️ Configuration"
    ])
    
    with tab1:
        show_securities_tab()
    
    with tab2:
        show_transactions_tab()
    
    with tab3:
        show_accounts_tab()
    
    with tab4:
        show_configuration_tab()

def show_securities_tab():
    """Securities management tab (stubbed for now)"""
    st.subheader("Securities Management")
    st.info("Securities functionality will be implemented in Phase 2")
    
    # Sub-tabs for Funds and Bonds
    funds_tab, bonds_tab = st.tabs(["📈 Funds", "🏛️ Bonds/Gilts"])
    
    with funds_tab:
        st.write("Fund management features:")
        st.write("- Add/edit equity funds, ETFs")
        st.write("- View current prices from yfinance")
        st.write("- Manage fund watchlist")
    
    with bonds_tab:
        st.write("Bond/Gilt management features:")
        st.write("- Add individual bonds with maturity dates")
        st.write("- Track coupon payments")
        st.write("- Bond ladder visualization")

def show_transactions_tab():
    """Transactions management tab (stubbed for now)"""
    st.subheader("Transaction Management")
    st.info("Transaction functionality will be implemented in Phase 2")
    
    st.write("Transaction features:")
    st.write("- Manual transaction entry")
    st.write("- View transaction history")
    st.write("- Edit/delete transactions")
    st.write("- Multi-currency support")

def show_accounts_tab():
    """Fully functional accounts management tab"""
    st.subheader("Account Management")
    
    # Add new account section
    with st.expander("➕ Add New Account", expanded=False):
        add_account_form()
    
    # Display existing accounts
    display_accounts_table()
    
    # CSV import/export section
    st.markdown("---")
    csv_import_export_section()

def show_configuration_tab():
    """Configuration management tab (stubbed for now)"""
    st.subheader("System Configuration")
    st.info("Configuration functionality will be implemented in Phase 2")
    
    st.write("Configuration options:")
    st.write("- Database path settings")
    st.write("- Date format preferences")
    st.write("- Default currency settings")
    st.write("- yfinance update frequency")

def add_account_form():
    """Form to add a new account"""
    try:
        session = db_manager.get_session()
        
        # Get lookup data
        owners = session.query(Owner).all()
        institutions = session.query(Institution).all()
        account_types = session.query(AccountType).all()
        
        with st.form("add_account_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                account_name = st.text_input("Account Name*", placeholder="e.g., My SIPP")
                account_number = st.text_input("Account Number", placeholder="Optional")
                
            with col2:
                owner_options = {owner.owner_name: owner.owner_id for owner in owners}
                selected_owner = st.selectbox("Owner*", options=list(owner_options.keys()))
                
                institution_options = {inst.institution_name: inst.institution_id for inst in institutions}
                selected_institution = st.selectbox("Institution*", options=list(institution_options.keys()))
                
                account_type_options = {at.type_name: at.account_type_id for at in account_types}
                selected_account_type = st.selectbox("Account Type*", options=list(account_type_options.keys()))
            
            submitted = st.form_submit_button("Add Account", type="primary")
            
            if submitted:
                if account_name and selected_owner and selected_institution and selected_account_type:
                    try:
                        new_account = Account(
                            account_name=account_name,
                            account_number=account_number if account_number else None,
                            owner_id=owner_options[selected_owner],
                            institution_id=institution_options[selected_institution],
                            account_type_id=account_type_options[selected_account_type]
                        )
                        
                        session.add(new_account)
                        session.commit()
                        st.success(f"Account '{account_name}' added successfully!")
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
    """Display accounts in an editable table"""
    try:
        session = db_manager.get_session()
        
        # Query accounts with related data
        accounts_query = session.query(
            Account.account_id,
            Account.account_name,
            Account.account_number,
            Owner.owner_name,
            Institution.institution_name,
            AccountType.type_name
        ).join(Owner).join(Institution).join(AccountType).all()
        
        if not accounts_query:
            st.info("No accounts found. Add your first account above.")
            return
        
        # Convert to DataFrame
        df = pd.DataFrame(accounts_query, columns=[
            'ID', 'Account Name', 'Account Number', 'Owner', 'Institution', 'Account Type'
        ])
        
        # Display the table
        st.subheader(f"📋 Accounts ({len(df)})")
        
        # Add edit/delete functionality
        with st.container():
            for idx, row in df.iterrows():
                col1, col2, col3 = st.columns([6, 1, 1])
                
                with col1:
                    account_info = f"**{row['Account Name']}** ({row['Owner']}) - {row['Institution']} - {row['Account Type']}"
                    if row['Account Number']:
                        account_info += f" - #{row['Account Number']}"
                    st.write(account_info)
                
                with col2:
                    if st.button("✏️", key=f"edit_{row['ID']}", help="Edit account"):
                        st.session_state[f"editing_{row['ID']}"] = True
                        st.rerun()
                
                with col3:
                    if st.button("🗑️", key=f"delete_{row['ID']}", help="Delete account"):
                        if delete_account(row['ID'], row['Account Name']):
                            st.rerun()
                
                # Edit form (if editing)
                if st.session_state.get(f"editing_{row['ID']}", False):
                    edit_account_form(row['ID'], row)
                
                st.divider()
    
    except Exception as e:
        st.error(f"Error loading accounts: {str(e)}")
        logger.error(f"Error displaying accounts table: {e}")
    finally:
        session.close()

def edit_account_form(account_id, current_data):
    """Form to edit an existing account"""
    try:
        session = db_manager.get_session()
        
        # Get lookup data
        owners = session.query(Owner).all()
        institutions = session.query(Institution).all()
        account_types = session.query(AccountType).all()
        
        with st.form(f"edit_account_form_{account_id}"):
            st.subheader(f"Edit Account: {current_data['Account Name']}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                new_name = st.text_input("Account Name", value=current_data['Account Name'])
                new_number = st.text_input("Account Number", value=current_data['Account Number'] or "")
                
            with col2:
                owner_options = {owner.owner_name: owner.owner_id for owner in owners}
                current_owner_idx = list(owner_options.keys()).index(current_data['Owner'])
                new_owner = st.selectbox("Owner", options=list(owner_options.keys()), index=current_owner_idx)
                
                institution_options = {inst.institution_name: inst.institution_id for inst in institutions}
                current_inst_idx = list(institution_options.keys()).index(current_data['Institution'])
                new_institution = st.selectbox("Institution", options=list(institution_options.keys()), index=current_inst_idx)
                
                account_type_options = {at.type_name: at.account_type_id for at in account_types}
                current_type_idx = list(account_type_options.keys()).index(current_data['Account Type'])
                new_account_type = st.selectbox("Account Type", options=list(account_type_options.keys()), index=current_type_idx)
            
            col_save, col_cancel = st.columns(2)
            
            with col_save:
                save_clicked = st.form_submit_button("💾 Save Changes", type="primary")
            
            with col_cancel:
                cancel_clicked = st.form_submit_button("❌ Cancel")
            
            if save_clicked:
                if new_name:
                    try:
                        account = session.query(Account).filter(Account.account_id == account_id).first()
                        if account:
                            account.account_name = new_name
                            account.account_number = new_number if new_number else None
                            account.owner_id = owner_options[new_owner]
                            account.institution_id = institution_options[new_institution]
                            account.account_type_id = account_type_options[new_account_type]
                            
                            session.commit()
                            st.success("Account updated successfully!")
                            st.session_state[f"editing_{account_id}"] = False
                            st.rerun()
                        else:
                            st.error("Account not found")
                    except Exception as e:
                        session.rollback()
                        st.error(f"Error updating account: {str(e)}")
                        logger.error(f"Error updating account {account_id}: {e}")
                else:
                    st.error("Account name is required")
            
            if cancel_clicked:
                st.session_state[f"editing_{account_id}"] = False
                st.rerun()
    
    except Exception as e:
        st.error(f"Error loading edit form: {str(e)}")
        logger.error(f"Error in edit account form: {e}")
    finally:
        session.close()

def delete_account(account_id, account_name):
    """Delete an account with confirmation"""
    try:
        # Check if account has transactions
        session = db_manager.get_session()
        from database.models import Transaction
        
        transaction_count = session.query(Transaction).filter(Transaction.account_id == account_id).count()
        
        if transaction_count > 0:
            st.error(f"Cannot delete account '{account_name}' - it has {transaction_count} transactions")
            return False
        
        # Confirm deletion
        if st.checkbox(f"Confirm deletion of '{account_name}'", key=f"confirm_delete_{account_id}"):
            account = session.query(Account).filter(Account.account_id == account_id).first()
            if account:
                session.delete(account)
                session.commit()
                st.success(f"Account '{account_name}' deleted successfully!")
                return True
            else:
                st.error("Account not found")
        
        return False
        
    except Exception as e:
        session.rollback()
        st.error(f"Error deleting account: {str(e)}")
        logger.error(f"Error deleting account {account_id}: {e}")
        return False
    finally:
        session.close()

def csv_import_export_section():
    """CSV import and export functionality for accounts"""
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
            help="CSV format: AccountName,AccountNumber,OwnerName,InstitutionName,AccountTypeName"
        )
        
        if uploaded_file is not None:
            import_accounts_csv(uploaded_file)

def export_accounts_csv():
    """Export accounts to CSV"""
    try:
        session = db_manager.get_session()
        
        # Query accounts with related data
        accounts_query = session.query(
            Account.account_name,
            Account.account_number,
            Owner.owner_name,
            Institution.institution_name,
            AccountType.type_name
        ).join(Owner).join(Institution).join(AccountType).all()
        
        if not accounts_query:
            st.warning("No accounts to export")
            return
        
        # Convert to DataFrame
        df = pd.DataFrame(accounts_query, columns=[
            'AccountName', 'AccountNumber', 'OwnerName', 'InstitutionName', 'AccountTypeName'
        ])
        
        # Replace None values with empty strings
        df = df.fillna('')
        
        # Convert to CSV
        csv_data = df.to_csv(index=False)
        
        # Create download button
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
    """Import accounts from CSV"""
    try:
        # Read CSV
        df = pd.read_csv(uploaded_file)
        
        # Validate required columns
        required_columns = ['AccountName', 'OwnerName', 'InstitutionName', 'AccountTypeName']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            st.error(f"Missing required columns: {', '.join(missing_columns)}")
            return
        
        # Show preview
        st.subheader("Preview Import Data")
        st.dataframe(df)
        
        if st.button("Confirm Import", type="primary"):
            session = db_manager.get_session()
            
            success_count = 0
            error_count = 0
            errors = []
            
            for idx, row in df.iterrows():
                try:
                    # Get or create lookup records
                    owner = get_or_create_owner(session, row['OwnerName'])
                    institution = get_or_create_institution(session, row['InstitutionName'])
                    account_type = get_or_create_account_type(session, row['AccountTypeName'])
                    
                    # Create account
                    account = Account(
                        account_name=row['AccountName'],
                        account_number=row.get('AccountNumber') if pd.notna(row.get('AccountNumber')) else None,
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
    """Get existing owner or create new one"""
    owner = session.query(Owner).filter(Owner.owner_name == owner_name).first()
    if not owner:
        owner = Owner(owner_name=owner_name)
        session.add(owner)
        session.flush()  # Get the ID without committing
    return owner

def get_or_create_institution(session, institution_name):
    """Get existing institution or create new one"""
    institution = session.query(Institution).filter(Institution.institution_name == institution_name).first()
    if not institution:
        institution = Institution(institution_name=institution_name)
        session.add(institution)
        session.flush()
    return institution

def get_or_create_account_type(session, type_name):
    """Get existing account type or create new one"""
    account_type = session.query(AccountType).filter(AccountType.type_name == type_name).first()
    if not account_type:
        account_type = AccountType(type_name=type_name)
        session.add(account_type)
        session.flush()
    return account_type