#!/usr/bin/env python

import xlsxwriter
import datetime
from thehive4py.api import TheHiveApi
from thehive4py.query import Eq

### variables ###
api_key = "xxx"
url = "http://192.168.1.46:9000"
excel_path = "Incidents_{}.xlsx".format(str(datetime.date.today()).replace("-", "_"))

query = {}
# If need only a type decomment next line
# query = Eq('dataType', 'mail')
#################

def main():
    api = TheHiveApi(url, api_key)
    cases = api.find_cases(range="all")
    cases = cases.json()

    workbook = xlsxwriter.Workbook(excel_path)
    worksheet = workbook.add_worksheet()

    bold = workbook.add_format({"bold": True})
    worksheet.write("A1", "TheHive ID", bold)
    worksheet.write("B1", "CaseID", bold)
    worksheet.write("C1", "Status", bold)
    worksheet.write("D1", "Title", bold)
    worksheet.write("E1", "Date", bold)
    worksheet.write("F1", "Owner", bold)
    worksheet.write("G1", "TLP", bold)
    worksheet.write("H1", "Tag", bold)

    row = 1
    for item in cases:
        item_id = item["id"] if "id" in item.keys() else item["_id"]
        worksheet.write(row, 0, item_id)
        worksheet.write(row, 1, item["caseId"])
        worksheet.write(row, 2, item["status"])
        worksheet.write(row, 3, item["title"])
        worksheet.write(
            row,
            4,
            datetime.datetime.fromtimestamp(item["startDate"] / 1000).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
        )
        worksheet.write(row, 5, item["owner"])
        worksheet.write(row, 6, item["tlp"])
        worksheet.write(row, 7, ",".join(item["tags"]))
        row += 1

    worksheet2 = workbook.add_worksheet()

    worksheet2.write("A1", "TheHive ID")
    worksheet2.write("B1", "Observable DataType")
    worksheet2.write("C1", "Observable Value")
    worksheet2.write("D1", "IOC")
    row = 1
    for item in cases:
        item_id = item["id"] if "id" in item.keys() else item["_id"]
        obs = api.get_case_observables(
            item_id, query=query, sort=["-startDate", "+ioc"], range="all"
        )
        obs = obs.json()
        for ob in obs:
            worksheet2.write(row, 0, item["caseId"])
            worksheet2.write(row, 1, ob["dataType"])
            if ob["dataType"] != "file":
                worksheet2.write(row, 2, ob["data"])
            else:
                worksheet2.write(row, 2, ",".join(ob["attachment"]["hashes"]))
            worksheet2.write(row, 3, True if ob["ioc"] == 1 else False)
            row += 1
    workbook.close()


if __name__ == "__main__":
    print("[INFO] Starting the script...")
    main()
    print("[INFO] No errors found. Output file generated successfully")
    print("[INFO] Program terminated. Exiting...")
