from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

from flask import Flask, request

from webdriver_manager.chrome import ChromeDriverManager


import time

app = Flask(__name__)


def download_selenium():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--ignore-certificate-errors")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

# options = Options()
# options.add_argument("--headless") 
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-gpu")
# options.add_argument("--disable-dev-shm-usage")

# service = Service(executable_path="chromedriver.exe")
# driver = webdriver.Chrome(service=service, options=options)


# options = Options()
# options.add_argument("--headless")

def find_url():
    driver = download_selenium()
    driver.get("https://www.seir-sanduk.com/linkzagledane.php")
    time.sleep(5)
    url = driver.current_url
    if url.startswith("https://www.seir-sanduk.com/?pass"):
        print(url)
        return {"url": url}
    else:
        driver.get("https://www.otustanausta.com/search.php?keywords=%D0%B4%D0%BE%D0%B1%D0%B0%D0%B2%D0%B5%D0%BD%D0%BE+%D0%BE%D1%82+%D0%BC%D0%BE%D0%B4%D0%B5%D1%80%D0%B0%D1%82%D0%BE%D1%80")
        time.sleep(5)
        consent_button = driver.find_element(By.CLASS_NAME, "fc-cta-consent")
        consent_button.click()

        time.sleep(5)
        post = driver.find_elements(By.CLASS_NAME, "postbody")

        post = post[0].find_element(By.TAG_NAME, "a").get_attribute("href")
        if post.startswith("https://www.otustanausta.com/"):
            driver.get(post)
            time.sleep(5)

            # content = driver.find_element(By.CLASS_NAME, "content")

            final_links = driver.find_elements(By.TAG_NAME, "a")
            for link in final_links:

                if link.get_attribute("href") and link.get_attribute("href").startswith("https://www.seir-sanduk.com/linkzagledane.php?parola="):
                    print(link.get_attribute("href"))
                    return {"url": link.get_attribute("href")}
                    break

@app.route('/', methods=['GET','POST'])
def home():

    if request.method == 'POST':
        result = find_url()
        if result and 'url' in result:
            return f'''
                <html>
                    <head>
                        <title>Found URL</title>
                        <meta name="viewport" content="width=device-width, initial-scale=1">
                        <style>
                            .container {{
                                display: flex;
                                justify-content: center;
                                align-items: center;
                                height: 100vh;
                                text-align: center;
                            }}
                            .link {{
                                font-size: 24px;
                                padding: 20px;
                                background-color: #4CAF50;
                                color: white;
                                text-decoration: none;
                                border-radius: 10px;
                                max-width: 80%;
                                word-wrap: break-word;
                            }}
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <a href="{result['url']}" class="link" target="_blank">Click here to open the link</a>
                        </div>
                    </body>
                </html>
            '''
    else:
        return '''
            <html>
                <head>
                    <title>Find URL</title>
                    <meta name="viewport" content="width=device-width, initial-scale=1">
                    <style>
                        .container {
                            display: flex;
                            flex-direction: column;
                            justify-content: center;
                            align-items: center;
                            height: 100vh;
                            text-align: center;
                        }
                        .button {
                            font-size: 24px;
                            padding: 20px 40px;
                            background-color: #4CAF50;
                            color: white;
                            border: none;
                            border-radius: 10px;
                            cursor: pointer;
                        }
                        #loading {
                            display: none;
                            margin-top: 20px;
                            font-size: 18px;
                        }
                    </style>
                    <script>
                        function showLoading() {
                            document.getElementById('loading').style.display = 'block';
                            document.getElementById('submitBtn').style.display = 'none';
                        }
                    </script>
                </head>
                <body>
                    <div class="container">
                        <form method="post" onsubmit="showLoading()">
                            <button type="submit" class="button" id="submitBtn">Find URL</button>
                        </form>
                        <div id="loading">
                            Loading... This may take up to 30 seconds<br>
                            <progress></progress>
                        </div>
                    </div>
                </body>
            </html>
        '''
        
    

    # if request.method == 'GET':
        # return find_url()


if __name__ == "__main__":
    app.run(debug=True, port=3000)