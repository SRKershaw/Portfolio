"""
Database connection and initialization
"""
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config
from database.models import Base

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Manages database connection and operations"""
    
    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self._initialize_database()
    
    def _initialize_database(self):
        """Initialize database connection and create tables"""
        try:
            # Create engine
            self.engine = create_engine(
                Config.get_database_url(),
                echo=False,  # Set to True for SQL logging
                connect_args={"check_same_thread": False}  # For SQLite
            )
            
            # Create session factory
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
            
            # Create all tables
            Base.metadata.create_all(bind=self.engine)
            
            # Initialize lookup data
            self._initialize_lookup_data()
            
            logger.info("Database initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise
    
    def _initialize_lookup_data(self):
        """Initialize basic lookup data if not exists"""
        try:
            session = self.get_session()
            
            # Import models here to avoid circular imports
            from database.models import (
                Owner, Institution, AccountType, TransactionType, 
                Bucket, Currency
            )
            
            # Initialize Owners
            if session.query(Owner).count() == 0:
                owners = [
                    Owner(owner_name="Sam"),
                    Owner(owner_name="Barbara"),
                    Owner(owner_name="Joint")
                ]
                session.add_all(owners)
            
            # Initialize Institutions
            if session.query(Institution).count() == 0:
                institutions = [
                    Institution(institution_name="External"),
                    Institution(institution_name="First Direct"),
                    Institution(institution_name="Marcus"),
                    Institution(institution_name="Interactive Investor"),
                    Institution(institution_name="Vanguard"),
                    Institution(institution_name="Hargreaves Lansdown")
                ]
                session.add_all(institutions)
            
            # Initialize Account Types
            if session.query(AccountType).count() == 0:
                account_types = [
                    AccountType(type_name="External"),
                    AccountType(type_name="Current Account"),
                    AccountType(type_name="Savings Account"),
                    AccountType(type_name="SIPP"),
                    AccountType(type_name="ISA"),
                    AccountType(type_name="Trading Account"),
                    AccountType(type_name="Joint Account")
                ]
                session.add_all(account_types)
            
            # Initialize Transaction Types
            if session.query(TransactionType).count() == 0:
                transaction_types = [
                    TransactionType(type_name="Buy"),
                    TransactionType(type_name="Sell"),
                    TransactionType(type_name="Dividend"),
                    TransactionType(type_name="Coupon"),
                    TransactionType(type_name="Interest"),
                    TransactionType(type_name="Fee"),
                    TransactionType(type_name="Transfer")
                ]
                session.add_all(transaction_types)
            
            # Initialize Buckets
            if session.query(Bucket).count() == 0:
                buckets = [
                    Bucket(
                        bucket_name="Growth_Funds",
                        description="Equity funds for long-term growth"
                    ),
                    Bucket(
                        bucket_name="Bond_Ladder",
                        description="Individual bonds and money market funds"
                    ),
                    Bucket(
                        bucket_name="Cash_Reserve",
                        description="Liquid cash holdings"
                    )
                ]
                session.add_all(buckets)
            
            # Initialize Currencies
            if session.query(Currency).count() == 0:
                currencies = [
                    Currency(
                        currency_code="GBP",
                        currency_name="Pounds Sterling",
                        conversion_to_gbp=1.0
                    ),
                    Currency(
                        currency_code="GBp",
                        currency_name="Pence Sterling",
                        conversion_to_gbp=0.01
                    ),
                    Currency(
                        currency_code="USD",
                        currency_name="US Dollar",
                        conversion_to_gbp=0.79  # Approximate - will be updated
                    ),
                    Currency(
                        currency_code="EUR",
                        currency_name="Euro",
                        conversion_to_gbp=0.86  # Approximate - will be updated
                    )
                ]
                session.add_all(currencies)
            
            session.commit()
            logger.info("Lookup data initialized successfully")
            
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to initialize lookup data: {e}")
            raise
        finally:
            session.close()
    
    def get_session(self):
        """Get a new database session"""
        if self.SessionLocal is None:
            raise RuntimeError("Database not initialized")
        return self.SessionLocal()
    
    def close(self):
        """Close database connection"""
        if self.engine:
            self.engine.dispose()

# Global database manager instance
db_manager = DatabaseManager()