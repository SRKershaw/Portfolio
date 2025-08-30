"""
SQLAlchemy models for Portfolio Manager
"""
from sqlalchemy import Column, Integer, String, DateTime, Date, Boolean, ForeignKey, BigInteger, Text, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from decimal import Decimal

Base = declarative_base()

class Owner(Base):
    __tablename__ = 'owners'
    
    owner_id = Column(Integer, primary_key=True)
    owner_name = Column(String(100), nullable=False)
    
    # Relationships
    accounts = relationship("Account", back_populates="owner")
    transactions = relationship("Transaction", back_populates="owner")

class Institution(Base):
    __tablename__ = 'institutions'
    
    institution_id = Column(Integer, primary_key=True)
    institution_name = Column(String(100), nullable=False)
    
    # Relationships
    accounts = relationship("Account", back_populates="institution")
    transactions = relationship("Transaction", back_populates="institution")

class AccountType(Base):
    __tablename__ = 'account_types'
    
    account_type_id = Column(Integer, primary_key=True)
    type_name = Column(String(50), nullable=False)
    
    # Relationships
    accounts = relationship("Account", back_populates="account_type")

class TransactionType(Base):
    __tablename__ = 'transaction_types'
    
    transaction_type_id = Column(Integer, primary_key=True)
    type_name = Column(String(50), nullable=False)
    
    # Relationships
    transactions = relationship("Transaction", back_populates="transaction_type")

class Bucket(Base):
    __tablename__ = 'buckets'
    
    bucket_id = Column(Integer, primary_key=True)
    bucket_name = Column(String(100), nullable=False)
    description = Column(Text)
    
    # Relationships
    transactions = relationship("Transaction", back_populates="bucket")

class Currency(Base):
    __tablename__ = 'currencies'
    
    currency_id = Column(Integer, primary_key=True)
    currency_code = Column(String(10), nullable=False, unique=True)
    currency_name = Column(String(100), nullable=False)
    conversion_to_gbp = Column(Numeric(10, 6), nullable=False, default=1.0)
    
    # Relationships
    securities = relationship("Security", back_populates="currency")
    transactions = relationship("Transaction", back_populates="currency")

class Account(Base):
    __tablename__ = 'accounts'
    
    account_id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('owners.owner_id'), nullable=False)
    institution_id = Column(Integer, ForeignKey('institutions.institution_id'), nullable=False)
    account_type_id = Column(Integer, ForeignKey('account_types.account_type_id'), nullable=False)
    account_number = Column(String(50))
 #   account_name = Column(String(200), nullable=False)
    
    # Relationships
    owner = relationship("Owner", back_populates="accounts")
    institution = relationship("Institution", back_populates="accounts")
    account_type = relationship("AccountType", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account")
    transfers_from = relationship("Transfer", foreign_keys="Transfer.from_account_id", back_populates="from_account")
    transfers_to = relationship("Transfer", foreign_keys="Transfer.to_account_id", back_populates="to_account")

class Security(Base):
    __tablename__ = 'securities'
    
    security_id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    ticker = Column(String(50), nullable=False)
    asset_class = Column(String(50), nullable=False)
    currency_id = Column(Integer, ForeignKey('currencies.currency_id'), nullable=False)
    maturity_date = Column(Date)  # NULL for funds
    coupon_rate = Column(Numeric(5, 3))  # Annual percentage for bonds
    coupon_frequency = Column(Integer)  # Payments per year
    last_coupon_date = Column(Date)
    next_coupon_date = Column(Date)
    
    # Relationships
    currency = relationship("Currency", back_populates="securities")
    security_prices = relationship("SecurityPrice", back_populates="security")
    trades = relationship("Trade", back_populates="security")
    incomes = relationship("Income", back_populates="security")

class SecurityPrice(Base):
    __tablename__ = 'security_prices'
    
    price_id = Column(Integer, primary_key=True)
    security_id = Column(Integer, ForeignKey('securities.security_id'), nullable=False)
    price_date = Column(Date, nullable=False)
    open_price = Column(Numeric(10, 4))
    high_price = Column(Numeric(10, 4))
    low_price = Column(Numeric(10, 4))
    close_price = Column(Numeric(10, 4), nullable=False)
    volume = Column(BigInteger)
    last_updated = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    security = relationship("Security", back_populates="security_prices")

class Transaction(Base):
    __tablename__ = 'transactions'
    
    transaction_id = Column(Integer, primary_key=True)
    transaction_type_id = Column(Integer, ForeignKey('transaction_types.transaction_type_id'), nullable=False)
    owner_id = Column(Integer, ForeignKey('owners.owner_id'), nullable=False)
    institution_id = Column(Integer, ForeignKey('institutions.institution_id'), nullable=False)
    account_id = Column(Integer, ForeignKey('accounts.account_id'), nullable=False)
    bucket_id = Column(Integer, ForeignKey('buckets.bucket_id'))
    currency_id = Column(Integer, ForeignKey('currencies.currency_id'), nullable=False)
    exchange_rate = Column(Numeric(10, 6), nullable=False, default=1.0)
    transaction_date = Column(DateTime, nullable=False)
    description = Column(Text)
    
    # Relationships
    transaction_type = relationship("TransactionType", back_populates="transactions")
    owner = relationship("Owner", back_populates="transactions")
    institution = relationship("Institution", back_populates="transactions")
    account = relationship("Account", back_populates="transactions")
    bucket = relationship("Bucket", back_populates="transactions")
    currency = relationship("Currency", back_populates="transactions")
    
    # One-to-one relationships with detail tables
    trade = relationship("Trade", back_populates="transaction", uselist=False)
    income = relationship("Income", back_populates="transaction", uselist=False)
    fee = relationship("Fee", back_populates="transaction", uselist=False)
    transfer = relationship("Transfer", back_populates="transaction", uselist=False)

class Trade(Base):
    __tablename__ = 'trades'
    
    trade_id = Column(Integer, primary_key=True)
    transaction_id = Column(Integer, ForeignKey('transactions.transaction_id'), nullable=False)
    security_id = Column(Integer, ForeignKey('securities.security_id'), nullable=False)
    units = Column(Numeric(15, 6), nullable=False)
    price = Column(Numeric(10, 4), nullable=False)
    trading_fee = Column(Numeric(10, 2), default=0.0)
    is_buy = Column(Boolean, nullable=False)
    
    # Relationships
    transaction = relationship("Transaction", back_populates="trade")
    security = relationship("Security", back_populates="trades")

class Income(Base):
    __tablename__ = 'incomes'
    
    income_id = Column(Integer, primary_key=True)
    transaction_id = Column(Integer, ForeignKey('transactions.transaction_id'), nullable=False)
    security_id = Column(Integer, ForeignKey('securities.security_id'))  # Nullable for cash interest
    amount = Column(Numeric(10, 2), nullable=False)
    
    # Relationships
    transaction = relationship("Transaction", back_populates="income")
    security = relationship("Security", back_populates="incomes")

class Fee(Base):
    __tablename__ = 'fees'
    
    fee_id = Column(Integer, primary_key=True)
    transaction_id = Column(Integer, ForeignKey('transactions.transaction_id'), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    
    # Relationships
    transaction = relationship("Transaction", back_populates="fee")

class Transfer(Base):
    __tablename__ = 'transfers'
    
    transfer_id = Column(Integer, primary_key=True)
    transaction_id = Column(Integer, ForeignKey('transactions.transaction_id'), nullable=False)
    from_account_id = Column(Integer, ForeignKey('accounts.account_id'), nullable=False)
    to_account_id = Column(Integer, ForeignKey('accounts.account_id'), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    
    # Relationships
    transaction = relationship("Transaction", back_populates="transfer")
    from_account = relationship("Account", foreign_keys=[from_account_id], back_populates="transfers_from")
    to_account = relationship("Account", foreign_keys=[to_account_id], back_populates="transfers_to")