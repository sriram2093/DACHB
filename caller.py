# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 13:29:59 2015

@author: sriram
"""

import xlrd
from xlwt import Workbook, easyxf



articleDictionary = {};
preBallotDictionary = {};
postBallotDictionary = {};
preImplementationDictionary = {};
postImplementationDictionary = {};

summaryList = [];
summaryDictionary = {};

def main():
    
    
    global summaryList,summaryDictionary,postImplementationDictionary
    wordMinFrequency = 3
    summaryNoOfLines = 5
    
    import FileReadProcess
    print "calling the filereader to read ArticleIndex.xlsx"
    path = "C:\Users\sriram\Documents\Python Scripts\ArticleIndex.xlsx"
    
    #reading the excel sheet and populating article dictionary
    excelFileReader(path)
    
    #reading the article dictionary and splitting into preballot, postballot, pre-implementation and post-implementation articles.
    timePeriodbasedArticles()
    #print preBallotDictionary.items()
    
    # 1 if article, 2 if comment
    articleSummary = FileReadProcess.mmain(articleDictionary,wordMinFrequency,summaryNoOfLines,1)
    
    print "\n\n ---------summary---------\n\n"
    print articleSummary
        
    summaryDictionary[FileReadProcess.mmain(preImplementationDictionary,wordMinFrequency,summaryNoOfLines,1)] = FileReadProcess.mmain(preImplementationDictionary,wordMinFrequency,summaryNoOfLines,2)
    summaryDictionary[FileReadProcess.mmain(postImplementationDictionary,wordMinFrequency,summaryNoOfLines,1)]= FileReadProcess.mmain(postImplementationDictionary,wordMinFrequency,summaryNoOfLines,2)
    summaryDictionary[FileReadProcess.mmain(preBallotDictionary,wordMinFrequency,summaryNoOfLines,1)]=FileReadProcess.mmain(preBallotDictionary,wordMinFrequency,summaryNoOfLines,2)
    summaryDictionary[FileReadProcess.mmain(postBallotDictionary,wordMinFrequency,summaryNoOfLines,1)]=FileReadProcess.mmain(postBallotDictionary,wordMinFrequency,summaryNoOfLines,2)
    
    
    wb = Workbook()
    ws = wb.add_sheet('Time Period based summarization')
    ws.write(0,0,'TimePeriod')
    first_col = ws.col(1)
    first_col.width = 256 * 20
    ws.write(0,1,'Article Summary')
    second_col = ws.col(2)
    second_col.width = 256 * 20
    ws.write(0,2,'Comments Summary')
    ws.col(0).width = len('Article Number') * 256
    #ws.col(1).width = max([len(l) for l in lines]) * 256
    #ws.col(2).width = max([len(l) for l in lines]) * 256
    r = 1
    for k,v in summaryDictionary.items():
        #print i;
        ws.write(r,0,r)
        #fileReadProcess.mmain returns the summary
        ws.write(r,1,k)
        ws.write(r,2,v)
        wb.save('Summary.xls')
        if r is 10: 
            break
        r=r+1
    wb.save('Summary.xls')
    print 'Wrote Summary.xls'
    
    summaryDictionary = {}
    
    ws2 = wb.add_sheet('Article wise Summarization')
    
    tempDictionary={}
    
    for k in articleDictionary.keys():
        tempDictionary[k]=articleDictionary.get(k)
        summaryDictionary[FileReadProcess.mmain(tempDictionary,wordMinFrequency,summaryNoOfLines,1)] = FileReadProcess.mmain(tempDictionary,wordMinFrequency,summaryNoOfLines,2)
        tempDictionary = {}
    
    r = 1
    for k,v in summaryDictionary.items():
        #print i;
        ws2.write(r,0,r)
        #fileReadProcess.mmain returns the summary
        ws2.write(r,1,k)
        ws2.write(r,2,v)
        wb.save('Summary.xls')
        r=r+1

def excelFileReader(path):
    print "reading excel file"
    book = xlrd.open_workbook(path)
    # print number of sheets
    #print book.nsheets
    # print sheet names
    #print book.sheet_names()
    # get the first worksheet
    first_sheet = book.sheet_by_index(0)
    
    # read a row
    #print first_sheet.row_values(0)
    # read a cell
    #cell = first_sheet.cell(0,7)
    #print cell
    #print cell.value
        
    for i in range(100):
        if i==0 : continue
        #print first_sheet.cell(i,7).value
        articleDictionary[int(first_sheet.cell(i,7).value)] = first_sheet.cell(i,8).value; # Add new entry
    #print articleDictionary.items()
    
    
def timePeriodbasedArticles():
    global preBallotDictionary,postBallotDictionary,preImplementationDictionary, postImplementationDictionary
    from datetime import datetime
    
    #pre ballot period jan 1st 2014 to nov 4th 2014.
    preBallotStart = datetime.strptime("01/01/2014" , '%d/%m/%Y')
    preBallotEnd = datetime.strptime("04/11/2014" , '%d/%m/%Y')
    
    #post ballot period nov 4th 2014 to jan 31st 2015.
    postBallotStart = datetime.strptime("04/11/2014" , '%d/%m/%Y')
    postBallotEnd = datetime.strptime("31/01/2015" , '%d/%m/%Y')
    
    #pre-implementation period : jan 1st 2014 to jan 1st 2015.
    preImplStart = datetime.strptime("01/01/2014" , '%d/%m/%Y')
    preImplEnd = datetime.strptime("01/01/2015" , '%d/%m/%Y')
    
    #post-implementation period : jan 1st 2015 to jan 31st 2015.
    postImplStart = datetime.strptime("01/01/2015" , '%d/%m/%Y')
    postImplEnd = datetime.strptime("31/01/2015" , '%d/%m/%Y')
    
    for article in articleDictionary:
        try:
            articleDate = datetime.strptime(str(articleDictionary[article]) , '%d/%m/%Y')
            #print articleDate
            if (articleDate>preBallotStart and articleDate<preBallotEnd):
                preBallotDictionary[article]=articleDate
                # "preBallotPeriod"
            if (articleDate>postBallotStart and articleDate<postBallotEnd):
                postBallotDictionary[article]=articleDate
                # "postBallotPeriod"
            if (articleDate>preImplStart and articleDate<preImplEnd):
                preImplementationDictionary[article]=articleDate
                # "pre Implementation period"
            if(articleDate>postImplStart and articleDate<postImplEnd):
                postImplementationDictionary[article]=articleDate
                # "post Implementation period"
        except ValueError:
            continue

    
main()


    