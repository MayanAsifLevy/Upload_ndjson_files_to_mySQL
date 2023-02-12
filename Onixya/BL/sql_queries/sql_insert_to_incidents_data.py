insert_to_incidents_data =  '''
                            INSERT INTO incidents_data
                                (TenantId,IncidentId,IntegrationName, EventId,EventCreatedTime,Severity, Status,TimeCreated,TimeClosed) 
                            VALUES (%s, %s, %s, %s,  %s, %s, %s, %s, %s)

                            '''