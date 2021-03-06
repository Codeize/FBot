import csv

E_TIER = 0 # Tier
J_NAME = 1 # Name of the job
J_SALARY = 2 # Job salary
J_DESC = 3 # Job description
D_NAME = 4 # Relative degree name
D_LENGTH = 5 # Degree length
D_MULTI = 6 # Multiplier required for degree

class econ:
    
    def load():

        global jobs, degrees, jobnames, degreenames
        global salaries, courses, degreejobs, jobdegrees
        jobs, degrees, jobnames, degreenames = {}, {}, {}, {}
        salaries, courses, degreejobs, jobdegrees = {}, {}, {}, {}
        with open("Info/CSVs/Economy.csv", encoding="utf_8_sig") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            for row in csv_reader:

                tier = int(row[E_TIER])
                
                data = (row[J_NAME], row[J_SALARY], row[J_DESC])
                try: jobs[tier].append(data)
                except: jobs[tier] = [data]

                salaries[row[J_NAME]] = int(row[J_SALARY])
                jobnames[row[J_NAME].lower()] = row[J_NAME]

                if row[J_NAME] == "Unemployed": continue

                data = (row[D_NAME], row[D_LENGTH], float(row[D_MULTI]))
                try: degrees[tier].append(data)
                except: degrees[tier] = [data]

                courses[row[D_NAME]] = (int(row[D_LENGTH]), float(row[D_MULTI]))
                degreenames[row[D_NAME].lower()] = row[D_NAME]

                degreejobs[row[D_NAME]] = row[J_NAME]
                jobdegrees[row[J_NAME]] = row[D_NAME]
        print(" > Loaded Economy.csv")

    def search(query, dev=False):

        query = query.lower()
        for command in commands:
            if not dev:
                if command[C_CAT] == "Dev":
                    continue
            if command[C_NAME] == query:
                return command
        return None
