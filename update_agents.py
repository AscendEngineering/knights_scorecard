import csv
import sqlite3
import argparse

class agent():
    def __init__(self,agent_data):
        self.name=agent_data[0]  + ' ' + agent_data[1]
        self.email=agent_data[2]


def main(dbName,csvFile):
    
    #open the csv file
    with open(csvFile,newline='') as agentList:
        agent_reader = csv.reader(agentList,delimiter=',')

        #skip headers
        next(agent_reader)

        #read in all agents
        agents = []
        for entry in agent_reader:

            #sanity check csv proper form
            if(len(entry) != 3):
                print("Error reading csv file")
                exit(1)

            #email sanity check
            current_agent = agent(entry)
            if((current_agent.email=="") or ("@gmail.com" not in current_agent.email)):
                continue
            else:
                agents.append(current_agent)
            

    #go through the list of agents
    conn = sqlite3.connect(dbName)
    db = conn.cursor()
    insert_template = "INSERT INTO scorecard_knightinfo (name,email) VALUES ('%s','%s')"
    for agent_data in agents:

        #insert them in the database
        insert_statement = insert_template % (agent_data.name,agent_data.email)
        db.execute(insert_statement)

    conn.commit()
    conn.close()



if __name__=="__main__":
    #parse the args
    parser = argparse.ArgumentParser(description='Tool for updating the agents in the database')
    parser.add_argument('csvFile',help='Enter the csv file')
    parser.add_argument('dbFile',help='Enter the sqlite3 file')
    args = parser.parse_args()

    #if the input file does not include .sqlite3 reject
    if(".sqlite3" not in args.dbFile):
        print("\n**** FILE MUST BE .sqlite3 ****\n")
        exit(1)

    if(".csv" not in args.csvFile):
        print("\n**** FILE MUST BE .csvFile ****\n")
        exit(1)
    
    #pass the file to main
    main(args.dbFile,args.csvFile)