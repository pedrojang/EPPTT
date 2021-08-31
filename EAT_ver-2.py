import ccxt 
import pandas as pd 
import time
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

apiKey = 'Y3dcAaJ0BtLZdQpk9YTryEaft7wQQNMPZc7UJcZAGLKRbDFbtvw2GkRGVeadkvsL'
secKey = 'DA9aVE2d9fs7QWL6YfDs7Q3mJYHblnhJoPdO4tWjbDw4kGJCXviTSlZNroF99Dk9'



lastBol_low = 0.0
lastBol_high = 0.0
binanceFUTURE = ccxt.binance(config={
    'apiKey': apiKey,
    'secret': secKey,
    'enableRateLimit': True, 
})

binanceFR = ccxt.binance(config={
    'apiKey': apiKey, 
    'secret': secKey,
    'enableRateLimit': True,
    'options': {
        'defaultType': 'future'
    }
})

markets = binanceFR.load_markets()
symbol = "ETH/USDT"
market = binanceFR.market(symbol)
leverage = 30

resp = binanceFR.fapiPrivate_post_leverage({
    'symbol': market['id'],
    'leverage': leverage
})


balance = binanceFUTURE.fetch_balance(params={"type": "future"})


def btcc():
    btc = binanceFR.fetch_ohlcv(
        symbol="ETH/USDT", 
        timeframe='5m', 
        since=None, 
        limit=2)


    return btc

def GetPD():
    dff = pd.DataFrame(btcc(), columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
    dff['datetime'] = pd.to_datetime(dff['datetime'], unit='ms')
    dff['dec'] = dff['high'] - dff['low']
    dff['RD'] = dff['close'] - dff['open']
    dff.set_index('datetime', inplace=True)
    return dff

# 고가 - 저가 
def getdec():

    lst = GetPD().dec.tolist()
    return lst

# 시가 - 종가 리스트
def getRD():
    lst = GetPD().RD.tolist()
    return lst

# 시가
def getopen():

    lst = GetPD().open.tolist()
    return lst
# 종가 
def getclose():

    lst = GetPD().close.tolist()
    return lst
# 고가
def gethigh():
    lst = GetPD().high.tolist()
    return lst
#저가 
def getlow():
    lst = GetPD().low.tolist()
    return lst
# text = 본문 / PN = 현재 포지션 -
def mail(text,PN):
    now = datetime.now()
    
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login('pedrojang777@gmail.com','mpgzxiggfdjbarqz')

    msg =  MIMEText(text)
    msg['Subject'] = PN + str(now)

    s.sendmail('pedrojang777@gmail.com','peter000520@naver.com',msg.as_string())

    s.quit()
# 선물 계좌 구하기 
def BGDF():
    balance = binanceFUTURE.fetch_balance(params={"type": "future"})

    return balance['USDT']['free']
# 현재가 구하기
def getcurrent():
    symbol = "ETH/USDT"
    btc = binanceFR.fetch_ticker(symbol)
    return btc['last']
# 현재 분 -
def nownow():
    now = datetime.now().minute

    return now

# 현재 시 -
def nowhour():
    NH = datetime.now().hour

    return NH

def amountgetter():
    money = BGDF()
    if BGDF() > 20000:
        money = 20000
    amountget = round(money/getcurrent(),6)*0.98
    return amountget

def timeline():
    answer = nowhour() >= 0
    return answer

#롱 - 풀매수 -
def buybit(a):
    order = binanceFR.create_market_buy_order(
    symbol=symbol,
    amount=a*leverage,
)

#숏 - 풀매도 -
def sellbit(a):
    order = binanceFR.create_market_sell_order(
    symbol=symbol,
    amount=a*leverage,
)

def mail(text,PN):
    now = datetime.now()
    
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login('pedrojang777@gmail.com','mpgzxiggfdjbarqz')

    msg =  MIMEText(text)
    msg['Subject'] = PN + str(now)

    s.sendmail('pedrojang777@gmail.com','peter000520@naver.com',msg.as_string())

    s.quit()

LongPossition = False
ShortPossition = False
nowH = -1
PM = 0.003
PM_S = 0.003
K_value = 0.35
StartMoney = BGDF()
reportdone = False
Chance15 = True
RED = False
while True:
    try:
        if timeline() == True:
            btcc()
            getcurrent()
            if 55 < nownow() < 60 and nowhour() == 23 :
                if reportdone == False:
                    PYD = BGDF()/StartMoney
                    TEXT = 'yesterday profit was... ' + str(PYD) +'\n you can put in or out money untill 23:59:59'
                    PN = 'Profit Yester Day'
                    mail(TEXT,PN)
                    StartMoney = BGDF()
                    reportdone = True
                    print('start new day...start money is '+str(StartMoney)+'...now: '+ str(datetime.now()))
                    RED = False
                StartMoney = BGDF()
            elif BGDF()/StartMoney < 1.4:
                reportdone = False
                if not(nowH == nownow()//5):
                    if LongPossition == True:
                        buybit(Longamount)
                        LongEndPrice = getcurrent()
                        time.sleep(1)
                        profit = round(BGDF()/StartMoney*100,2)
                        TEXT = 'SHORT POSSITION END... at:'+ str(LongEndPrice) +'\n profit:'+str(profit) + '\n deposit = ' + str(BGDF())
                        PN = 'SHORT POSSITION END '
                        mail(TEXT,PN)
                        print('2 |Long possition END'+'...now: '+ str(datetime.now()))
                        LongPossition = False
                    if ShortPossition == True:
                        sellbit(Shortamount)
                        ShortEndPrice = getcurrent()
                        time.sleep(1)
                        profit = round(BGDF()/StartMoney*100,2)
                        TEXT = 'LONG POSSITION END... at:'+ str(ShortEndPrice) +'\n profit:'+str(profit) + '%' + '\n deposit = ' + str(BGDF())
                        PN = 'LONG POSSITION END '+'Time:'
                        mail(TEXT,PN)
                        print('2N|Short possition END'+'...now: '+ str(datetime.now()))
                        ShortPossition = False
                    print('recycle 30min')
                    nowH = nownow()//5
                    chance15 = True
                RD =getRD()
                DEC = getdec()
                OPEN = getopen()
                CLOSE = getclose()
                HIGH = gethigh()
                LOW = getlow()

                    # 롱 잡기 
                if 1 < nownow()%5  and RD[0] > 0 and LOW[1] > ((OPEN[0]+CLOSE[0])/2) and getcurrent() > OPEN[1] + (RD[0]/2) and LongPossition == False and ShortPossition == False and chance15 == True:
                    Longamount = amountgetter()
                    sellbit(Longamount)
                    #Fbuyprice = OPEN[1] + (RD[0]/2)
                    buyprice = getcurrent()
                    LongPossition = True
                    time.sleep(1)
                    TEXT = 'SHORT POSSITION \n'+ str(Longamount) +'X'+ str(leverage)+'...'+'bought at'+ str(buyprice)
                    PN = 'SHORT Possition '
                    mail(TEXT,PN)
                    print('long possition'+ str(nowhour())+':'+str(nownow())+'...now: '+ str(datetime.now()))
                    chance15 = False
                    # 롱 정리 
                # elif 0 < nownow()%5 and LongPossition == True and ShortPossition == False:
                #     buybit(Longamount)
                #     LongEndPrice = getcurrent()
                #     LongPossition = False
                #     profit = round(BGDF()/StartMoney*100,2)
                #     time.sleep(1)
                #     TEXT = 'SHORT POSSITION END... at:'+ str(LongEndPrice) +'\n profit:'+str(profit) + '\n deposit = ' + str(BGDF())
                #     PN = 'SHORT POSSITION END '
                #     mail(TEXT,PN)
                #     print('1 |long possition END'+ str(nowhour())+':'+str(nownow())+'...now: '+ str(datetime.now()))
                #     # 숏 잡기 
                if 1 < nownow()%5 and RD[0] < 0 and HIGH[1] < (OPEN[0]+CLOSE[0])/2 and getcurrent() < OPEN[1] + (RD[0]/2) and LongPossition == False and ShortPossition == False and chance15 == True:
                    Shortamount = amountgetter()
                    buybit(Shortamount)
                    #Fsellprice = OPEN[1] + (RD[0]/2)
                    sellprice = getcurrent()
                    ShortPossition = True
                    time.sleep(1)
                    TEXT = 'LONG POSSITION \n'+ str(Shortamount) +'X'+ str(leverage)+'...'+'bought at'+ str(sellprice)
                    PN = 'LONG POSSITION  '
                    mail(TEXT,PN)
                    print('short possition'+ str(nowhour())+':'+str(nownow())+'...now: '+ str(datetime.now()))
                    chance15 = False
                    #숏 정리 
                #elif 0 < nownow()%5  and  ShortPossition == True and LongPossition == False:
                #    sellbit(Shortamount)
                #    ShortEndPrice = getcurrent()
                #    ShortPossition = False
                #    profit = round(BGDF()/StartMoney*100,2)
                #    time.sleep(1)
                #    TEXT = 'LONG POSSITION END... at:'+ str(ShortEndPrice) +'\n profit:'+str(profit) + '%' + '\n deposit = ' + str(BGDF())
                #    PN = 'LONG POSSITION END '
                #    mail(TEXT,PN)
                #    print('1N|short possition END'+ str(nowhour())+':'+str(nownow())+'...now: '+ str(datetime.now()))
            elif BGDF()/StartMoney > 1.5 or BGDF() > StartMoney + 8000:
                if RED == False:
                    print('done')
                    profit = round(BGDF()/StartMoney*100,2)
                    TEXT = 'todays trading over' +'\n profit=' + str(profit)
                    PN = 'TRADING OVER ... TIME:' + str(datetime.now())
                    mail(TEXT,PN)
                    RED = True


    except Exception as e:
        print(e)
        time.sleep(1)