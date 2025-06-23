# repositories/company_code_repository.py

from contextlib import AbstractContextManager
from sqlalchemy.orm import Session
from typing import Callable, List, Dict, Any

from webapp.ADM.machine_assets.machine_setup.company_code.models.company_code_model import CompanyCode


class CompanyCodeRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def _to_dict(self, company_code: CompanyCode) -> Dict[str, Any]:
        """Convert a CompanyCode model to a dictionary."""
        return {
            "id": company_code.id,
            "user_id": company_code.user_id,
            "client_id": company_code.client_id,
            "name": company_code.name,
            "description": company_code.description
        }

    def get_all(self) -> List[Dict[str, Any]]:
        with self.session_factory() as session:
            company_codes = session.query(CompanyCode).all()
            return [self._to_dict(company_code) for company_code in company_codes]

    def get_by_id(self, company_code_id: int) -> Dict[str, Any]:
        with self.session_factory() as session:
            company_code = session.query(CompanyCode).filter(CompanyCode.id == company_code_id).first()
            return self._to_dict(company_code) if company_code else None

    def add(self, user_id: int, client_id: int, name: str, description: str) -> Dict[str, Any]:
        with self.session_factory() as session:
            company_code = CompanyCode(user_id=user_id, client_id=client_id, name=name, description=description)
            session.add(company_code)
            session.commit()
            session.refresh(company_code)
            return self._to_dict(company_code)

    def delete_by_id(self, company_code_id: int) -> None:
        with self.session_factory() as session:
            company_code = session.query(CompanyCode).filter(CompanyCode.id == company_code_id).first()
            if company_code:
                session.delete(company_code)
                session.commit()

    def update_company_code(self, company_code_id: int, **kwargs) -> Dict[str, Any]:
        with self.session_factory() as session:
            company_code = session.query(CompanyCode).filter(CompanyCode.id == company_code_id).first()
            if company_code:
                for key, value in kwargs.items():
                    setattr(company_code, key, value)
                session.commit()
                session.refresh(company_code)
                return self._to_dict(company_code)
            return None
