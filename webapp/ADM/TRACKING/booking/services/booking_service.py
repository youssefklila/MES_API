# services/booking_service.py

from typing import List, Dict, Optional
from datetime import datetime

from webapp.ADM.TRACKING.booking.repositories.booking_repository import BookingRepository
from webapp.ADM.TRACKING.booking.schemas.booking_schema import BookingResponse

class BookingService:
    def __init__(self, repository: BookingRepository):
        self.repository = repository

    def _to_response(self, booking_dict: Dict) -> BookingResponse:
        """Convert dictionary to Pydantic response model."""
        return BookingResponse(**booking_dict)

    def get_all_bookings(self) -> List[BookingResponse]:
        """Get all bookings."""
        try:
            bookings = self.repository.get_all()
            return [self._to_response(b) for b in bookings]
        except Exception as e:
            raise ValueError(f"Failed to get bookings: {str(e)}")

    def get_booking_by_id(self, booking_id: int) -> Optional[BookingResponse]:
        """Get a booking by ID."""
        try:
            booking = self.repository.get_by_id(booking_id)
            if booking:
                return self._to_response(booking)
            return None
        except Exception as e:
            raise ValueError(f"Failed to get booking: {str(e)}")

    def create_booking(self, workorder_id: int, station_id: int, failed_id: int, date_of_booking: datetime, state: str, mesure_id: Optional[int] = None) -> BookingResponse:
        """Create a new booking."""
        try:
            # Validate input
            if not state or not state.strip():
                raise ValueError("State is required")
            
            booking = self.repository.add(
                workorder_id=workorder_id,
                station_id=station_id,
                failed_id=failed_id,
                date_of_booking=date_of_booking,
                state=state.strip(),
                mesure_id=mesure_id
            )
            return self._to_response(booking)
        except ValueError as e:
            raise e
        except Exception as e:
            raise ValueError(f"Failed to create booking: {str(e)}")

    def update_booking(self, booking_id: int, **kwargs) -> Optional[BookingResponse]:
        """Update a booking."""
        try:
            # Validate input
            if 'state' in kwargs and kwargs['state'] is not None:
                if not kwargs['state'].strip():
                    raise ValueError("State cannot be empty")
                kwargs['state'] = kwargs['state'].strip()
            
            booking = self.repository.update_booking(booking_id, **kwargs)
            if booking:
                return self._to_response(booking)
            return None
        except ValueError as e:
            raise e
        except Exception as e:
            raise ValueError(f"Failed to update booking: {str(e)}")

    def delete_booking(self, booking_id: int) -> bool:
        """Delete a booking."""
        try:
            return self.repository.delete_by_id(booking_id)
        except Exception as e:
            raise ValueError(f"Failed to delete booking: {str(e)}")
            
    def get_state_statistics(self) -> Dict[str, int]:
        """Get statistics about the number of bookings per state."""
        try:
            return self.repository.get_state_statistics()
        except Exception as e:
            raise ValueError(f"Failed to get booking statistics: {str(e)}")
    
    def search_bookings_by_state(self, state: str) -> List[BookingResponse]:
        """Search bookings by state."""
        try:
            if not state or not state.strip():
                raise ValueError("State is required for search")
                
            bookings = self.repository.search_by_state(state.strip())
            return [self._to_response(b) for b in bookings]
        except ValueError as e:
            raise e
        except Exception as e:
            raise ValueError(f"Failed to search bookings: {str(e)}")

    def get_bookings_by_date_range(self, start_date: datetime, end_date: datetime) -> List[BookingResponse]:
        """Get bookings within a date range.
        
        Args:
            start_date: Start date of the range (inclusive)
            end_date: End date of the range (inclusive)
            
        Returns:
            List of booking response objects
        """
        try:
            if start_date > end_date:
                raise ValueError("Start date must be before or equal to end date")
                
            bookings = self.repository.get_by_date_range(start_date, end_date)
            return [self._to_response(b) for b in bookings]
        except ValueError as e:
            raise e
        except Exception as e:
            raise ValueError(f"Failed to get bookings by date range: {str(e)}")
            
    def get_bookings_by_state_and_date(self, state: str, start_date: datetime, end_date: datetime) -> List[BookingResponse]:
        """Get bookings by state and within a date range.
        
        Args:
            state: Booking state to filter by
            start_date: Start date of the range (inclusive)
            end_date: End date of the range (inclusive)
            
        Returns:
            List of booking response objects
        """
        try:
            if not state or not state.strip():
                raise ValueError("State is required for search")
                
            if start_date > end_date:
                raise ValueError("Start date must be before or equal to end date")
                
            bookings = self.repository.get_by_state_and_date(state.strip(), start_date, end_date)
            return [self._to_response(b) for b in bookings]
        except ValueError as e:
            raise e
        except Exception as e:
            raise ValueError(f"Failed to get bookings by state and date: {str(e)}")
            
    def get_bookings_by_workorder_id(self, workorder_id: int) -> List[BookingResponse]:
        """Get bookings by workorder ID.
        
        Args:
            workorder_id: ID of the workorder to filter by
            
        Returns:
            List of booking response objects
        """
        try:
            if workorder_id <= 0:
                raise ValueError("Workorder ID must be a positive integer")
                
            bookings = self.repository.get_by_workorder_id(workorder_id)
            return [self._to_response(b) for b in bookings]
        except ValueError as e:
            raise e
        except Exception as e:
            raise ValueError(f"Failed to get bookings by workorder ID: {str(e)}")
