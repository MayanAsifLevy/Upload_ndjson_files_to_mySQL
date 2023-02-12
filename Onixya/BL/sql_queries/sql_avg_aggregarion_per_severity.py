avg_aggregarion_per_severity='''
            with total_sum_count_per_day as(
            select   date_start, 
                        severity, 
                        sum(sumPerDate) OVER (partition by severity  order by date_start     range between interval  7  day preceding  and interval 1  day preceding) as sumLast7Days, 
                        sum(countPerDate) OVER (partition by severity order by date_start   range between interval  7  day preceding  and interval 1  day preceding) as countLast7Days,
                        DATE_ADD(first_value(date_start)over(partition by severity order by date_start ) ,INTERVAL 7 day) as firstDateAvailableperseverity
            from summarytbl
            order by date_start
            )

            select date_start,  round(sumLast7Days/countLast7Days,0) as avgPerdayoflast7days, severity
            from total_sum_count_per_day
            where date_start>=firstDateAvailableperseverity
            order by date_start

          '''