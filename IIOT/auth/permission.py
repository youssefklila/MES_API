# webapp/auth/permissions.py
from typing import Dict, List, Set

# Permission definitions with descriptions
API_PERMISSIONS: Dict[str, str] = {
    # User permissions
    "user:create": "Create users",
    "user:read": "View users",
    "user:update": "Update users",
    "user:delete": "Delete users",

    # IOT permissions
    "iot:read": "Read IOT sensor data",
    "iot:publish": "Publish IOT sensor data",
    "iot:subscribe": "Subscribe to IOT sensor data",
    "iiot_sensor_data:create": "Create IIOT sensor data",
    "iiot_sensor_data:read": "Read IIOT sensor data",
    "iiot_sensor_data:update": "Update IIOT sensor data",
    "iiot_sensor_data:delete": "Delete IIOT sensor data",

    # Add permissions for all your other endpoints
    # Following the same pattern: "resource:action"
}

# Permission groups for common role patterns
PERMISSION_GROUPS: Dict[str, Set[str]] = {
    "READ_ONLY": {
        "user:read",
        "iot:read",
        "iiot_sensor_data:read"
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