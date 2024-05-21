from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
import time

from flask import Flask, request, jsonify
opts = ChromeOptions()
opts.add_argument("--headless=new")
opts.page_load_strategy = 'eager'

def google_search(num_result, query):
    prefix = 'https://www.google.com/search?q='
    contents = query.split(' ')
    suffix = '+'.join(contents)
    url = prefix+suffix

    driver = webdriver.Chrome(options=opts)
    driver.implicitly_wait(1)

    driver.get(url)

    origin = ScrollOrigin.from_viewport(0, 0)

    while True:
        results = driver.find_elements(By.CLASS_NAME, 'g')
        if len(results) >= num_result:
            break
        else:
            time.sleep(1)
            ActionChains(driver).scroll_from_origin(origin, 0, 400).perform()
            try:
                more_button = driver.find_element(By.CSS_SELECTOR, '.T7sFge')
                more_button.click()
            except:
                continue

    output = []
    for result in results[:num_result]:
        dic = {}
        headline = result.find_element(By.TAG_NAME, 'h3')
        domain = result.find_element(By.TAG_NAME, 'cite')
        url = result.find_element(By.TAG_NAME, 'a')
        spans = result.find_elements(By.TAG_NAME, 'span')

        s_text = [s.text for s in spans]
        domain_part = domain.text.split('›')
        if ' ...' in domain_part:
            domain_part.remove(' ...')

        dic['title'] = str(headline.text)
        dic['tags'] = domain_part
        dic['url'] = str(url.get_attribute('href'))
        dic['description'] = str(s_text[-1])
        dic['time'] = str(s_text[-2])
        output.append(dic)

    driver.quit()   
    return output

app = Flask(__name__)

@app.route('/', methods = ["GET"])
def welcome():
    return "Hello"

@app.route('/googlesearch', methods = ["POST"])
def googlesearch():
    data = request.get_json()
    num_results = data['num_result']
    query = data['query']
    outputs = google_search(num_results, query)

    return jsonify(outputs), 200

if __name__=="__main__":
    app.run(debug= True)

# def main():
#     # query = input("Input your query: ")
#     query = 'iran president death'
#     # num_result = int(input("Enter number of results you want: "))
#     num_result = 5
#     prefix = 'https://www.google.com/search?q='
#     contents = query.split(' ')
#     suffix = '+'.join(contents)
#     url = prefix+suffix

#     output = google_search(num_result, url)
#     print(output)















