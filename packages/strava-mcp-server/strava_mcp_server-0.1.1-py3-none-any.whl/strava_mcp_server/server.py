#!/usr/bin/env python3
"""
MCP server for Strava API integration.
This server exposes methods to query the Strava API for athlete activities.
"""

import os
import time
from datetime import date, datetime, timedelta
from typing import Any, Optional

import httpx
from mcp.server.fastmcp import FastMCP

from dotenv import load_dotenv

load_dotenv()


class StravaClient:
    """Client for interacting with the Strava API."""

    BASE_URL = "https://www.strava.com/api/v3"
    
    def __init__(self, refresh_token: str, client_id: str, client_secret: str):
        """
        Initialize the Strava API client.

        Args:
            refresh_token: Refresh token for Strava API
            client_id: Client ID for Strava API
            client_secret: Client secret for Strava API
        """
        self.refresh_token = refresh_token
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.expires_at = 0
        self.client = httpx.Client(timeout=30.0)
        
    def _ensure_valid_token(self) -> None:
        """Ensure we have a valid access token, refreshing if necessary."""
        current_time = int(time.time())
        
        # If token is missing or expired, refresh it
        if not self.access_token or current_time >= self.expires_at:
            self._refresh_token()
    
    def _refresh_token(self) -> None:
        """Refresh the access token using the refresh token."""
        refresh_url = "https://www.strava.com/oauth/token"
        payload = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refresh_token,
            'grant_type': 'refresh_token'
        }
        
        response = self.client.post(refresh_url, data=payload)
        if response.status_code != 200:
            error_msg = f"Error {response.status_code}: {response.text}"
            raise Exception(error_msg)
        
        token_data = response.json()
        self.access_token = token_data['access_token']
        self.expires_at = token_data['expires_at']
        print("Token refreshed successfully")

    def _make_request(self, endpoint: str, params: Optional[dict] = None) -> Any:
        """Make an authenticated request to the Strava API."""
        self._ensure_valid_token()
        
        url = f"{self.BASE_URL}/{endpoint}"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        response = self.client.get(url, headers=headers, params=params)
        if response.status_code != 200:
            error_msg = f"Error {response.status_code}: {response.text}"
            raise Exception(error_msg)
        
        return response.json()

    def get_activities(self, limit: int = 10, before: Optional[int] = None, after: Optional[int] = None) -> list:
        """
        Get the authenticated athlete's activities.
        
        Args:
            limit: Maximum number of activities to return
            before: Unix timestamp to filter activities before this time
            after: Unix timestamp to filter activities after this time
            
        Returns:
            List of activities
        """
        params = {"per_page": limit}
        
        if before:
            params["before"] = before
        
        if after:
            params["after"] = after
            
        return self._make_request("athlete/activities", params)
    
    def get_activity(self, activity_id: int) -> dict:
        """
        Get detailed information about a specific activity.
        
        Args:
            activity_id: ID of the activity to retrieve
            
        Returns:
            Activity details
        """
        return self._make_request(f"activities/{activity_id}")
    
    def get_athlete(self) -> dict:
        """
        Get the authenticated athlete's profile.
        
        Returns:
            Athlete profile
        """
        return self._make_request("athlete")
    
    def close(self) -> None:
        """Close the HTTP client."""
        self.client.close()


def timestamp_to_date(timestamp: int) -> date:
    """
    Convert a Unix timestamp to a date object.
    
    Args:
        timestamp: Unix timestamp
        
    Returns:
        Date object
    """
    return datetime.fromtimestamp(timestamp).date()


def date_to_timestamp(date_obj: date) -> int:
    """
    Convert a date object to a Unix timestamp (end of day).
    
    Args:
        date_obj: Date object
        
    Returns:
        Unix timestamp
    """
    dt = datetime.combine(date_obj, datetime.max.time())
    return int(dt.timestamp())


def parse_date(date_str: str) -> date:
    """
    Parse a date string in ISO format (YYYY-MM-DD).

    Args:
        date_str: Date string in ISO format

    Returns:
        Date object
    """
    try:
        return date.fromisoformat(date_str)
    except ValueError as err:
        raise ValueError(
            f"Invalid date format: {date_str}. Expected format: YYYY-MM-DD"
        ) from err


# Create MCP server and StravaClient at module level
mcp = FastMCP("Strava API MCP Server")

# Default tokens (will be overridden in main or by direct assignment)
default_refresh_token = os.environ.get("STRAVA_REFRESH_TOKEN")
default_client_id = os.environ.get("STRAVA_CLIENT_ID")
default_client_secret = os.environ.get("STRAVA_CLIENT_SECRET")

strava_client = None
if default_refresh_token and default_client_id and default_client_secret:
    strava_client = StravaClient(default_refresh_token, default_client_id, default_client_secret)


# Add tools for querying activities
@mcp.tool()
def get_activities(limit: int = 10) -> dict[str, Any]:
    """
    Get the authenticated athlete's recent activities.

    Args:
        limit: Maximum number of activities to return (default: 10)

    Returns:
        Dictionary containing activities data
    """
    if strava_client is None:
        return {"error": "Strava client not initialized. Please provide refresh token, client ID, and client secret."}

    try:
        activities = strava_client.get_activities(limit=limit)
        return {"data": activities}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_activities_by_date_range(start_date: str, end_date: str, limit: int = 30) -> dict[str, Any]:
    """
    Get activities within a specific date range.

    Args:
        start_date: Start date in ISO format (YYYY-MM-DD)
        end_date: End date in ISO format (YYYY-MM-DD)
        limit: Maximum number of activities to return (default: 30)

    Returns:
        Dictionary containing activities data
    """
    if strava_client is None:
        return {"error": "Strava client not initialized. Please provide refresh token, client ID, and client secret."}

    try:
        start = parse_date(start_date)
        end = parse_date(end_date)
        
        # Convert dates to timestamps
        after = int(datetime.combine(start, datetime.min.time()).timestamp())
        before = int(datetime.combine(end, datetime.max.time()).timestamp())
        
        activities = strava_client.get_activities(limit=limit, before=before, after=after)
        return {"data": activities}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_activity_by_id(activity_id: int) -> dict[str, Any]:
    """
    Get detailed information about a specific activity.

    Args:
        activity_id: ID of the activity to retrieve

    Returns:
        Dictionary containing activity details
    """
    if strava_client is None:
        return {"error": "Strava client not initialized. Please provide refresh token, client ID, and client secret."}

    try:
        activity = strava_client.get_activity(activity_id)
        return {"data": activity}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_recent_activities(days: int = 7, limit: int = 10) -> dict[str, Any]:
    """
    Get activities from the past X days.

    Args:
        days: Number of days to look back (default: 7)
        limit: Maximum number of activities to return (default: 10)

    Returns:
        Dictionary containing activities data
    """
    if strava_client is None:
        return {"error": "Strava client not initialized. Please provide refresh token, client ID, and client secret."}

    try:
        # Calculate timestamp for X days ago
        now = datetime.now()
        days_ago = now - timedelta(days=days)
        after = int(days_ago.timestamp())
        
        activities = strava_client.get_activities(limit=limit, after=after)
        return {"data": activities}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_athlete_profile() -> dict[str, Any]:
    """
    Get the authenticated athlete's profile.

    Returns:
        Dictionary containing athlete profile data
    """
    if strava_client is None:
        return {"error": "Strava client not initialized. Please provide refresh token, client ID, and client secret."}

    try:
        athlete = strava_client.get_athlete()
        return {"data": athlete}
    except Exception as e:
        return {"error": str(e)}


def main() -> None:
    """Main function to start the Strava MCP server."""
    print("Starting Strava MCP server!")
    
    # Initialize Strava client if not already done
    global strava_client
    if strava_client is None:
        refresh_token = os.environ.get("STRAVA_REFRESH_TOKEN")
        client_id = os.environ.get("STRAVA_CLIENT_ID")
        client_secret = os.environ.get("STRAVA_CLIENT_SECRET")
        
        if refresh_token and client_id and client_secret:
            strava_client = StravaClient(refresh_token, client_id, client_secret)
        else:
            print("Warning: Strava client not initialized. Please set STRAVA_REFRESH_TOKEN, STRAVA_CLIENT_ID, and STRAVA_CLIENT_SECRET environment variables.")
    
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main() 