# Installation
RSS Watchers requires python3.8 and mongoDb
```bash
git clone https://github.com/aykuttars/rsswatcher.git
```
# DOCKER (Development)
You can start both api and frontend development servers by typing `docker-compose up -d`.
## Backend
Jwt authentication used to create API functionality.
``` bash
cd backend
pip install -r requirements.txt
```
# Running App Locally
## Backend
``` bash
Python app.py

```
Backend serves on 5000 port.
## Frontend
Used Bootstrap 4 and Jquery libraries
# API Usage
## Register a new user
**Request**
`POST /users/`
**Arguments**
-  `"username":string` unique name or unique email for user
-  `"name":string` name for user
-  `"surname":string` surname for user
-  `"password":string` password for user
```bash
curl --location --request POST 'http://127.0.0.1:5000/users/'

--form 'username=newuser' 
--form 'password=newpassword'
--form 'name=newname'
--form 'surname=newsurname'
```
```
**Response**
- 200: New User Created
- 401: user already exists or fields are missing
```
## Get auth token for user (login)
**Request**
`POST /login/`
**Arguments**
-  `"username":string`
-  `"password":string`
```bash

curl --location --request POST 'http://127.0.0.1:5000/login/'
--data-urlencode 'username=useradmin' 
--data-urlencode 'password=userpasswd'
```
**Response**
- 200: logged in successfully
- 400: invalid credentials
```json
{
"is_admin": true,

"jwt_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6ImRmNTVkNzBiLWMxOTgtNDY2MS1hYWYyLTU5OWExYTljYTcwYSIsImV4cGlyZXMiOiIyMDIwLTA3LTA2IDA0OjI4OjQ3LjUxNjQ0NCJ9.bqahqrCYeFo8DN_okmeo2puEkpvHa_4otUSp2D8LMiw",

"token_expires": "2020-07-06T04:28:47.516444+00:00",

"user_name": "admin"
}
```
### Verify user token
**Request**
`POST /login/`
**Arguments**
-  `"token":string`
```bash
curl --location --request POST 'http://127.0.0.1:5000/' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--x-access-token 'token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6InRlc3R1c2VyIiwiZXhwIjoxNTg2MzUyOTczLCJlbWFpbCI6InRlc3RAcGl6emEuY29tIiwib3JpZ19pYXQiOjE1ODYzNTE5NzN9.IpwRhxHdkUUqmPYyiZSoVt0K0gKIULvilj9eKonofQg'
```
**Response**
- 200: verified the token
- 400: token expired or invalid
### Get user data with token
**Request**
`GET /users`
```bash
curl --location --request GET 'http://127.0.0.1:5000/users/<user_id>' \
--header 'x-access-token:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6InRlc3R1c2VyIiwiZXhwIjoxNTg2MzUyOTczLCJlbWFpbCI6InRlc3RAcGl6emEuY29tIiwib3JpZ19pYXQiOjE1ODYzNTE5NzN9.IpwRhxHdkUUqmPYyiZSoVt0K0gKIULvilj9eKonofQg'
```
**Response*
- 200: returns user list
- 400: token expired or invalid
```json
{

"user": {

"id": "8cc065f3-be3c-42f7-9dd5-dd74c8d2ce7f",

"name": "aykut",

"password": "sha256$uwYBzcWP$fe0dc15d9b9cc057290aa9c89c800bd11f1797a07f4f1219d67a1bae011d669d",

"surname": "arslantas",

"user_name": "admin2"

}
```
### Delete User
**Request**
`DELETE /users`
```bash
curl --location --request DELETE 'http://127.0.0.1:5000/users/<user_id>' \
--header 'x-access-token:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6InRlc3R1c2VyIiwiZXhwIjoxNTg2MzUyOTczLCJlbWFpbCI6InRlc3RAcGl6emEuY29tIiwib3JpZ19pYXQiOjE1ODYzNTE5NzN9.IpwRhxHdkUUqmPYyiZSoVt0K0gKIULvilj9eKonofQg'
```
**Response*
- 200: returns success
- 400: token expired or invalid
```json
{
'message':'The user has been deleted'
}
```
### Authorize User
**Request**
`PUT /users`
```bash
curl --location --request DELETE 'http://127.0.0.1:5000/users/<user_id>' \
--header 'x-access-token:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6InRlc3R1c2VyIiwiZXhwIjoxNTg2MzUyOTczLCJlbWFpbCI6InRlc3RAcGl6emEuY29tIiwib3JpZ19pYXQiOjE1ODYzNTE5NzN9.IpwRhxHdkUUqmPYyiZSoVt0K0gKIULvilj9eKonofQg'
```
**Response*
- 200: returns success
- 400: token expired or invalid
```json
{
'message':'The user has been authorized to admin'
}
```
### List all users
**Request**

`GET /users`
```bash
curl --location --request GET 'http://127.0.0.1:5000/users/' \
--header 'x-access-token:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6InRlc3R1c2VyIiwiZXhwIjoxNTg2MzUyOTczLCJlbWFpbCI6InRlc3RAcGl6emEuY29tIiwib3JpZ19pYXQiOjE1ODYzNTE5NzN9.IpwRhxHdkUUqmPYyiZSoVt0K0gKIULvilj9eKonofQg'
**Response**
- 200: returns list of users
- 401: unauthorized, invalid or expired token
```json
{

"users": [

{

"id": "df55d70b-c198-4661-aaf2-599a1a9ca70a",

"is_admin": true,

"name": "aykut",

"password": "sha256$xWeAG8WK$97d28b85f0c5e60347226ddcf541ef057d2078f043285a419f3aec124f5438dc",

"surname": "arslantas",

"user_name": "admin"

},

{

"id": "8cc065f3-be3c-42f7-9dd5-dd74c8d2ce7f",

"is_admin": false,

"name": "aykut",

"password": "sha256$uwYBzcWP$fe0dc15d9b9cc057290aa9c89c800bd11f1797a07f4f1219d67a1bae011d669d",

"surname": "arslantas",

"user_name": "admin2"

},

{

"id": "d813de39-6aa3-4f23-9b2a-c424fe75972e",

"is_admin": false,

"name": "test",

"password": "sha256$SAdRpS09$7313b7159f73d42c1125d710c3f7d12ba97baee1f71127f61f6b30c37f26e463",

"surname": "test",

"user_name": "234562156"

}

]

}
```
### List all feeds
**Request**
`GET /feeds/`
**Arguments**
-  `"start":integer`
-  `"length":inteher`
-  `"length":inteher`
-  `"searchl":string`
-  `"date":string`
````bash
curl --location --request GET 'http://127.0.0.1:5000/feeds/' \
--header 'x-access-token:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6InRlc3R1c2VyIiwiZXhwIjoxNTg2MzUyOTczLCJlbWFpbCI6InRlc3RAcGl6emEuY29tIiwib3JpZ19pYXQiOjE1ODYzNTE5NzN9.IpwRhxHdkUUqmPYyiZSoVt0K0gKIULvilj9eKonofQg'
````
**Response**
- 200: success
- 400: Token expired, invalid or missing field

```json
{
"date": "2020-07-05T05:37:30+00:00",
"detail": "Gaziantep'te düzenlenen operasyonda 15 kilo 400 gram eroin ve 6 kilo 460 gram metamfetamin ele geçirildi, bir şüpheli gözaltına alındı.\n",
"header": "Gaziantep'te 15 kilo 400 gram eroin ele geçirildi",
"id": "5f0284d52ef02742ef4747e3",
"image": "https://iasbh.tmgrup.com.tr/21eb82/650/344/0/36/652/379?u=https://isbh.tmgrup.com.tr/sbh/2020/07/05/gaziantepte-15-kilo-400-gram-eroin-ele-gecirildi-1593927581143.jpg",
"provider": "Sabah",
"rank": 0.0,
"url": "https://www.sabah.com.tr/gundem/2020/07/05/gaziantepte-15-kilo-400-gram-eroin-ele-gecirildi"
},
{
"date": "2020-07-05T05:54:52+00:00",
"detail": "Uyuşturucu baronu Nejat Daş tutuklandı! Türkiye, geçtiğimiz hafta yapılan Bataklık Operasyonu ile ilgili son dakika haberlerini konuşuyor. Uyuşturucu çetesine yönelik yapılan operasyonda, Nejat Daş ile...\n",
"header": "Son Dakika Haberi: Nejat Daş kimdir? Bataklık Operasyonu ile çökertilen çetede Nejat Daş tutuklandı",
"id": "5f0284d52ef02742ef4747e2",
"image": "https://iasbh.tmgrup.com.tr/ac2984/650/344/0/112/800/532?u=https://isbh.tmgrup.com.tr/sbh/2020/07/05/1593927836561.jpg",
"provider": "Sabah",
"rank": 0.0,
"url": "https://www.sabah.com.tr/gundem/2020/07/05/son-dakika-haberi-nejat-das-kimdir-bataklik-operasyonu-ile-cokertilen-cetede-nejat-das-tutuklandi"
},
{
"date": "2020-07-05T06:02:16+00:00",
"detail": "Suudi Arabistan'ın İstanbul’daki Başkonsolosluğunda öldürülen Suudi gazeteci Cemal Kaşıkçı’nın geçtiğimiz gün görülen davasında tanık olarak ifade veren konsolosluk çalışanı Zeki Demir, şoke eden açıklamalarda...\n",
"header": "Kaşıkçı davasında şoke eden ifadeler! 'Tandırı yaktırıp, Yallah dediler'",
"id": "5f0284d52ef02742ef4747e1",
"image": "https://iasbh.tmgrup.com.tr/e31773/320/320/83/0/349/266?u=https://isbh.tmgrup.com.tr/sbh/2020/07/05/kasikci-davasinda-soke-eden-ifadeler-tandiri-yaktirip-yallah-dediler-1593929552147.jpg",
"provider": "Sabah",
"rank": 0.0,
"url": "https://www.sabah.com.tr/gundem/2020/07/05/kasikci-davasinda-soke-eden-ifadeler-tandiri-yaktirip-yallah-dediler"
},
{
"date": "2020-07-05T06:02:18+00:00",
"detail": "İki sezondur şampiyonluğu göğüsledikten sonra bu sezon zirveden kopan Galatasaray'da değişim başlıyor! Hem maliyet, hem kadronun doymuşluğu hem de yabancı kuralı nedeniyle yerlilere yönelen sarı-kırmızılılarda altyapıdan birçok yetenek de A Takıma göz kırpıyor! İşte 2020-21 model Galatasaray!\n",
"header": "2020-21 model Galatasaray!",
"id": "5f0284d42ef02742ef474792",
"image": "https://im.haberturk.com/2020/07/04/ver1593928938/2733803_manset.jpg",
"provider": "haberturk",
"rank": 0.0,
"url": "https://www.haberturk.com/galatasaray-da-degisim-basliyor-2733803-spor"
},
{
"date": "2020-07-05T06:24:55+00:00",
"detail": "Dünya genelinde milyonlarca insanın enfekte olduğu yüz binlerce insanın ise hayatını kaybettiği Koronavirüs etkisini devam ettiriyor. Öte yandan İstanbul'da skandal olarak nitelenecek görüntüler meydana...\n",
"header": "Skandal görüntüler! Koronavirüs'e aldırmadan Haliç'te yat partisi düzenlediler",
"id": "5f0284d52ef02742ef4747e0",
"image": "https://iasbh.tmgrup.com.tr/873ca9/320/320/145/0/596/451?u=https://isbh.tmgrup.com.tr/sbh/2020/07/05/soke-eden-goruntuler-koronaviruse-aldirmadan-halicte-yat-partisi-duzenlediler-1593930452372.jpg",
"provider": "Sabah",
"rank": 0.0,
"url": "https://www.sabah.com.tr/gundem/2020/07/05/soke-eden-goruntuler-koronaviruse-aldirmadan-halicte-yat-partisi-duzenlediler"
}
],
"recordsFiltered": 6,
"recordsTotal": 140
}
```


### Create new Feed

**Request**

`POST /rss_sources`

**Arguments**


-  `"name":string` feed name

-  `"url":string` feed url

```bash
curl --location --request GET 'http://127.0.0.1:5000/feeds/' \
--header 'x-access-token:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6InRlc3R1c2VyIiwiZXhwIjoxNTg2MzUyOTczLCJlbWFpbCI6InRlc3RAcGl6emEuY29tIiwib3JpZ19pYXQiOjE1ODYzNTE5NzN9.IpwRhxHdkUUqmPYyiZSoVt0K0gKIULvilj9eKonofQg'
```
**Response**
- 201: created successfully
- 400: token, invalid or missing field
- 401: unauthorized
```json
{'Message':'New source created','id':5f0284d52ef02742ef4747e2}
```
### Delete a Feed

**Request**
`DELETE /rss_sources/<source_id>`
**Arguments**
-  `"source_id":string` source id
```bash
curl --location --request POST 'http://127.0.0.1:5000/task_list/1/rss_sources/' \
--header 'x-access-token:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6InRlc3R1c2VyIiwiZXhwIjoxNTg2MzUyOTczLCJlbWFpbCI6InRlc3RAcGl6emEuY29tIiwib3JpZ19pYXQiOjE1ODYzNTE5NzN9.IpwRhxHdkUUqmPYyiZSoVt0K0gKIULvilj9eKonofQg'
```
**Response**
- 204: source deleted
- 401: unauthorized
- 404: no source found by given id
- 
### Give Rank

**Request**
`PUT/feeds/<feed_id>`
**Arguments**
-  `"feed_id":string` feed id
- `"rank":query float` feed rank
```bash
curl --location --request POST 'http://127.0.0.1:5000/task_list/1/rss_sources/' \
--header 'x-access-token:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6InRlc3R1c2VyIiwiZXhwIjoxNTg2MzUyOTczLCJlbWFpbCI6InRlc3RAcGl6emEuY29tIiwib3JpZ19pYXQiOjE1ODYzNTE5NzN9.IpwRhxHdkUUqmPYyiZSoVt0K0gKIULvilj9eKonofQg'
```
**Response**
- 204: feed ranked
- 401: unauthorized
- 404: no feed found by given id