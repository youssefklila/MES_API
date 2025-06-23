# exceptions/bom_exceptions.py

class BomNotFoundException(Exception):
    """Exception raised when a BOM is not found."""
    def __init__(self, bom_id: int):
        self.message = f"BOM with ID {bom_id} not found"
        super().__init__(self.message)

class BomValidationError(Exception):
    """Exception raised when BOM data validation fails."""
    def __init__(self, message: str):
        self.message = f"BOM validation error: {message}"
        super().__init__(self.message)

class BomVersionConflictError(Exception):
    """Exception raised when there's a conflict with BOM versions."""
    def __init__(self, bom_version: int):
        self.message = f"Conflict with existing BOM version {bom_version}"
        super().__init__(self.message) 