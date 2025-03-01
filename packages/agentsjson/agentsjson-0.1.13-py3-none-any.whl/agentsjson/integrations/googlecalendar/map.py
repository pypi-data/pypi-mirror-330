from .tools import Executor
from ..types import ExecutorType

# Define the type of execution (REST API, Function call, etc.)
map_type = ExecutorType.SDK

# Mapping of operation IDs to corresponding function implementations
map = {
    # Calendar Operations
    "google_calendar_calendars_insert": Executor.create_calendar,
    "google_calendar_calendars_delete": Executor.delete_calendar,
    "google_calendar_calendars_get": Executor.get_calendar_details,
    "google_calendar_calendars_list": Executor.list_calendars,
    "google_calendar_calendars_update": Executor.update_calendar_settings,

    # Event Operations
    "google_calendar_events_insert": Executor.create_event,
    "google_calendar_events_delete": Executor.delete_event,
    "google_calendar_events_patch": Executor.update_event,
    "google_calendar_events_get": Executor.get_event_details,
    "google_calendar_events_list": Executor.list_events,

    # Attendee Management
    "google_calendar_events_attendees_add": Executor.add_attendee,
    "google_calendar_events_attendees_remove": Executor.remove_attendee,
    "google_calendar_events_attendees_update": Executor.update_attendee_response,

    # Permissions & ACL
    "google_calendar_acl_insert": Executor.set_calendar_permissions,
    "google_calendar_acl_list": Executor.list_calendar_access_control,
    "google_calendar_acl_delete": Executor.remove_user_access,

    # Availability & Scheduling
    "google_calendar_freebusy_query": Executor.check_free_busy,
    "google_calendar_working_hours_set": Executor.set_working_hours,
    "google_calendar_events_reschedule": Executor.reschedule_event,

    # Notifications & Reminders
    "google_calendar_events_reminders_set": Executor.set_event_reminder,
    "google_calendar_notifications_subscribe": Executor.subscribe_calendar_updates,
    "google_calendar_notifications_unsubscribe": Executor.unsubscribe_calendar_updates,

    # AI-Powered Features
    "google_calendar_ai_generate_agenda": Executor.auto_generate_agenda,
    "google_calendar_ai_categorize_event": Executor.smart_event_categorization,
    "google_calendar_ai_predict_meeting_time": Executor.predict_best_meeting_time,

    # Data Import/Export
    "google_calendar_events_import": Executor.import_events,
    "google_calendar_calendars_export": Executor.export_calendar,
    "google_calendar_events_migrate": Executor.migrate_events,

    # Bulk Operations
    "google_calendar_events_bulk_delete": Executor.bulk_delete_events,
    "google_calendar_events_bulk_update": Executor.bulk_update_events,

    # Advanced Analytics
    "google_calendar_events_summary_report": Executor.generate_event_summary,
    "google_calendar_meeting_attendance_track": Executor.track_meeting_attendance,
    "google_calendar_events_trends_analysis": Executor.analyze_event_trends,
}
