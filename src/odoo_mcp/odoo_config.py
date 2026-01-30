import json
import logging
import os

from odoo_mcp.odoo_client import OdooClient, OdooConfig


def load_config() -> OdooConfig:
    """
    Load Odoo configuration from environment variables or config file

    Returns:
        dict: Configuration dictionary with url, db, username, password
    """
    # Try environment variables first
    if all(var in os.environ
           for var in ["ODOO_URL", "ODOO_DB", "ODOO_USERNAME", "ODOO_PASSWORD"]):
        return OdooConfig(os.environ["ODOO_URL"],
                          os.environ["ODOO_DB"],
                          os.environ["ODOO_USERNAME"],
                          os.environ["ODOO_PASSWORD"],
                          )

    # Try to load from file
    # Define config file paths to check
    config_paths = [
        "odoo_config.json",
        os.path.expanduser(os.path.join("~", ".config", "odoo", "config.json")),
        os.path.expanduser(os.path.join("~", ".odoo_config.json")),
    ]

    for path in config_paths:
        expanded_path = os.path.expanduser(path)
        if os.path.exists(expanded_path):
            with open(expanded_path, "r") as f:
                return json.load(f)

    raise FileNotFoundError(
        f"No Odoo configuration found. Either create environment variables OR place a config file in one of these locations: {config_paths}"
    )


def get_odoo_client():
    """
    Get a configured Odoo client instance

    Returns:
        OdooClient: A configured Odoo client instance
    """
    config = load_config()

    # Get additional options from environment variables
    config.timeout = int(os.environ.get("ODOO_TIMEOUT", "30"))  # Increase default timeout to 30 seconds
    config.verify_ssl = os.environ.get("ODOO_VERIFY_SSL", "1").lower() in ["1", "true", "yes"]

    # Print detailed configuration
    logging.debug("Odoo client configuration:")
    logging.debug(f"  URL: {config.url}")
    logging.debug(f"  Database: {config.db}")
    logging.debug(f"  Username: {config.username}")
    logging.debug(f"  Timeout: {config.timeout}s")
    logging.debug(f"  Verify SSL: {config.verify_ssl}")

    return OdooClient(config)
