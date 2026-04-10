"""
API package for stock trading simulation
Exports router and initialization function
"""

from .routes import router, initialize_services

__all__ = ["router", "initialize_services"]
