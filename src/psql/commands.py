# Todo : Prevent SQL Injection

GET_ALL_COMMANDS = """
        SELECT session, url, created_at, action_target, action_data, action, TO_CHAR(timestamp,'DD-MM-YYYY-HH-MI-SS') 
        FROM ui_events
    """

GET_URL_COMMAND = """
    SELECT 
        DISTINCT url 
    FROM 
        ui_events
"""