import ndjson, json
import builtins

from BL.sql_queries.sql_insert_to_incidents_data import insert_to_incidents_data
from BL.sql_queries.sql_insert_to_summaryTbl import insert_to_summaryTbl
from BL.sql_queries.sql_avg_aggregarion_per_severity import avg_aggregarion_per_severity
from BL.sql_queries.sql_create_summaryTBL import create_summaryTBL
from BL.sql_queries.sql_create_incidents_data import create_incidents_data




def parseJSON(filePath, mydb,  mycursor):
        with open(filePath, 'r') as f:
            jsonData=ndjson.loads(f.read())
        try:   
            mycursor.execute("DROP TABLE IF EXISTS  primary_db.incidents_data")
            mydb.commit()

            mycursor.execute(create_incidents_data)
            mydb.commit()

        except Exception as e: 
            print(e)
            mydb.rollback()
        
        tpls=[]
        # for row in jsonData:    
        for row in jsonData:
            list = tuple(( v) for v in row.values())
            tpls.append(list)
 
        try:       
            mycursor.executemany(insert_to_incidents_data, tpls)
            mydb.commit()
        except Exception as e: 
            print(e)
            mydb.rollback()

        # working on table: summarytbl ============================================
        
        try:
            mycursor.execute("DROP TABLE IF EXISTS primary_db.summaryTbl")
            mydb.commit()

            mycursor.execute(create_summaryTBL)
            mydb.commit()
        
            mycursor.execute(insert_to_summaryTbl)
            mydb.commit()

        except Exception as e: 
            print(e)
            mydb.rollback()
 
        # get split files per severity ============================================

        mycursor.execute(avg_aggregarion_per_severity)
        results = mycursor.fetchall()
        recrodsList = []
        for record in results:
            dictRecord = {}
            dictRecord['datestart'] = record[0].strftime("%d/%m/%Y")
            dictRecord['avgPerdayoflast7days'] = int(record[1])
            dictRecord['severity'] = record[2]

            recrodsList.append(dictRecord)

        severity= set(row['severity'] for row in recrodsList)
        # to convert the set into list
        list1 = builtins.list 
        list_of_severities = list1(severity)

  
        for sev in list_of_severities:
            file_name= 'downloads/average_of_'+sev+'.json'
            summaryFilterPerSeverity= list1(filter(lambda x: x['severity']==sev, recrodsList))
            with open(file_name, 'w') as f:
                json.dump(summaryFilterPerSeverity, f)
            