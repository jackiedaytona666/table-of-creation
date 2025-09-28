"""
utils.py
--------
Role: Shared utility functions (e.g., logging setup) for all scraper modules.
"""
import logging

def setup_logging():
    """
    Set up logging for the project.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        handlers=[logging.StreamHandler()]
    )
