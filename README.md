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

`POST /users`

**Arguments**

-  `"username":string` unique name or unique email for user
-  `"name":string` name for user
-  `"surname":string` surname for user
-  `"password":string` password for user


```bash
  curl --location --request POST 'http://127.0.0.1:5000/users' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "username": "aykut",
    "name": "aykut",
    "surname":"arslantas",
    "password":"test1234"
  }'
```

**Response**

- 201: New User Created
- 401: user already exists or fields are missing

## Get auth token for user (login)

**Request**

`POST /login`

**Arguments**

-  `"username":string`
-  `"password":string`

```bash
curl --location --request POST 'http://127.0.0.1:5000/login' \
--header 'Content-Type: application/json' \
--data-raw '{
   "username": "admin",
   "password": "testadmin"
}'
```

**Response**

- 201: logged in successfully
- 401: invalid credentials

```json
{
  "is_admin": true,
  "jwt_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6ImRmNTVkNzBiLWMxOTgtNDY2MS1hYWYyLTU5OWExYTljYTcwYSIsImV4cGlyZXMiOiIyMDIwLTA3LTA2IDA0OjI4OjQ3LjUxNjQ0NCJ9.bqahqrCYeFo8DN_okmeo2puEkpvHa_4otUSp2D8LMiw",
  "token_expires": "2020-07-06T04:28:47.516444+00:00",
  "user_name": "admin"
}
```
### List all users

**Request**

`GET /users`

```bash
curl --location --request GET 'http://127.0.0.1:5000/users' \
--header 'x-access-token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjVmYjE0N2U3LWM0YjEtNGEzMC1iNDIzLTY2ODFjMjJiNTQ1MiIsImV4cGlyZXMiOiIyMDIwLTA3LTA2IDE5OjIxOjAyLjkxMTA2NCJ9.3-PzrgA0hCXMVuQQLeEBvmggkF--WCERjHun4zoRL2Q'
```

**Response**

- 201: returns list of users
- 401: unauthorized, invalid or expired token

```json
{
  "users": [
    {
      "id": "df55d70b-c198-4661-aaf2-599a1a9ca70a",
      "is_admin": true,
      "name": "aykut",
      "surname": "arslantas",
      "user_name": "admin"
    },
    {
      "id": "8cc065f3-be3c-42f7-9dd5-dd74c8d2ce7f",
      "is_admin": false,
      "name": "aykut",
      "surname": "arslantas",
      "user_name": "admin2"
    },
    {
      "id": "d813de39-6aa3-4f23-9b2a-c424fe75972e",
      "is_admin": false,
      "name": "test",
      "surname": "test",
      "user_name": "234562156"
    }
  ]
}
```
### Get user data with token

**Request**  
`GET /users/<user_id>`

```bash
curl --location --request GET 'http://127.0.0.1:5000/users/<user_id>' \
--header 'x-access-token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjVmYjE0N2U3LWM0YjEtNGEzMC1iNDIzLTY2ODFjMjJiNTQ1MiIsImV4cGlyZXMiOiIyMDIwLTA3LTA2IDE5OjIxOjAyLjkxMTA2NCJ9.3-PzrgA0hCXMVuQQLeEBvmggkF--WCERjHun4zoRL2Q'
```
**Response**

- 201: returns user list

- 401: token expired or invalid
```json
{
  "user": {
    "id": "8cc065f3-be3c-42f7-9dd5-dd74c8d2ce7f",
    "name": "aykut",
    "surname": "arslantas",
    "user_name": "admin"
  }
}
```
### Delete User

**Request**  
`DELETE /users/<user_id>`
```bash
curl --location --request DELETE 'http://127.0.0.1:5000/users/<user_id>' \
--header 'x-access-token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjVmYjE0N2U3LWM0YjEtNGEzMC1iNDIzLTY2ODFjMjJiNTQ1MiIsImV4cGlyZXMiOiIyMDIwLTA3LTA2IDE5OjIxOjAyLjkxMTA2NCJ9.3-PzrgA0hCXMVuQQLeEBvmggkF--WCERjHun4zoRL2Q'
```

**Response**

- 204: returns success
- 401: token expired or invalid

### Authorize User
**Request**

`PUT /users`

```bash
curl --location --request PUT 'http://127.0.0.1:5000/users/<user_id>' \
--header 'x-access-token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjVmYjE0N2U3LWM0YjEtNGEzMC1iNDIzLTY2ODFjMjJiNTQ1MiIsImV4cGlyZXMiOiIyMDIwLTA3LTA2IDE5OjIxOjAyLjkxMTA2NCJ9.3-PzrgA0hCXMVuQQLeEBvmggkF--WCERjHun4zoRL2Q'
```

**Response**

- 200: returns success
- 401: token expired or invalid

```json
{
  "message": "The user has been authorized to admin"
}
```
### List all feeds

**Request**

`GET /feeds`

**Arguments**

-  `"start":integer`
-  `"length":integer`
-  `"search":string`
-  `"date":string`

````bash
curl --location --request GET 'http://127.0.0.1:5000/feeds?start=10&length=5&search=null&date=1_day' \
--header 'x-access-token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjVmYjE0N2U3LWM0YjEtNGEzMC1iNDIzLTY2ODFjMjJiNTQ1MiIsImV4cGlyZXMiOiIyMDIwLTA3LTA2IDE5OjIxOjAyLjkxMTA2NCJ9.3-PzrgA0hCXMVuQQLeEBvmggkF--WCERjHun4zoRL2Q'
````

**Response**

- 201: success
- 401: Token expired, invalid or missing field

```json
[
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
]
```
### Create new source

**Request**

`POST /rss_sources`

**Arguments**

-  `"name":string`
-  `"url":string`

```bash
curl --location --request POST 'http://127.0.0.1:5000/rss_sources' \
--header 'x-access-token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjVmYjE0N2U3LWM0YjEtNGEzMC1iNDIzLTY2ODFjMjJiNTQ1MiIsImV4cGlyZXMiOiIyMDIwLTA3LTA2IDE5OjIxOjAyLjkxMTA2NCJ9.3-PzrgA0hCXMVuQQLeEBvmggkF--WCERjHun4zoRL2Q' \
--header 'Content-Type: application/json' \
--data-raw '{
   "name": "mynet",
   "url":"http://www.mynet.com/haber/rss/sondakika"
}'
```
**Response**

- 201: created successfully
- 401: token, invalid or missing field
- 401: unauthorized

```json
{
  "Message": "New source created",
  "id": "5f0284d52ef02742ef4747e2"
}
```

### Delete a source

**Request**

`DELETE /rss_sources/<source_id>`


```bash
curl --location --request DELETE 'http://127.0.0.1:5000/rss_sources/<source_id>' \
--header 'x-access-token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjVmYjE0N2U3LWM0YjEtNGEzMC1iNDIzLTY2ODFjMjJiNTQ1MiIsImV4cGlyZXMiOiIyMDIwLTA3LTA2IDE5OjIxOjAyLjkxMTA2NCJ9.3-PzrgA0hCXMVuQQLeEBvmggkF--WCERjHun4zoRL2Q'
```
**Response**

- 204: returns success
- 401: unauthorized
- 404: no source found by given id

### Give Rank
**Request**

`PUT /feeds/<feed_id>`

**Arguments**

-  "feed_id" : string
-  "rank" : float

```bash
curl --location --request PUT 'http://127.0.0.1:5000/feeds/<feed_id>' \
--header 'x-access-token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjVmYjE0N2U3LWM0YjEtNGEzMC1iNDIzLTY2ODFjMjJiNTQ1MiIsImV4cGlyZXMiOiIyMDIwLTA3LTA2IDE5OjIxOjAyLjkxMTA2NCJ9.3-PzrgA0hCXMVuQQLeEBvmggkF--WCERjHun4zoRL2Q' \
--header 'Content-Type: application/json' \
--data-raw '{
   "rank": 1.0
}'
```

**Response**

- 200: feed ranked
- 401: unauthorized
- 404: no feed found by given id

### Logout

**Request**

`DELETE /login`

```bash
curl --location --request DELETE 'http://127.0.0.1:5000/login' \
--header 'x-access-token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjVmYjE0N2U3LWM0YjEtNGEzMC1iNDIzLTY2ODFjMjJiNTQ1MiIsImV4cGlyZXMiOiIyMDIwLTA3LTA2IDE5OjIxOjAyLjkxMTA2NCJ9.3-PzrgA0hCXMVuQQLeEBvmggkF--WCERjHun4zoRL2Q''
```

**Response**
- 204: returns success
- 401: unauthorized
- 404: no feed found by given id