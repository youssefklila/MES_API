# repositories/line_repository.py

from typing import List, Optional, Dict, Any, Set
from contextlib import AbstractContextManager
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError

from webapp.ADM.machine_assets.machine_setup.line.models.line_model import Line, line_station_association
from webapp.ADM.machine_assets.machine_setup.station.models.station_model import Station

class LineRepository:
    def __init__(self, session_factory: AbstractContextManager[Session]):
        self.session_factory = session_factory

    def _to_dict(self, line: Line) -> Dict[str, Any]:
        """Convert a Line object to a dictionary with related stations."""
        if not line:
            return None
            
        result = {
            'id': line.id,
            'name': line.name,
            'description': line.description,
            'date': line.date,
            'user_id': line.user_id,
            'station_ids': [station.id for station in line.stations] if line.stations else []
        }
        return result

    def get_all(self) -> List[Dict[str, Any]]:
        """Get all lines with their associated stations."""
        with self.session_factory() as session:
            lines = session.query(Line).options(joinedload(Line.stations)).all()
            return [self._to_dict(line) for line in lines]

    def get_by_id(self, line_id: int) -> Optional[Dict[str, Any]]:
        """Get a line by ID with its associated stations."""
        with self.session_factory() as session:
            line = session.query(Line).options(joinedload(Line.stations))\
                                   .filter(Line.id == line_id).first()
            return self._to_dict(line)

    def get_by_station_id(self, station_id: int) -> List[Dict[str, Any]]:
        """Get all lines that include the specified station."""
        with self.session_factory() as session:
            lines = session.query(Line).join(Line.stations)\
                                     .filter(Station.id == station_id).all()
            return [self._to_dict(line) for line in lines]

    def add(self, **kwargs) -> Dict[str, Any]:
        """Add a new line with associated stations."""
        station_ids = kwargs.pop('station_ids', [])
        with self.session_factory() as session:
            try:
                # Create the line
                line = Line(**kwargs)
                
                # Add associated stations if any
                if station_ids:
                    stations = session.query(Station).filter(Station.id.in_(station_ids)).all()
                    line.stations = stations
                
                session.add(line)
                session.commit()
                session.refresh(line)
                return self._to_dict(line)
            except SQLAlchemyError as e:
                session.rollback()
                raise ValueError(f"Failed to add line: {str(e)}")

    def update(self, line_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        """Update a line and its associated stations."""
        station_ids = kwargs.pop('station_ids', None)
        with self.session_factory() as session:
            try:
                line = session.query(Line).options(joinedload(Line.stations))\
                                       .filter(Line.id == line_id).first()
                if not line:
                    return None

                # Update basic fields
                for key, value in kwargs.items():
                    if hasattr(line, key) and value is not None:
                        setattr(line, key, value)
                
                # Update stations if provided
                if station_ids is not None:
                    # Get current station IDs for comparison
                    current_station_ids = {station.id for station in line.stations}
                    new_station_ids = set(station_ids)
                    
                    # Find stations to add and remove
                    stations_to_add = new_station_ids - current_station_ids
                    stations_to_remove = current_station_ids - new_station_ids
                    
                    # Get station objects to add
                    if stations_to_add:
                        stations = session.query(Station).filter(
                            Station.id.in_(stations_to_add)
                        ).all()
                        line.stations.extend(stations)
                    
                    # Remove stations not in the new list
                    if stations_to_remove:
                        stations_to_keep = [s for s in line.stations 
                                         if s.id not in stations_to_remove]
                        line.stations = stations_to_keep
                
                session.commit()
                session.refresh(line)
                return self._to_dict(line)
            except SQLAlchemyError as e:
                session.rollback()
                raise ValueError(f"Failed to update line: {str(e)}")

    def delete_by_id(self, line_id: int) -> bool:
        """Delete a line by ID."""
        with self.session_factory() as session:
            try:
                line = session.query(Line).filter(Line.id == line_id).first()
                if not line:
                    return False

                session.delete(line)
                session.commit()
                return True
            except SQLAlchemyError as e:
                session.rollback()
                raise ValueError(f"Failed to delete line: {str(e)}")
