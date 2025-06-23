# models/measurement_data_model.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from webapp.database import Base

class MeasurementData(Base):
    """Measurement Data model."""
    
    __tablename__ = "measurement_data"
    __table_args__ = {'extend_existing': True}
    
    id = Column("ID", Integer, primary_key=True, autoincrement=True)
    station_id = Column("STATION_ID", Integer, ForeignKey("stations.id"))
    workorder_id = Column("WORKORDER_ID", Integer, ForeignKey("work_orders.id"))
    book_date = Column("BOOK_DATE", DateTime)
    measure_name = Column("MEASURE_NAME", String(80))
    measure_value = Column("MEASURE_VALUE", String(800))
    lower_limit = Column("LOWER_LIMIT", String(30))
    upper_limit = Column("UPPER_LIMIT", String(30))
    nominal = Column("NOMINAL", String(50))
    tolerance = Column("TOLERANCE", String(30))
    measure_fail_code = Column("MEASURE_FAIL_CODE", Integer)
    booking_id = Column("BOOKING_ID", Integer, ForeignKey("bookings.id"), nullable=True)
    measure_type = Column("MEASURE_TYPE", String(20))
    
    # Define relationships
    station = relationship("Station", back_populates="measurement_data")
    workorder = relationship("WorkOrder", back_populates="measurement_data")
    booking = relationship("Booking", back_populates="measurement_data")
