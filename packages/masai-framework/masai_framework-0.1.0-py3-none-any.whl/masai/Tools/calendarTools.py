import nylas
import os, json
from datetime import datetime, timedelta
from nylas import Client
from datetime import datetime
from typing import Optional, Dict, Any
from typing import Optional
import pytz  # pip install pytz
from langchain.tools import tool


# Initialize Nylas client
nylas = Client(
    api_key=os.getenv("NYLAS_API_KEY"),
    api_uri="https://api.us.nylas.com"  # https://api.us.nylas.com
)

# print(nylas, os.getenv("NYLAS_API_KEY"),os.getenv("NYLAS_GRANT_ID"))

@tool("Calendar_Event_Fetcher", return_direct=False)
def fetch_calendar_events(lastNdays=10, nextNdays=10) -> list:
    """
    Fetch all events from user's calendar. All calendar events  written to MAS,PRIVATE,Calendar,calendar.json
    lastNdays:int = fetches all calendar events from last n days. Example: n=10 fetches all data from last 10 days.
    nextNdays:int = fetches all events till current day + nth day. Example: n=10 fetches all events from current to next 10 days.
    Note nextNdays > lastNdays.
    --------------------IMPORTANT NOTES For Calendar Events Fetcher--------------------------------------------------------
    range in format (start_date,end_date)=(datetime.now - last+Ndays to datetime.now + nextNdays)
    Fetch todays' data by setting lastNdays=0, nextNdays=1.
    """
    try:
        if lastNdays is None or nextNdays is None:
            lastNdays = 2
            nextNdays = 2
        start = int((datetime.now() - timedelta(days=int(lastNdays))).timestamp())
        end = int((datetime.now() + timedelta(days=int(nextNdays))).timestamp())
        delta_seconds = end - start
        delta_days = delta_seconds // 86400
        if delta_days<30:
            limit=20
        elif delta_days>=30:
            limit=40
        elif delta_days>=60:
            limit=50
        elif delta_days>=90:
            limit=100

        grant_id = os.environ.get("NYLAS_GRANT_ID")

        calendar_id: str = "primary"
        events = nylas.events.list(
            identifier=grant_id,
            query_params={
                "calendar_id": calendar_id,
                "limit":limit,  # Max allowed
                "start": start,
                "end":end
            }
        ).data


        formatted_events = []
        
        for event in events:
            event_data = {
                "id": event.id,
                "title": event.title,
                "description": event.description,
                "organizer": event.organizer if event.organizer else None,
                "status": event.status,
                "conference_link": event.conferencing.details if event.conferencing else None,
                "participants": [p.email for p in event.participants],
                "start": datetime.fromtimestamp(event.when.start_time).strftime("%d/%m/%Y, %H:%M:%S"),
                "end": datetime.fromtimestamp(event.when.end_time).strftime("%d/%m/%Y, %H:%M:%S")
            }
            formatted_events.append(event_data)

        os.makedirs(os.path.join("MAS","PRIVATE","Calendar"),exist_ok=True)
        with open(os.path.join("MAS","PRIVATE","Calendar","calendar.json"), "w", encoding="utf-8") as json_file:
                json.dump(formatted_events, json_file, indent=4)
        if limit<=40:        
            return f"Successfully saved {len(formatted_events)} events to calendar.json. HERE ARE YOUR EVENTS:",formatted_events
        else:
            return f"Successfully saved {len(formatted_events)} events to calendar.json"

    except Exception as e:
        print(e)
        return f"Error: {str(e)}"

def parse_datetime(input_str: str) -> datetime:
    """
    Convert LLM-generated datetime string to timezone-aware datetime object
    
    Supported formats:
    1. "2025-02-03 14:30 Asia/Kolkata" (recommended)
    2. "2025-02-03 2:30 PM IST"
    3. ISO 8601: "2025-02-03T14:30:00+05:30"
    """
    try:
        # Try ISO format first
        return datetime.fromisoformat(input_str)
    except ValueError:
        try:
            # Parse custom format
            dt_str, tz_str = input_str.rsplit(' ', 1)
            dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
            return pytz.timezone(tz_str).localize(dt)
        except ValueError:
            # Fallback to dateutil parser (pip install python-dateutil)
            from dateutil import parser
            return parser.parse(input_str)


@tool("Calendar_Event_Tool", return_direct=False)
def manage_calendar_event(
    mode: str = "create",
    title: Optional[str] = None,
    description: Optional[str] = None,
    startTime: Optional[str] = None,  # Accept string input
    endTime: Optional[str] = None,   # Accept string input
    participants: Optional[list] = None,
    eventId: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Calendar tool to create/update calendar events with proper Nylas v3 API structure for scheduling meetings
    params:
    mode: str = create or update meeting details.
    title:str = title of the meeting
    description:  str = description of the meeting
    ------------TIME FORMAT------------: YYYY-MM-DD HH:MM Asia/Kolkata
    startTime : takes str.
    endTime: takes str in format like 2025-02-03 14:30 Asis/Kolkata
    participants: List[str] = example [email1@example.com, email2@example.com]
    eventId: str = needed when updating an event, to get the required event.
    
    """
    calendar_id = "primary"
    timezone:str = "Asia/Kolkata"    # Default if not in input
    grant_id=os.environ.get("NYLAS_GRANT_ID")
    start_time=parse_datetime(startTime)
    end_time=parse_datetime(endTime)
    print(timezone)
    try:
        request_body: Dict[str, Any] = {}
        query_params = {"calendar_id": calendar_id}
        
        if mode == "create":
            if not all([title, start_time, end_time]):
                raise ValueError("Title, start_time, and end_time are required for event creation")

            # Proper when structure for timespan event
            request_body.update({
                "title": title,
                "when": {
                    "start_time": int(start_time.timestamp()),
                    "end_time": int(end_time.timestamp()),
                    "start_timezone": str(timezone),
                    "end_timezone": str(timezone)
                },
                "description":description,
                "conferencing": {
                    "provider": "Google Meet",
                    "autocreate": {}
                }
            })

        elif mode == "update":
            if not eventId:
                raise ValueError("event_id is required for updates")
            
            if title:
                request_body["title"] = title
            if start_time and end_time:
                request_body["when"] = {
                    "start_time": int(start_time.timestamp()),
                    "end_time": int(end_time.timestamp()),
                    "start_timezone": timezone,
                    "end_timezone": timezone
                }

        if participants:
            request_body["participants"] = [{"email": email} for email in participants]

        # request_body.update(kwargs)

        if mode == "create":
            event = nylas.events.create(
                identifier=grant_id,
                query_params=query_params,
                request_body=request_body
            )
        elif mode == "update":
            event = nylas.events.update(
                identifier=grant_id,
                event_id=eventId,
                query_params=query_params,
                request_body=request_body
            )

        return {
            "eventId": event.data.id,
            "title": event.data.title,
            "description": event.data.description,
            "meeting_link": event.data.conferencing.details if event.data.conferencing else None,
            "calendar_id": event.data.calendar_id,
            "status": event.data.status,
            "html_link": event.data.html_link,
        }
        
    except Exception as e:
        return {"error": f"Error managing event: {str(e)}"}