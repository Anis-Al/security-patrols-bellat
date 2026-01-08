import math
from odoo.http import request


def _parse_int(value):
    try:
        return int(value) if value is not None else None
    except (TypeError, ValueError):
        return None


def _parse_float(value):
    try:
        return float(value) if value is not None else None
    except (TypeError, ValueError):
        return None


def _calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points on Earth (in meters)
    using the Haversine formula.
    
    Args:
        lat1, lon1: Latitude and longitude of first point (in decimal degrees)
        lat2, lon2: Latitude and longitude of second point (in decimal degrees)
    
    Returns:
        Distance in meters, or None if coordinates are invalid
    """
    if None in (lat1, lon1, lat2, lon2):
        return None
    
    # Earth radius in meters
    R = 6371000
    
    # Convert degrees to radians
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    # Haversine formula
    a = math.sin(delta_phi / 2) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = R * c
    return distance


def _serialize_checkpoint(checkpoint):
    return {
        "id": checkpoint.id,
        "name": checkpoint.name,
        "identifier": checkpoint.identifier,
        "check_type": checkpoint.check_type,
        "site": {
            "id": checkpoint.site_id.id,
            "name": checkpoint.site_id.name,
        } if checkpoint.site_id else None,
        "latitude": checkpoint.latitude,
        "longitude": checkpoint.longitude,
    }


def _serialize_tour(tour):
    return {
        "id": tour.id,
        "name": tour.name,
        "date": tour.date,
        "start_time": tour.start_time,
        "end_time": tour.end_time,
        "state": tour.state,
        "site": {
            "id": tour.site_id.id,
            "name": tour.site_id.name,
        } if tour.site_id else None,
        "config": {
            "grace_period": tour.grace_period,
            "strict_ordering": tour.strict_ordering,
            "require_selfie": tour.require_selfie,
            "require_photo_place": tour.require_photo_place,
            "max_checkpoint_distance": tour.max_checkpoint_distance,
        },
        "checkpoints": [
            {
                "line_id": line.id,
                "checkpoint_id": line.checkpoint_id.id,
                "sequence": line.sequence,
                "checkpoint_name": line.checkpoint_id.name,
                "identifier": line.checkpoint_id.identifier,
                "check_type": line.checkpoint_id.check_type,
                "latitude": line.checkpoint_id.latitude,
                "longitude": line.checkpoint_id.longitude,
            }
            for line in tour.checkpoint_ids
        ],
    }


def _get_param(name, default=None):
    return request.params.get(name, default)



