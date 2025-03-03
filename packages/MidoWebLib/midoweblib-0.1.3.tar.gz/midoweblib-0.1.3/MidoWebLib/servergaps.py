import base64, hashlib, requests, xml.etree.ElementTree as ET, json, random,string
from hashlib import sha256

def orango_500_mega(number, passowrd):
  url = 'https://services.orange.eg/SignIn.svc/SignInUser'
  header ={"net-msg-id": "61f91ede006159d16840827295301013", "x-microservice-name": "APMS", "Content-Type": "application/json; charset=UTF-8", "Content-Length": "166", "Host": "services.orange.eg", "Connection": "Keep-Alive", "Accept-Encoding": "gzip", "User-Agent": "okhttp/3.14.9",}
  data = '{"appVersion":"7.2.0","channel":{"ChannelName":"MobinilAndMe","Password":"ig3yh*mk5l42@oj7QAR8yF"},"dialNumber":"%s","isAndroid":true,"password":"%s"}' % (number, passowrd)
  r=requests.post(url,headers=header,data=data).json()
  userid=r["SignInUserResult"]["UserData"]["UserID"]
  urlo = "https://services.orange.eg/GetToken.svc/GenerateToken"
  hdo = {"Content-type":"application/json", "Content-Length":"78", "Host":"services.orange.eg", "Connection":"Keep-Alive", "User-Agent":"okhttp/3.12.1"}
  datao = '{"appVersion":"2.9.8","channel":{"ChannelName":"MobinilAndMe","Password":"ig3yh*mk5l42@oj7QAR8yF"},"dialNumber":"%s","isAndroid":true,"password":"%s"}' %(number, passowrd)
  ctv = requests.post(urlo,headers=hdo,data = datao).json()["GenerateTokenResult"]["Token"]
  key = ',{.c][o^uecnlkijh*.iomv:QzCFRcd;drof/zx}w;ls.e85T^#ASwa?=(lk'
  htv=(str(hashlib.sha256((ctv+key).encode('utf-8')).hexdigest()).upper())
  url2="https://services.orange.eg/APIs/Promotions/api/CAF/Redeem"
  data2='{"Language":"ar","OSVersion":"Android7.0","PromoCode":"رمضان كريم","dial":"%s","password":"%s","Channelname":"MobinilAndMe","ChannelPassword":"ig3yh*mk5l42@oj7QAR8yF"}' %(number, passowrd)
  header2={ "_ctv": ctv, "_htv": htv, "UserId": userid, "Content-Type": "application/json; charset=UTF-8", "Content-Length": "142", "Host": "services.orange.eg", "Connection": "Keep-Alive", "User-Agent": "okhttp/3.14.9",}
  da=data2.encode('utf-8')
  try:
    response = requests.post(url2, headers=header2, data=da).json()
  except:
    return False, "حدث خطأ يرجي المحاولة في وقت لاحق"
  if 'ErrorDescription' in response:
    if response['ErrorDescription'] == 'Success':
        return True, "تم إضافة 524 ميجا بنجاح"
    elif response['ErrorDescription'] == 'User is redeemed before':
        return False, "قمت بتفعيل العرض سابقا\n حاول مرة اخري في وقت لاحق"
    else:
        return False, "حدث خطأ، حاول مرة أخرى"
  else:
    return False, "حدث خطأ غير متوقع، حاول مرة أخرى"
    
def orange_wheel(number, password):
  url2 = "https://services.orange.eg/GetToken.svc/GenerateToken"
  hd2 = {"Content-type":"application/json", "Content-Length":"78", "Host":"services.orange.eg", "Connection":"Keep-Alive", "User-Agent":"okhttp/3.12.1"}
  data2 = '{"appVersion":"2.9.8","channel":{"ChannelName":"MobinilAndMe","Password":"ig3yh*mk5l42@oj7QAR8yF"},"dialNumber":"%s","isAndroid":true,"password":"%s"}' %(number, password)
  ctv = requests.post(url2,headers=hd2,data = data2).json()["GenerateTokenResult"]["Token"]
  a=ctv+',{.c][o^uecnlkijh*.iomv:QzCFRcd;drof/zx}w;ls.e85T^#ASwa?=(lk'
  htv=(sha256(a.encode('utf-8')).hexdigest().upper())
  ur1 = 'https://services.orange.eg/SignIn.svc/SignInUser' 
  headers ={'IsAndroid': 'true', '_ctv': ctv, '_htv': htv, 'OsVersion': '9', 'AppVersion': '6.4.0', 'Content-type': 'application/json', 'Accept': 'application/json', 'User-Agent': 'okhttp/3.14.9', 'Host': 'services.orange.eg'}
  data1 = '{"appVersion":"6.4.0","channel":{"ChannelName":"MobinilAndMe","Password":"ig3yh*mk5l42@oj7QAR8yF"},"dialNumber":"%s","isAndroid":true,"password":"%s"}'  % (number, password)
  req=requests.post(ur1,headers=headers,data=data1).json()
  longe = str(req["SignInUserResult"]["ErrorDescription"])
  if longe == 'invalid number or password ...' :
    return False, "يرجي التحقق من رقمك او كلمة السر"
  urlo = "https://services.orange.eg/GetToken.svc/GenerateToken"
  hdo = {"Content-type":"application/json", "Content-Length":"78", "Host":"services.orange.eg", "Connection":"Keep-Alive", "User-Agent":"okhttp/3.12.1"}
  datao = '{"appVersion":"2.9.8","channel":{"ChannelName":"MobinilAndMe","Password":"ig3yh*mk5l42@oj7QAR8yF"},"dialNumber":"%s","isAndroid":true,"password":"%s"}' %(number, password)
  ctv = requests.post(urlo,headers=hdo,data = datao).json()["GenerateTokenResult"]["Token"]
  key = ',{.c][o^uecnlkijh*.iomv:QzCFRcd;drof/zx}w;ls.e85T^#ASwa?=(lk'
  htv=(str(hashlib.sha256((ctv+key).encode('utf-8')).hexdigest()).upper())
  url3 ="https://services.orange.eg/APIs/Gaming/api/WheelOfFortune/Spin"
  data3 ='{"ChannelName":"MobinilAndMe","ChannelPassword":"ig3yh*mk5l42@oj7QAR8yF","Dial":"%s","Language":"ar","Password":"%s","ServiceClassId":"831"}' %(number, password)
  header3 ={"_ctv": ctv, "_htv": htv, "isEasyLogin": "false", "net-msg-id": "a53a6ccd021379dq17106206219231068", "x-microservice-name": "APMS", "Content-Type": "application/json; charset=UTF-8", "Content-Length": "157", "Host": "services.orange.eg", "Connection": "Keep-Alive", "Accept-Encoding": "gzip", "User-Agent": "okhttp/3.14.9",}
  reqe=requests.post(url3,headers=header3,data=data3).json()
  jj=reqe["OfferDetails"]["OfferId"]
  try:
    jjj=reqe["SecondryButtonDetails"]["CategoryId"]
  except:
    return False, "شكلك خلصت فرصك ف العجلة\n تيجي نجيب واحدة تانية؟ 😅"
  des=reqe["OfferDetails"]["OfferDescription"]
  urlo2 = "https://services.orange.eg/GetToken.svc/GenerateToken"
  hdo2 = {"Content-type":"application/json", "Content-Length":"78", "Host":"services.orange.eg", "Connection":"Keep-Alive" , "User-Agent":"okhttp/3.12.1"}
  datao2 = '{"appVersion":"2.9.8","channel":{"ChannelName":"MobinilAndMe","Password":"ig3yh*mk5l42@oj7QAR8yF"},"dialNumber":"%s","isAndroid":true,"password":"%s"}' %(number, password)
  ctv2 = requests.post(urlo2,headers=hdo2,data = datao2).json()["GenerateTokenResult"]["Token"]
  key2 = ',{.c][o^uecnlkijh*.iomv:QzCFRcd;drof/zx}w;ls.e85T^#ASwa?=(lk'
  htv2=(str(hashlib.sha256((ctv2+key2).encode('utf-8')).hexdigest()).upper())
  url4="https://services.orange.eg/APIs/Gaming/api/WheelOfFortune/Fulfill"
  data4='{"CategoryId":"%s","ChannelName":"MobinilAndMe","ChannelPassword":"ig3yh*mk5l42@oj7QAR8yF","Dial":"%s","Language":"ar","OfferId":"%s","Password":"%s","ServiceClassId":"831"}' %(jjj, number, jj, password)
  header4={"_ctv": ctv2, "_htv": htv2, "isEasyLogin": "false", "net-msg-id": "a53a6ccd021379d17106206400481072", "x-microservice-name": "APMS", "Content-Type": "application/json; charset=UTF-8", "Content-Length": "190", "Host": "services.orange.eg", "Connection": "Keep-Alive", "Accept-Encoding": "gzip", "User-Agent": "okhttp/3.14.9",}
  r4=requests.post(url4,headers=header4,data=data4).json()
  return False, f"تم تفعيل العرض: {des}"

def eand_AlAhly_hours(number, password, email):
  if "01" in number:
    number = number[+1:]
  elif "+201" in number:
    number = number[+3:]
  else:
    num = number
  code = email + ":" + password
  ccode = code.encode("ascii")
  base64_bytes = base64.b64encode(ccode)
  auth = base64_bytes.decode("ascii")
  xauth = "Basic" + " " + auth
  urllog = "https://mab.etisalat.com.eg:11003/Saytar/rest/authentication/loginWithPlan"
  headerslog = {"applicationVersion": "2", "applicationName": "MAB", "Accept": "text/xml", "Authorization": xauth, "APP-BuildNumber": "964", "APP-Version": "27.0.0", "OS-Type": "Android", "OS-Version": "12", "APP-STORE": "GOOGLE", "Is-Corporate": "false", "Content-Type": "text/xml; charset=UTF-8", "Content-Length": "1375", "Host": "mab.etisalat.com.eg:11003", "Connection": "Keep-Alive", "Accept-Encoding": "gzip", "User-Agent": "okhttp/5.0.0-alpha.11", "ADRUM_1": "isMobile:true", "ADRUM": "isAjax:true"}
  datalog = "<?xml version='1.0' encoding='UTF-8' standalone='yes' ?><loginRequest><deviceId></deviceId><firstLoginAttempt>true</firstLoginAttempt><modelType></modelType><osVersion></osVersion><platform>Android</platform><udid></udid></loginRequest>"
  log = requests.post(urllog, headers=headerslog, data=datalog)
  print(log)
  if "true" in log.text:
    st = log.headers["Set-Cookie"]
    ck = st.split(";")[0] 
    br = log.headers["auth"]
    url = "https://mab.etisalat.com.eg:11003/Saytar/rest/zero11/offersV3?req=<dialAndLanguageRequest><subscriberNumber>%s</subscriberNumber><language>1</language></dialAndLanguageRequest>"%(number)
    headers = {'applicationVersion': "2", 'Content-Type': "text/xml", 'applicationName': "MAB", 'Accept': "text/xml", 'Language': "ar", 'APP-BuildNumber': "10459", 'APP-Version': "29.9.0", 'OS-Type': "Android", 'OS-Version': "11", 'APP-STORE': "GOOGLE", 'auth': "Bearer " + br, 'Host': "mab.etisalat.com.eg:11003", 'Is-Corporate': "false", 'Connection': "Keep-Alive", 'Accept-Encoding': "gzip", 'User-Agent': "okhttp/5.0.0-alpha.11", 'Cookie': ck}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
      root = ET.fromstring(response.text)
      offer_id = None
      for category in root.findall('.//mabCategory'):
        for product in category.findall('.//mabProduct'):
          for parameter in product.findall('.//fulfilmentParameter'):
            if parameter.find('name').text == 'Offer_ID':
              offer_id = parameter.find('value').text
              break
          if offer_id:
            break
        if offer_id:
          break
    else:
      return False, "هذا العرض غير متاح حاليا ليك حاول بكره تاني"
  else:
    return False, "الرقم او كلمة السر غلط"
  if "true" in log.text:
    st = log.headers["Set-Cookie"]
    ck = st.split(";")[0] 
    br = log.headers["auth"]
    urlsub = "https://mab.etisalat.com.eg:11003/Saytar/rest/zero11/submitOrder"
    headerssub = {"applicationVersion": "2", "applicationName": "MAB", "Accept": "text/xml", "Cookie": ck, "Language": "ar", "APP-BuildNumber": "964", "APP-Version": "27.0.0", "OS-Type": "Android", "OS-Version": "12", "APP-STORE": "GOOGLE", "auth": "Bearer " + br + "", "Is-Corporate": "false", "Content-Type": "text/xml; charset=UTF-8", "Content-Length": "1375", "Host": "mab.etisalat.com.eg:11003", "Connection": "Keep-Alive", "User-Agent": "okhttp/5.0.0-alpha.11"}
    datasub = "<?xml version='1.0' encoding='UTF-8' standalone='yes' ?><submitOrderRequest><mabOperation></mabOperation><msisdn>%s</msisdn><operation>ACTIVATE</operation><parameters><parameter><name>GIFT_FULLFILMENT_PARAMETERS</name><value>Offer_ID:%s;ACTIVATE:True;isRTIM:Y</value></parameter></parameters><productName>FAN_ZONE_HOURLY_BUNDLE</productName></submitOrderRequest>" % (number, offer_id)
    subs = requests.post(urlsub, headers=headerssub, data=datasub).text
    if "true" in subs:
      return True, "تم تفعيل ساعتين اتصالات بنجاح"
    else:
      return False, "تحقق من بياناتك"
  else:
    return False, "تحقق من مدخلاتك"

