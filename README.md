# 신용카드 리스트 사이트 데이터 수집
1. 사이트는 [네이버](https://naver.com)사이트에서 지원하는 신용카드 데이터를 가져왔습니다.   각 카드사의 카테고리를 클릭한 url 정보는 아래와 같습니다.
  + [신한카드](https://card-search.naver.com/list?companyCode=SH&brandNames=&sortMethod=ri&isRefetch=true&bizType=CPC)
  + [현대카드](https://card-search.naver.com/list?companyCode=HD&brandNames=&sortMethod=ri&isRefetch=true&bizType=CPC)
  + [삼성카드](https://card-search.naver.com/list?companyCode=SS&brandNames=&sortMethod=ri&isRefetch=true&bizType=CPC)
  + [국민카드](https://card-search.naver.com/list?companyCode=KB&brandNames=&sortMethod=ri&isRefetch=true&bizType=CPC)
  + [롯데카드](https://card-search.naver.com/list?companyCode=LO&brandNames=&sortMethod=ri&isRefetch=true&bizType=CPC)
  + [하나카드](https://card-search.naver.com/list?companyCode=SK&brandNames=&sortMethod=ri&isRefetch=true&bizType=CPC)
  + [우리카드](https://card-search.naver.com/list?companyCode=WR&brandNames=&sortMethod=ri&isRefetch=true&bizType=CPC)
  + [농협카드](https://card-search.naver.com/list?companyCode=NH&brandNames=&sortMethod=ri&isRefetch=true&bizType=CPC)
  + [기업카드](https://card-search.naver.com/list?companyCode=IB&brandNames=&sortMethod=ri&isRefetch=true&bizType=CPC)

2. 모든 정보를 모아 수집할 수 있었지만 그렇게하면 자료를 분리하는데 불편함이 있어 각 카테고리별 url을 분류해 수집하였습니다.
  
3. 수집에 사용한 언어는 `python`이며 `selenium`과`webdriver`를 사용해 수집하였습니다.   `python`으로 수집된 데이터는 아래와 같습니다.
  + 카드 명칭
  + 카드 연회비
  + 카드 요약 혜택
  + 카드 이미지
