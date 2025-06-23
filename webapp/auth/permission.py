# webapp/auth/permissions.py
from typing import Dict, List, Set

# Permission definitions with descriptions
API_PERMISSIONS: Dict[str, str] = {
    # Cell permissions
    "cell:create": "Create new cells",
    "cell:read": "View cells",
    "cell:update": "Update cells",
    "cell:delete": "Delete cells",

    # Client permissions
    "client:create": "Create new clients",
    "client:read": "View clients",
    "client:update": "Update clients",
    "client:delete": "Delete clients",

    # User permissions
    "user:create": "Create users",
    "user:read": "View users",
    "user:update": "Update users",
    "user:delete": "Delete users",
    
    # Measurement Data permissions
    "measurement_data:create": "Create measurement data",
    "measurement_data:read": "View measurement data",
    "measurement_data:update": "Update measurement data",
    "measurement_data:delete": "Delete measurement data",

    # Line permissions
    "line:create": "Create new lines",
    "line:read": "View lines",
    "line:update": "Update lines",
    "line:delete": "Delete lines",

    # Maintenance Configuration permissions
    "maintenance:configuration:create": "Create maintenance configurations",
    "maintenance:configuration:read": "View maintenance configurations",
    "maintenance:configuration:update": "Update maintenance configurations",
    "maintenance:configuration:delete": "Delete maintenance configurations",

    # Maintenance LocalStorage permissions
    "maintenance:localStorage:create": "Create localStorage items",
    "maintenance:localStorage:read": "View localStorage items",
    "maintenance:localStorage:update": "Update localStorage items",
    "maintenance:localStorage:delete": "Delete localStorage items",

    # Add permissions for all your other endpoints
    # Following the same pattern: "resource:action"
}

# Permission groups for common role patterns
PERMISSION_GROUPS: Dict[str, Set[str]] = {
    "CELL_MANAGER": {
        "cell:create",
        "cell:read",
        "cell:update",
        "cell:delete"
    },
    "CLIENT_MANAGER": {
        "client:create",
        "client:read",
        "client:update",
        "client:delete"
    },
    "READ_ONLY": {
        "cell:read",
        "client:read",
        "user:read"
    }
}


def validate_permissions(permissions: List[str]) -> List[str]:
    """Validate that requested permissions exist in the system."""
    invalid_perms = [p for p in permissions if p not in API_PERMISSIONS]
    if invalid_perms:
        raise ValueError(f"Invalid permissions: {', '.join(invalid_perms)}")
    return permissions


def expand_permission_groups(permissions: List[str]) -> Set[str]:
    """Expand permission groups into individual permissions."""
    expanded_perms = set()
    for perm in permissions:
        if perm in PERMISSION_GROUPS:
            expanded_perms.update(PERMISSION_GROUPS[perm])
        else:
            expanded_perms.add(perm)
    return expanded_perms


def get_all_permissions() -> Dict[str, str]:
    """Get all available permissions with their descriptions."""
    return API_PERMISSIONS


def get_permission_groups() -> Dict[str, Set[str]]:
    """Get all available permission groups."""
    return PERMISSION_GROUPS