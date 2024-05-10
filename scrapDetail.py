from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from datetime import datetime
import time
from selenium.webdriver.common.action_chains import ActionChains
import json

def scrape_and_save(url, filename):
    # 현재 날짜 가져오기
    current_date = datetime.now().strftime("%Y-%m-%d")
    folder_path = "scrapList"
    # 파일 경로 생성
    filename = f"{folder_path}/{filename}_{current_date}.json"
    userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

    options = ChromeOptions()
    options.add_argument("user-agent=" + userAgent)
    options.add_argument("--headless")
    #service = ChromeService(executable_path=ChromeDriverManager().install())
    browser = webdriver.Chrome(options=options)
    browser.get(url)

    # 페이지가 완전히 로드될 때까지 대기
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "list"))
    )

    # 스크롤을 최하단으로 이동하고 ".more" 버튼을 클릭하여 추가 콘텐츠를 로드하는 함수 정의
    def scroll_and_click_more(browser):
        while True:
            # 현재 브라우저의 높이 가져오기
            last_height = browser.execute_script("return document.body.scrollHeight")
            # 스크롤을 최하단으로 이동
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # 스크롤이 완료될 때까지 대기
            time.sleep(1)  # 적절한 대기 시간을 선택합니다.
            try:
                # ".more" 버튼 요소 찾기
                more_button = browser.find_element(By.CSS_SELECTOR, ".more")
                # ".more" 버튼이 존재하면 클릭하고, 그렇지 않으면 반복문을 종료
                if more_button:
                    more_button.click()
                    # 스크롤 후에 페이지가 업데이트되어 더 이상 스크롤이 필요하지 않을 때까지 반복
                    while True:
                        # 새로운 높이 가져오기
                        new_height = browser.execute_script("return document.body.scrollHeight")
                        if new_height == last_height:
                            break
                        last_height = new_height
                        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(1)  # 적절한 대기 시간을 선택합니다.
                else:
                    break
            except NoSuchElementException:
                break

    # 스크롤을 최하단으로 이동하고 ".more" 버튼을 클릭하여 추가 콘텐츠를 로드
    scroll_and_click_more(browser)

    def scroll_to_element(element):
        browser.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'start', inline: 'nearest'});", element)
        browser.execute_script("window.scrollBy(0, -100);")


    card_detail_url_box= browser.find_elements(By.CLASS_NAME , "preview")

    card_detail_urls  = [url.find_element(By.TAG_NAME , "a").get_attribute('href') for url in card_detail_url_box]

    card_detail_info = []
    
    for url in card_detail_urls:
        browser.get(url)
        time.sleep(2)

        page_source = browser.page_source
        soup = BeautifulSoup(page_source, 'html.parser')  

        dtlBtns = browser.find_elements(By.CSS_SELECTOR , ".Benefits .details")

        cardName = soup.select_one(".cardname .txt").text.strip()
        search_box = soup.select(".cardinfo .list")
        for list in search_box:
            cardTitle = browser.find_element(By.CSS_SELECTOR , ".BaseInfo .cardname .txt").text.strip()
            cardAnnualFee = list.select_one(".as_annualFee").text.strip()
            cardBasePerformance = list.select_one(".as_baseRecord").text.strip()
            cardSummaryInfo = list.select(".cardinfo .list .desc:last-child .txt")

            if(len(cardSummaryInfo) > 1):
                cardSummary = " ".join(summary.text.strip() for summary in cardSummaryInfo)
            
            cardBtnUrl = browser.find_element(By.CSS_SELECTOR , ".BaseInfo .cardinfo .btns .apply").get_attribute("href")

            BenefitsTitle = browser.find_element(By.CSS_SELECTOR , ".Benefits .title").text

        for i in range(len(dtlBtns)):
          btn = dtlBtns[i]
          
          print("btn is clicked")
            
          action_chains = ActionChains(browser)
        
          action_chains.move_to_element(btn).click().perform()
          

          time.sleep(3)
          
          browser.execute_script("arguments[0].click();", btn)


          time.sleep(3)  # 요소가 로드되는 동안 대기

          if i < len(dtlBtns) - 1:
            next_btn = dtlBtns[i + 1]
            scroll_to_element(next_btn)
            time.sleep(3)  # 스크롤 완료 대기

        summaryInfo = []
        summaryTitles = {}
        openDtls = browser.find_elements(By.CSS_SELECTOR , ".Benefits .details[open]")

        for dtl in openDtls:
            # 각 detail 요소에서 필요한 정보 추출
            dtlTitles = dtl.find_elements(By.CSS_SELECTOR , ".Benefits .detail>.list .detail_title")
            dtlDesc = dtl.find_elements(By.CSS_SELECTOR , ".Benefits .detail>.list>.desc")
            dtlDescText = "\n".join([desc.text.strip() for desc in dtlDesc])
            summaryTitles = []
            for title in dtlTitles:
                summaryTitles.append(title.text.strip())
            
            summaryInfo.append({
                "summaryTitles" : summaryTitles,
                "summaryDescs" : dtlDescText
            })
        print(cardName)
        card_detail_info.append({
            "cardName" : cardName ,
            "cardTitle" : cardTitle , 
            "cardAnnualFee" : cardAnnualFee,
            "cardBasePerformance" : cardBasePerformance , 
            "cardSummary" : cardSummary ,
            "cardBtnUrl" : cardBtnUrl , 
            "BenefitsTitle" : BenefitsTitle ,
            "summaryInfo" : summaryInfo
        })
    

    # # 데이터를 JSON 파일로 저장
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(card_detail_info, f, ensure_ascii=False, indent=4)
    
    # 5초 동안 대기
    time.sleep(5)
    # 브라우저 종료
    browser.quit()

scrape_and_save("https://card-search.naver.com/list?sortMethod=ri&ptn=2&bizType=CPC&companyCode=&brandNames=&benefitCategoryIds=&subBenefitCategoryIds=&affiliateIds=&minAnnualFee=0&maxAnnualFee=0&basePayment=0", "scrapCardDetail")
