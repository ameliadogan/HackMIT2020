import pandas as pd
import dateutil.parser as dparser
import datetime
import re

'''
uses regex to identify dates or make them unclear
'''
def date_parser(report_info):
    try:
        date_format = r"(\d{1,2}-\d{1,2}-\d{2,4})"
        date = re.search(date_format, report_info)
        date = str(date.groups()[0])
        if date == "2-29-18":
            date = "03-01-18"
        return date

    except:
        return "Unclear"
complaint_data = pd.read_csv('data/ppd_complainant_demographics.csv')
complaint_outcome = pd.read_csv('data/ppd_complaint_disciplines.csv')

#recast indian, middle east to other race category
complaint_data = complaint_data.replace('indian', 'other')
complaint_data = complaint_data.replace('middle east', 'other')
complaint_data = complaint_age.replace(-1, )

#replace nan values to unreported
complaint_data['complainant_race'].fillna('unreported', inplace = True)
complaint_data['complainant_sex'].fillna('unreported', inplace = True)
complaint_outcome['po_sex'].fillna('unreported', inplace = True)
complaint_outcome['po_race'].fillna('unreported', inplace = True)


#identify dates
complaint_reports = pd.read_csv('data/ppd_complaints.csv')
complaint_reports['incident_date'] = complaint_reports['summary'].apply(lambda x: date_parser(x) )


#merge datasets
complaint_reports = complaint_reports.merge(complaint_data, on = 'complaint_id')
complaint_reports = complaint_reports.merge(complaint_outcome, on = 'complaint_id')

complaint_reports.to_csv('data/complaint_clean_merged.csv')