#!/usr/bin/python3
import time

class CWASubmissionMaker:
    """Helps make CWA Outcome submission XML file"""
    def __init__(self, filename="outcomes.xml"):
        """Setup first part of file"""
        self.filename = filename
        self.lines = []
        self.lines.append('<?xml version="1.0"?>')
        self.lines.append('<submission xsi:schemaLocation="http://www.legalservices.gov.uk/sms/ActivityManagement/XMLSchema/ LSCSMSBulkLoadSchemaV2.xsd" xmlns="http://www.legalservices.gov.uk/sms/ActivityManagement/XMLSchema/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">')

    def add_top(self, account, submission_period, aol, schedule):
        """Add the top part of the file with office account and schedule details
        Args:
            account - office account number in 0A123B format
            submission_persion - schedule submission period, eg "JAN-2015"
            aol - Area of Law, e.g. "CRIME LOWER"
            schedule - schedule reference
        """
        self.lines.append('<office account="{}">\n'.format(account))
        self.lines.append('<schedule submissionPeriod="{}" areaOfLaw="{}" scheduleNum="{}">'.format(submission_period, aol, schedule))
        
    def add_outcome(self, matter, outcome_items):
        """Add an outcome to the file
        Args:
            matter - matter type, e.g. "INVC"
            outcome_items - dictionary of outcome items
        """
        self.lines.append('<outcome matterType="{}">'.format(matter)) 
        for k, v in outcome_items.items() :
            self.lines.append('<outcomeItem name="{}">{}</outcomeItem>'.format(k, v))
        self.lines.append('</outcome>')
        self.lines.append('')
    
    def add_end(self):
        """Add end part of file"""
        self.lines.append("</schedule>")
        self.lines.append("</office>")
        self.lines.append("</submission>")      
        
    def write(self, filename=""):
        """Export contents xml file"""
        if not filename:
            filename = self.filename
        with open(filename, "w") as xmlfile:
            for line in self.lines:
                xmlfile.write(line+"\n")


def unique_str():
    """Create and return unique str by taking Unix time and replacing
    digits with letters A to J"""
    unixtime = str(time.time())
    letters = [chr(65+int(c)) for c in unixtime if c.isdigit()]
    return "".join(letters)


if __name__ == "__main__":

    # Create new submission
    mysub = CWASubmissionMaker()
    mysub.add_top("0W160B", "AUG-2018", "CRIME LOWER", "CRM/0W160B/19")

    # Starting values for an outcome
    outcome_detail = {"CLIENT_FORENAME": "A",
                   "CLIENT_SURNAME": "NOTREAL",
                   "GENDER": "F",
                   "ETHNICITY": "99",
                   "DISABILITY": "UKN",
                   "UFN": "060218/001",
                   "OUTCOME_CODE": "CN04",
                   "CRIME_MATTER_TYPE": "7",
                   "PROFIT_COST": "12.34",
                   "VAT_INDICATOR": "Y",
                   "DISBURSEMENTS_AMOUNT": "0.00",
                   "DISBURSEMENTS_VAT": "0.00",
                   "TRAVEL_COSTS": "7.89",
                   "TRAVEL_WAITING_COSTS": "0.00",
                   "WORK_CONCLUDED_DATE": "20/01/2019",
                   "NO_OF_SUSPECTS": "1",
                   "NO_OF_POLICE_STATION": "1",
                   "POLICE_STATION": "RD026",
                   "DUTY_SOLICITOR": "Y",
                   "YOUTH_COURT": "N",
                   "SCHEME_ID":"1136",
                   "MAAT_ID": "",
                   "DSCC_NUMBER": "180207780A",
                   "PA_NUMBER": ""    
                   }

    # Used in UFN generation
    ufn_day = 1
    ufn_digit = 1

    # Add multiple outcomes with generated surname and UFN
    for i in range(2001):
        outcome_detail["CLIENT_SURNAME"] = unique_str()
        outcome_detail["UFN"] = str(ufn_day).zfill(2) + "0318/" + str(ufn_digit).zfill(3)
        # Update values used to make ufn
        ufn_digit = ufn_digit + 1
        if ufn_digit > 999:
            ufn_digit = 0
            ufn_day +=1
        mysub.add_outcome("INVC", outcome_detail)
        
    # Add end bit to file
    mysub.add_end()
    # Export to file
    mysub.write()
    print("Finished!")
