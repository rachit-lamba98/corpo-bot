#!flask/bin/python
from flask import Flask, jsonify
from splinter import Browser
import json
import pandas as pd

app = Flask(__name__)

@app.route('/scrape/<string:company_name>', methods=['GET'])

def crawl(company_name):
    browser = Browser('chrome')
    browser.driver.minimize_window()
    dataFull = {}
    #Looping through different CA's and scraping data
    caType = ['book', 'board', 'agm', 'egm', 'dividend', 'bonus', 'split', 'rights']
    for purpose in caType:
        browser.visit('https://www.business-standard.com/company/tcs-5400/corporate-action?purpose=' + purpose)
        
#         drop_down = browser.find_by_xpath('//select[@name="purpose"]//option[@value=' + purpose + ']').first
#         drop_down.click()
#         submit_btn = browser.find_by_xpath('//input[@value="SUBMIT"]').first
#         submit_btn.click()

        #reading data from table
        table = browser.find_by_xpath('//*[@id="hpcontentbox"]/div[8]/div[1]/div/div[2]/table/tbody/tr')
        data = [[]]
        for row in table:
            columns = row.find_by_xpath('./td')
            tempList = []
            for cell in columns:
                if(len(cell.find_by_xpath('./span')) == 0):
                    tempList.append(cell.text)
                else:
                    tempList.append(cell.find_by_xpath('./span')[0]['title'])
            data.append(tempList)
       
        if data[2][0] == 'NO RECORD FOUND.':
            data[2][0] = 'NA'
            for _ in range(len(data[1])-1):
                data[2].append('NA')

        df = pd.DataFrame(data=data[2:], columns=data[1])
        df = df.to_json()
        dataFull[purpose] = df
    browser.quit()
    return jsonify(dataFull)

if __name__ == '__main__':
    app.run(debug=True)
