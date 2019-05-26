# woowacourse-lunch-slackBot
우아한테크코스 슬랙채널에서 사용할 점심 추천 슬랙봇 개발 프로젝트

## 기능 목록
   * Jumsimbot class 구현 
     - 사용자로부터 '밥!' 요청을 받아야 합니다.
     - 사용자 요청에 따라 Restaurant Repository로부터 식당 정보를 
       받아와야 합니다.
     - 받아올 식당들의 key를 랜덤하게 뽑아야 합니다.
   * Restaurant Repository class 구현
     - 받아온 식당 정보를 사용하기 편한 형태로 가공해야 합니다.
     - 가공한 데이터를 저장해두어야 합니다.
     - primary key를 통해 저장해 놓은 데이터 중 원하는 식당 정보를
       찾아 되돌려줄 수 있어야 합니다.
     - primary key를 통해 저장해 놓은 데이터에 접근해 따봉 숫자를
       수정할 수 있어야 합니다.
     - 어떤 식당들의 따봉 숫자가 새로 수정되었는지 기억하고 있어야
       합니다.
   * GSpreadClient 구현
     - google spread sheet로부터 모든 식당 정보를 받아와야 합니다.
     - google spread sheet에 원하는 정보를 업데이트할 수 있어야 합니다.
   * Time Stamp Id table 구현
     - 사용자에게 되돌려준 response의 식당 정보와 Time stamp를
       Mapping해 기억하고 있어야 합니다.
     - Time stamp를 이용해 식당 정보의 primray key를 찾아주어야 합니다.
     - 가장 최신 response의 time stamp 뿐만 아니라 일정 개수의 과거
       response에 대해서도 time stamp와 primary key 쌍을 기억해 
       두어야 합니다.

## TODO
- logger를 통해 서버에 이상이 생긴 경우 원인을 파악할 수 있어야 합니다.
- jenkins를 통한 자동 배포를 할 수 있을지 고민해보아야 합니다.