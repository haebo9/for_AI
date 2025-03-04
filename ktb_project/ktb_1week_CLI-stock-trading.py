import time
import pandas as pd
from tabulate import tabulate
from random import choice, randint, uniform

# 주식 종목의 기본값 설정
class Stocks:
    def __init__(self, name, code, price, buy_price=0, return_rate=0, ave_buy=0, up=50, have=0):
        self.code = code
        self.name = name # 주식의 이름
        self.up = up # 상승 확률
        self.have = have # 가지고 있는 주식수
        self.price = price # 주식 현재가
        self.buy_price = buy_price # 구매시점 주식의 총 구매가격
        self.ave_buy = ave_buy # 구매시점 주식의 평단가
        self.return_rate = return_rate # 수익률

    # 매 턴마다 주식 가격의 변동값 지정 (-5% ~ 10%)
    def move_stock_price():
        for i in stock_list:
            i.price = int(i.price*uniform(0.95,  1.1))

    def ave_buy_price():
        for i in stock_list:
            i.ave_buy = int(i.buy_price/max(1,i.have))

    def return_rate_price():
        for i in stock_list:
            i.return_rate = round((i.price-i.ave_buy)*100/ i.ave_buy if i.have > 0 else 0,1)

    def __str__(self):
        return self.name
    

# 이벤트 클래스 생성
class Events:
    def __init__(self, message, target, change):
        self.message = message
        self.target = target
        self.change = change

    def print_msg(curr_event):
        up_dn = ('증가' if curr_event.change >= 0 else '감소')
        return (f'"{curr_event.message}"이(가) 발생했습니다! "{curr_event.target}"의 상승확률이 "{up_dn}"합니다.')

    # 이벤트 발생 확률 설정
    def event_target():
        global stock_list
        target = choice(stock_list)
        e1 = Events('전염성 질병', target.name, -70)
        e2 = Events('부동산 위기설', target.name, -25)
        e3 = Events('반도체 호황설', target.name, 40)
        e4 = Events('달러 가치 상승', target.name, -30)
        e5 = Events('경제 호황', target.name, 60)
        e6 = Events('양적 완화', target.name, 30)
        e7 = Events('무난한 성장', target.name, 10)
        e8 = Events('나스닥 상장', target.name, 70)
        curr_event = choice([e1,e2,e3,e4,e5,e6,e2,e3,e4,e5,e6,e7,e7,e7,e7,e7,e7,e7,e7,e7,e7,e8])
        Events.event_active(target, curr_event)

    # 이벤트를 시작하는 함수
    def event_active(target, curr_event):
        target.up += curr_event.change # 확률 변경
        if target.up > 100: # 상승/하락 결과 계산
            target.up = 100
        elif target.up < 0: # 상승이 target.up 만큼, 하락이 100-target.up
            target.up = 0

        up_dn_100 = choice([1]*(target.up) + [-1]*(100-(target.up)))
        per = up_dn_100*randint(10,30)
        move = target.price*per*0.01
        target.price = int(target.price+move)
        print(f'{Events.print_msg(curr_event)}')
        temp = ('상승' if up_dn_100 ==1 else '하락')
        print(f'"{target.name}"이(가) {per}% "추가{temp}"했습니다.')
        print("- "*30)

    # 보유현금 증가 룰렛을 돌리는 특별이벤트 실행 함수
    def special_event():
        global my_money
        print('=='*30)
        print("!!!특별 현금 룰렛 이벤트 발생!!!")
        if my_money < 10000:
            print("소유한 현금이 부족합니다. 아벤트를 진행할 수 없습니다. **참가비1만원**")
            print('=='*30)
            return

        start = input('진행하시겠습니까? 참가비 1만원 | 예[y], 아니오[n] | :').lower()
        if start == 'y' or start == 'ㅛ':
            my_money -= 10000
            print('@보유 현금 :',my_money)
            print('룰렛 모드를 선택해주세요.')
            luck_ck = input(" | 현금 곱하기(x0.5~3배)[1], 현금보너스(+1~100만원)[2] | :")
            while luck_ck not in ['1','2']:
                print('가능한 선택지 중에 다시 선택해 주세요!') 
                luck_ck = input(" | 현금 곱하기(x0.1~3배)[1], 현금보너스(+1~100만원)[2] | :")
                
            print()

            if luck_ck == '1':
                luck = round(uniform(0.1, 3),1)
                luck_ck = ("축하" if luck > 1 else "ㅠㅠ")
                print(f'=> 당신의 현금자산이 {luck}배가 되었습니다! ({luck_ck})')
                my_money = int(my_money*luck)
            elif luck_ck == '2':
                luck = randint(10000, 1000000)
                print(f'=> 축하합니다! {luck}원의 보너스가 입금되었습니다. ')
                my_money = my_money+luck

            print('@보유 현금 :',my_money)
            print()
            any= (input('확인했습니다. | 네[y] | :'))
            print('=='*30)
        else:
            print()
            any= (input('확인했습니다. | 네[y] | :'))
            print('=='*30)


## 현재 보유 총 자산(주식, 현금) 계산
def money_stock_total():
    global my_money, stock_list

    my_stock = [i.have for i in stock_list]
    stock_price = [i.price for i in stock_list]

    my_stock_price = [a*b for a,b in zip(my_stock,stock_price)]
    my_total = my_money + sum(my_stock_price)
    return my_total

### 성공/실패 결과확인 함수
def success_fail():
    global ck_buy_sell, stock_list
    stock_price = [i.price for i in stock_list]
    my_stock = [i.have for i in stock_list]

    my_total = money_stock_total()
    if my_total >= 5000000:
        print()
        print("=> 성공: 이제는 이곳을 떠나 행복을 찾으시길 바랍니다. ")
        print(' '*9,'^');print(' '*8,'*'*3);print(' '*7,'*'*5);print(' '*5,'*'*9)
        print('--- Made by heabo ---')
        ck_buy_sell = 0

    elif (my_total <= min(stock_price) and max(my_stock)==0):
        print("=> 실패: 더이상 구매할 수 있는 종목이 없습니다. 안녕히가십시오.")
        ck_buy_sell = 0


### 현재 상황판 보여주는 함수
def display_my():
    global my_money, my_total_before, stock_list
    my_total = money_stock_total()
    Stocks.ave_buy_price()
    Stocks.return_rate_price()

    data = {'종목명': [i.name for i in stock_list],
            '가격' : map(lambda x:str(x)+'원',[i.price for i in stock_list]),
            '보유수' : map(lambda x:str(x)+'개',[i.have for i in stock_list]),
            '구매가능' : map(lambda x:str(my_money//x)+'개',[i.price for i in stock_list]),
            '구매평균가' : map(lambda x:str(x)+'원',[i.ave_buy for i in stock_list]),
            '수익률' : map(lambda x:str(round(x,1))+'%',[i.return_rate for i in stock_list])
            }

    display = pd.DataFrame(data, index=[i.code for i in stock_list])
    my_total_rate = round((my_total-my_total_before)*100/my_total_before,1)
    print(tabulate(display, headers='keys', tablefmt='simple', showindex= True))
    print()
    print(f'@보유 현금 : {my_money}원')
    print(f'@총 자산 : {my_total}원({my_total_rate}%)')


# 주식 거래 함수
# 매수 매도 할 주식과 그 수를 입력
def buy_sell():
    global my_money, ck_buy_sell, code_match, stock_list, stock_name

    while True:
        display_my()
        try:
            print('- '*30)
            print('수행할 작업을 입력하시오. ')
            option = int(input(' | 구매[1], 판매[2], 종료[9], 포기하기[119] | :'))
            while option not in [1,2,9,119]:
                print("가능한 선택지 중에 다시 선택해 주세요!")
                option = int(input('  | 구매[1], 판매[2], 종료[9], 포기하기[119] | :'))

            if option == 119:
                print("=> 포기하셨습니다. 대회를 종료합니다.")
                ck_buy_sell = 0
                break

            elif option == 9: # 매매 지속여부 NO
                print('=> 오늘의 매매를 종료합니다.')
                break

            else: # 매매 지속여부 YES
                print('거래할 종목을 고르시오.')
                code = int(input(f' | {stock_name} | :'))
                while code not in [i.code for i in stock_list]:
                    print("가능한 선택지 중에 다시 선택해 주세요!")
                    code = int(input(f' | {stock_name} | :'))

                code_class = code_match[code] # 클래스 인스턴트로 바꿈
                if option == 1: # buy
                    num = int(input('몇개를 구매하시겠습니까? : ')) # 몇개 살지
                    if code_class.price*num <= my_money:
                        code_class.have = code_class.have + num
                        my_money -= code_class.price*num
                        code_class.buy_price = code_class.buy_price+code_class.price*num
                        print("=> 거래가 완료되었습니다.")
                        print("- "*30)
                    else:
                        print('=> 돈이 부족합니다.')
                elif option == 2: # sell
                    num = int(input('몇개를 판매하시겠습니까? : ')) # 몇개 팔지
                    if code_class.have >= num:
                        code_class.have = code_class.have - num
                        my_money += code_class.price*num
                        code_class.buy_price = code_class.buy_price-code_class.ave_buy*num
                        print(f'{code_class}의 구매 총액 : {code_class.buy_price}')
                        print("=> 거래가 완료되었습니다.")
                        print("- "*30)
                    else:
                        print('=> 보유주식이 부족합니다.')
                continue # 거래 다시 진행할지?
        except ValueError:
            print("숫자를 입력하여 주십시오. 다시 실행합니다.")
            continue

# 게임 시작 전 방법 안내
def story():
    text = ["안녕하세요. 천하제일 단타대회에 오신 당신을 환영합니다.",
            "게임방법을 설명드리겠습니다.",
            '. '*10,
            "$ 목표: 100만원 -> 500만원 (30일안에)",
            "$ 과정: 구매or판매 -> 종목선택 -> 수량선택",
            "$ 이벤트: 매일 한번 추가 상승or하락이 발생",
            '. '*10,
            "그럼 성공 투자 하십시오."]
    print("="*60)
    for t in text:
        print(t)
        time.sleep(0.5)


# 출력 가능한 힌트 모음
def hint():
    hints = ['***주식이 오른데는 다 이유가 있습니다.***',
             "***전염병은 엄청난 주가의 하락을 가져올 수 있습니다.***",
             '***특별 현금 이벤트를 위해서 현금을 모아두는 것이 좋습니다.***',
             '***나스닥 상장은 우리에게 희망을 줍니다.***',
             '***가끔은 아무것도 하지 않는 편이 낫습니다.***',
             '***지나친 조언은 개발자를 화나게 합니다.***',
             '***무리한 투자는 인생을 신나게 합니다.***',
             '***모든 일에 완전한 우연은 없습니다.***'
            ]
    return choice(hints)

# 주식 이름과 코드 모음
def stock_name_code():
    global stock_list
    name_code = ''
    for i in stock_list:
        name_code += i.name+'['+str(i.code)+']'+' '
    return name_code

def main():
    global my_money, ck_buy_sell, my_total_before
    story() # 시작 설명 멘트 안내

    # 턴을 하나씩 돌며, 이벤트 발생시킴
    tern = 0
    spe1, spe2, spe3 = randint(5, 9), randint(10, 19), randint(20, 28)

    while tern != 30 and ck_buy_sell == 1:
        tern += 1
        my_total = money_stock_total()
        my_total_before = my_total # before값 갱신

        print()
        print("="*60)
        print(f'<<<{tern}번째 날이 밝았습니다.{30-tern}일 남았습니다.>>>')
        Stocks.move_stock_price() # 주식의 기본 변동값 설정
        Events.event_target() # 무작위 이벤트 발생

        if tern in [5, 10, 15, 20, 25]: print(hint())
        elif tern in [8, 13]: print(hint())
        elif tern in [spe1, spe2, spe3]: Events.special_event()

        buy_sell() # 매수매도 반복 진행
        success_fail() # 성공/실패 요건 달성 확인

    else:
        if ck_buy_sell == 1:
            display_my()
            print("=> 실패: 시간이 종료되었습니다.")
            print(f'당신의 총 자산은 : {my_total}')
            
#######################################################
#######################################################
# 주식 인스턴스 설정
A = Stocks('구름식품',1,randint(3000, 30000))
B = Stocks('카카오반도체',2,randint(3000, 30000))
C = Stocks('판교뱅크',3,randint(3000, 30000))
D = Stocks('부트바이오',4,randint(3000, 30000))
E = Stocks('유스페이스건설', 5, randint(3000, 30000))

# 초기 자산값
my_money = 1000000
my_total_before = 1000000
ck_buy_sell = 1
code_match = {1:A, 2:B, 3:C, 4:D, 5:E} # 종목 코드 -> Stocks 인스턴트]
stock_list = list(code_match.values()) # 종목 리스트
stock_name = [i.name for i in stock_list]
stock_name = stock_name_code()

# 실행 함수
if __name__ == __name__:
    main()