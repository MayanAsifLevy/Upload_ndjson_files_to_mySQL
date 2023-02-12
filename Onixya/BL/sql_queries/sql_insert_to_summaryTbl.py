insert_to_summaryTbl= '''
                        insert into primary_db.summaryTbl (date_start, severity,  sumPerDate,  countPerDate)
                        with tableData as(
                            select severity, convert(FROM_UNIXTIME(TimeCreated/1000), date) as date_start,   TIMESTAMPDIFF(HOUR, FROM_UNIXTIME(TimeCreated/1000), FROM_UNIXTIME(timeclosed/1000)) AS hours_difference /*, if(severity='critical' and convert(FROM_UNIXTIME(TimeCreated/1000), date) in ("2022-12-12",'2022-12-11', "2022-12-10"),1, 0) as datetoignore*/
                            from primary_db.incidents_data
                            where status='closed'  

                            )
                            , sumPerdate as (
                            (select date_start, severity, sum(hours_difference) as sumPerDate, count(hours_difference) as countPerDate
                            from tableData
                            group by date_start, severity)

                            Union

                            (select date_start, "All" as severity, sum(hours_difference) as sumPerDate, count(hours_difference) as countPerDate
                                from tableData
                                group by date_start)

                            )

                            select *
                            from sumPerdate
                            order by date_start, severity
                '''