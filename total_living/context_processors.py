from django.conf import settings


def map_tiles(request):
    """Expose map tile provider config to templates."""
    return {
        'MAP_TILES': {
            'url': getattr(settings, 'MAP_TILE_URL', 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'),
            'attribution': getattr(settings, 'MAP_TILE_ATTRIBUTION', '&copy; OpenStreetMap contributors'),
            'subdomains': getattr(settings, 'MAP_TILE_SUBDOMAINS', 'abc'),
            'max_zoom': getattr(settings, 'MAP_TILE_MAX_ZOOM', 19),
        }
    }
