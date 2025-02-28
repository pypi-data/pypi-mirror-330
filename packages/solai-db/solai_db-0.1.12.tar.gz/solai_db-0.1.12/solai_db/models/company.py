from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.orm import relationship
from .base import Base, HumanIDMixin, TimestampMixin


class User(Base):
    """
    A user is a person who can login to the system.

    Users are managed in Auth0.
    """

    __tablename__ = "users"

    id = Column(TEXT, primary_key=True)


class Company(Base):
    """
    An company is a group of users who are part of the same company.

    Companies are managed in Auth0 as organizations.
    """

    __tablename__ = "companies"

    id = Column(TEXT, primary_key=True)
    name = Column(TEXT, nullable=False)

    customers = relationship("Customer", back_populates="company")


class Customer(Base, HumanIDMixin, TimestampMixin):
    """
    A customer is created by an organization.
    """

    __tablename__ = "customers"

    id = Column(TEXT, primary_key=True)
    name = Column(TEXT, nullable=False)
    email = Column(TEXT, nullable=False)

    # Relationships
    company_id = Column(
        TEXT,
        ForeignKey("companies.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    company = relationship("Company", back_populates="customers")
