# repositories/booking_repository.py

from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict, List, Optional, Callable
from datetime import datetime
from contextlib import AbstractContextManager

from webapp.ADM.TRACKING.booking.models.booking_model import Booking

class BookingRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory

    def get_by_id(self, booking_id: int) -> Optional[Dict]:
        """Get a booking by ID."""
        with self.session_factory() as session:
            booking = session.query(Booking).filter(Booking.id == booking_id).first()
            if not booking:
                return None
            return self._to_dict(booking)

    def get_all(self) -> List[Dict]:
        """Get all bookings."""
        with self.session_factory() as session:
            bookings = session.query(Booking).all()
            return [self._to_dict(booking) for booking in bookings]

    def add(self, workorder_id: int, station_id: int, failed_id: int, date_of_booking: datetime, state: str, mesure_id: Optional[int] = None) -> Dict:
        """Add a new booking."""
        with self.session_factory() as session:
            booking = Booking(
                workorder_id=workorder_id,
                station_id=station_id,
                failed_id=failed_id,
                date_of_booking=date_of_booking,
                state=state,
                mesure_id=mesure_id
            )
            session.add(booking)
            session.commit()
            session.refresh(booking)
            return self._to_dict(booking)

    def update_booking(self, booking_id: int, **kwargs) -> Optional[Dict]:
        """Update a booking."""
        with self.session_factory() as session:
            booking = session.query(Booking).filter(Booking.id == booking_id).first()
            if not booking:
                return None

            # Update only provided fields
            for key, value in kwargs.items():
                if value is not None and hasattr(booking, key):
                    setattr(booking, key, value)

            session.commit()
            session.refresh(booking)
            return self._to_dict(booking)

    def delete_by_id(self, booking_id: int) -> bool:
        """Delete a booking by ID."""
        with self.session_factory() as session:
            booking = session.query(Booking).filter(Booking.id == booking_id).first()
            if not booking:
                return False

            session.delete(booking)
            session.commit()
            return True

    def get_state_statistics(self) -> Dict[str, int]:
        """Get statistics about the number of bookings per state."""
        with self.session_factory() as session:
            result = {}
            # Query to count bookings by state
            stats = session.query(Booking.state, func.count(Booking.id).label('count')).\
                group_by(Booking.state).all()
            
            # Convert to dictionary
            for state, count in stats:
                result[state] = count
            
            return result
    
    def search_by_state(self, state: str) -> List[Dict]:
        """Search bookings by state."""
        with self.session_factory() as session:
            bookings = session.query(Booking).filter(Booking.state == state).all()
            return [self._to_dict(booking) for booking in bookings]
    
    def get_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Dict]:
        """Get bookings within a date range.
        
        Args:
            start_date: Start date of the range (inclusive)
            end_date: End date of the range (inclusive)
            
        Returns:
            List of booking dictionaries
        """
        with self.session_factory() as session:
            bookings = session.query(Booking).filter(
                Booking.date_of_booking >= start_date,
                Booking.date_of_booking <= end_date
            ).order_by(Booking.date_of_booking).all()
            
            return [self._to_dict(booking) for booking in bookings]
    
    def get_by_state_and_date(self, state: str, start_date: datetime, end_date: datetime) -> List[Dict]:
        """Get bookings by state and within a date range.
        
        Args:
            state: Booking state to filter by
            start_date: Start date of the range (inclusive)
            end_date: End date of the range (inclusive)
            
        Returns:
            List of booking dictionaries
        """
        with self.session_factory() as session:
            bookings = session.query(Booking).filter(
                Booking.state == state,
                Booking.date_of_booking >= start_date,
                Booking.date_of_booking <= end_date
            ).order_by(Booking.date_of_booking).all()
            
            return [self._to_dict(booking) for booking in bookings]
    
    def get_by_workorder_id(self, workorder_id: int) -> List[Dict]:
        """Get bookings by workorder ID.
        
        Args:
            workorder_id: ID of the workorder to filter by
            
        Returns:
            List of booking dictionaries
        """
        with self.session_factory() as session:
            bookings = session.query(Booking).filter(
                Booking.workorder_id == workorder_id
            ).order_by(Booking.date_of_booking).all()
            
            return [self._to_dict(booking) for booking in bookings]
    
    def _to_dict(self, booking: Booking) -> Dict:
        """Convert a Booking model to a dictionary."""
        return {
            "id": booking.id,
            "workorder_id": booking.workorder_id,
            "station_id": booking.station_id,
            "failed_id": booking.failed_id,
            "date_of_booking": booking.date_of_booking,
            "state": booking.state,
            "mesure_id": booking.mesure_id
        }
