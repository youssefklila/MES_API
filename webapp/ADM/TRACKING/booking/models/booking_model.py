# models/booking_model.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from webapp.database import Base

class Booking(Base):
    __tablename__ = "bookings"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    workorder_id = Column(Integer, ForeignKey("work_orders.id"), nullable=False)
    station_id = Column(Integer, ForeignKey("stations.id"), nullable=False)
    failed_id = Column(Integer, ForeignKey("failure_types.failure_type_id"), nullable=False)  # Foreign key to failure_types table
    date_of_booking = Column(DateTime(timezone=True), nullable=False)  # Changed to DateTime with timezone
    state = Column(String, nullable=False)
    mesure_id = Column(Integer, nullable=True)  # Changed from mesure_name (String) to mesure_id (Integer)

    # Relationships
    workorder = relationship("WorkOrder", backref="bookings")
    station = relationship("Station", backref="bookings")
    failure_type = relationship("FailureType", back_populates="bookings")
    measurement_data = relationship("MeasurementData", back_populates="booking")

    def __repr__(self):
        return f"<Booking(id={self.id}, workorder_id={self.workorder_id}, station_id={self.station_id}, failed_id={self.failed_id}, date_of_booking={self.date_of_booking}, state={self.state}, mesure_id={self.mesure_id})>"
