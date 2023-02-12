create_incidents_data=  '''
            CREATE TABLE primary_db.incidents_data (
            TenantId text,
            IncidentId text,
            IntegrationName text,
            EventId text,
            EventCreatedTime bigint DEFAULT NULL,
            Severity text,
            Status text,
            TimeCreated bigint DEFAULT NULL,
            TimeClosed text,
            TimeCreated_Datetime datetime DEFAULT NULL,
            TimeClosed_Datetime datetime DEFAULT NULL
            ) 

            '''