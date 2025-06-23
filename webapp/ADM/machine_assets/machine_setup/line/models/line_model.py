# models/line_model.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from webapp.database import Base

# Association table for many-to-many relationship between lines and stations
line_station_association = Table(
    'line_station_association',
    Base.metadata,
    Column('line_id', Integer, ForeignKey('lines.id'), primary_key=True),
    Column('station_id', Integer, ForeignKey('stations.id'), primary_key=True),
    Column('created_at', DateTime, default=datetime.utcnow, nullable=False)
)

class Line(Base):
    __tablename__ = "lines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    date = Column(DateTime, default=datetime.utcnow, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    stations = relationship(
        "Station",
        secondary=line_station_association,
        back_populates="lines"
    )
    user = relationship("User", back_populates="lines")

    def __repr__(self):
        station_ids = [str(station.id) for station in self.stations]
        return f"<Line(id={self.id}, name={self.name}, description={self.description}, date={self.date}, station_ids={', '.join(station_ids)})>"
