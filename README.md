<p align = center> <a href="https://git.io/typing-svg" align = center><img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&pause=1000&random=false&width=435&lines=%D0%A7%D0%B0%D1%82-%D0%B1%D0%BE%D1%82+%D0%B4%D0%BB%D1%8F+%D0%BE%D1%81%D0%BC%D0%BE%D1%82%D1%80%D0%B0+%D1%81%D1%82%D1%80%D0%B0%D1%85%D0%BE%D0%B2%D1%8B%D1%85+%D0%BE%D0%B1%D1%8A%D0%B5%D0%BA%D1%82%D0%BE%D0%B2" alt="Typing SVG" /></a> </p>
<div align="justify">Чат-бот, разработанный в рамках кейс-чемпионата от Совкомбанка, предназначен для упрощения процесса осмотра страхуемого имущества клиентами. Благодаря использованию технологий компьютерного зрения, чат-бот позволяет клиенту без специальных экспертных навыков осуществить осмотр имущества и получить обратную связь от сотрудника страховой компании. Логика работы включает в себя процессы регистрации, авторизации и администрироавния.
Решение включает в себя функции распознавания наличия автомобиля, лобового стекла и читаемого VIN номера на предоставленных фотографиях. В разработке продукта принимали участие: <a href = "https://github.com/mishantique"> Собственно я</a>, <a href = "https://github.com/MrShaller"> Никита Недобежкин</a>, <a href = "https://github.com/ponyotyan"> Анастасия Ефимова</a>.</div>

<!-- ROADMAP -->

## Функционал сервиса 

- [x] Ролевая модель
    - [x] Возможность регистрации и аутентификации в чате для доступа к функционалу
    - [x] Роль клиента 
        - [x] Возможность подачи новой заявки на осмотр
        - [x] Просмотр статуса текущей заявки на осмотр
        - [x] Просмотр истории заявок
    - [x] Роль администратора бота
        - [x] Возможность просмотра заявок клиентов
        - [x] Возможность принятия/отклонения/корректировки заявок клиентов

- [x] Загрузка данных по объекту страхования
    - [x] Возможность выбора объекта страхования (транспортное средство/загородный дом)
    - [x] Возможность отправки текстового описания объекта
    - [x] Загрузка фотографий объекта
    - [x] Соответствие фотографии необходимому разрешению
    - [x] Определение геолокации объекта, даты и время съемки по фото
    - [x] Дополнительно: автоматическая валидация фотографий
        - [ ] Проверка качества фотографии
            - [x] Фотография сделана без размытия/шумов
            - [ ] Фотография сделана с достаточным количеством света
            - [x] Фотография не была отредактирована пользователем
        - [x] Анализ соответствия фотографии требованиям

- [x] Возможности страховщика
    - [x] Возможность принятия/отклонения заявки
    - [x] Возможность отправки на корректировку заявки (исправление одной или нескольких фотографий, сделанных клиентом)
    - [x] Выдача акта осмотра клиенту
    - [x] Возможность связаться с клиентом


## Технологии

* ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
* ![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
* ![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white)
* ![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white)
* ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)


<p align="right">(<a href="#readme-top">back to top</a>)</p>
    


## 📂 Структура проекта

```sh
└── project
    ├── data
    │   ├── databases.py
    │   ├── logo.jpg
    │   ├── own_token.py
    │   └── states.py
    ├── handlers
    │   ├── admin.py 
    │   ├── heicjpg.py
    │   ├── order.py
    │   ├── order_auto.py
    │   ├── order_house.py
    │   ├── orders_insurer.py
    │   ├── status.py
    │   ├── status_auto.py
    │   ├── status_house.py
    │   ├── registration.py
    │   ├── authorization.py
    │   ├── authorization_insurer.py
    │   ├── history.py
    │   ├── bot_messages.py
    │   ├── user_commands.py
    ├── img
    ├── keyboards
    │   ├── fabrics.py
    │   ├── inline.py
    │   ├── reply.py
    ├── model
    │   ├── IMAGIN
    │   │   ├── CAR.jpg
    │   │   ├── CAR2.jpg
    │   │   ├── CAR_error.jpg
    │   │   ├── LOB.jpg
    │   │   ├── LOB_error.jpg
    │   │   ├── Real_error.jpg
    │   │   ├── VIN.jpg
    │   │   ├── VIN_error.jpg
    │   ├── modules
    │   │   ├── Car_check.py
    │   │   ├── realcheck.py
    │   │   ├── Shapecheck.py
    │   │   ├── VIN.py
    │   │   ├── WindShield.py
    │   ├── veh_detec
    │   │   ├── Auto-libs.txt
    │   │   ├── Auto-libs.bat
    │   │   ├── Readme.txt
    │   │   ├── requirements.txt
    │   │   ├── zapysk.py
    ├── pictures
    │   ├── contains photo-samples to send to user
    ├── QR
    │   ├── qr.png
    ├── venv
    │   ├── .env
    │   ├── admin.env
    │   ├── bot.py
    │   ├── config_reader.py
    │   ├── README.md
    │   ├── requirements.txt
```
## 📦 Для быстрого старта

|    |   Feature         | Description |
|----|-------------------|---------------------------------------------------------------|
| 📔 | **data**  | Директория для работы с базой данных и формированием папок с заявками от пользователей, а также актов осмотра, направленных сотрудником компании |
| 📔 | **data/States.py**  | Набор классов, используемых в машине состояний. Классы позволяют организовать поведение чат-бота в зависимости от текущего "состояния" диалога. |
| 📄 | **handlers/order_.py**  | Набор асинхронных обработчиков, направленных на формирование новой заявки в зависимости от выбранного объекта страхования |
| 📄 | **handlers/orders_insurer.py** | Обработка команд от пользователя, авторизовавшегося как сотрудник страховой компании |
| 📄 | **handlers/status.py**  | Обращение к базе данных с целью формирования отклика на запрос о состоянии поданных заявок |
| 🖼️ | **Model/IMAGIN**    | Образцовые фотографии для легит-чека работы модели |
| 🖼️ | **pictures**       | Директория, содержащая набор файлов, отправляемых пользователю |




## 🚀 Установка и запуск
Для запуска бота необходимо выполнить следующие шаги:

***Requirements***

Убедитесь, что у Вас установлены необходимые зависимости:

* **Python**: `version x.y.z`

### ⚙️ Installation
1. Клонируйте репозиторий:

```sh
gh repo clone mishantique/Chat-bot-with-AI
```

2. Установите необходимые зависимости:

```sh
pip install -r requirements.txt
```


### 🤖 Инициализация бота
<ol>
<li> Зарегистрировать своего бота через <a href = 'https://t.me/BotFather'>@BotFather </a> в Telegram и получить уникальный токен. </li>
<li> Вставить полученный токен в файл конфигурации <b>.env. </b> </li>

``` Python
#Put your token here
BOT_TOKEN = ''
```
<li> Инициализируйте бота запуском <b> bot.py </b> </li>

``` Python
if name == 'main':
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)
    asyncio.run(main())
```
При первом запуске будет автоматически инициализирована база данных sqlite3.
</ol>

## 🧪 Машинное обучение

Для распознавания объектов и текста на изображениях используются cv2, easyocr.

Проверка качества фотографии и извлечение метаданных реализовано в *Shapechek.py*. Желаемое разрешение для проверки задаётся в функции ниже:

``` Python
    def checking(self): #Разрешение фото
        with Image.open(self.file_path) as im:
            if im.size[0] >= 1600 and im.size[1] >= 720:
                #print("Фото хорошего разрешения")

                # Чек метаданных:
                metadata = self.extract_metadata()
                if metadata == False:
                    return "Нет метаданных"
                return True

            else:
                return "Плохое разрешение"
```
Проверка наличия VIN-номера на фотографии производится согласно шаблону, определенному функцией *extract_vin*

``` Python
class VIN:
    @staticmethod
    def extract_vin(text_list):
        vin_numbers = []

        for text in text_list:
            # Преобразование в список
            filtered_text_list = text.split()

            # Проход по каждому элементу списка, очистка слов и извлечение VIN-номера
            for word in filtered_text_list:
                # Удаление всех символов, кроме букв и цифр (включая "O")
                cleaned_word = re.sub(r'[^A-HJ-NPR-Z0-9IO]', '', word)

                # Проверка, содержит ли текст и буквы и цифры, и длина от 16 до 18 символов
                if any(c.isalpha() for c in cleaned_word) and any(c.isdigit() for c in cleaned_word) and 16 <= len(
                        cleaned_word) <= 18:
                    vin_numbers.append(cleaned_word)

        return vin_numbers

```

### Проверка разрешения, извлечение метаданных, проверка VIN номера

![Alt text](/VIN.png?raw=true "Optional Title")

``` Python
Фото хорошего разрешения
Metadata: {'imageTakenTime': '2023:10:15 07:25:14', 'geolocation_lat: 59.8720555', 'geolocation_lng': 30.367008}
['OPEL 0482001711670094 WOLOAHL6785065544 71870 K9 3145 170955 K9 220955 20R XXL0 8']
```

<!-- USAGE EXAMPLES -->
## Примеры использования
После регистрации и авторизации пользователи могут отправлять фотографии для осмотра через чат-бота. Бот автоматически определит наличие автомобиля, лобового стекла и VIN номера. 
После окончания формирования заявка автоматически отправляется сотруднику-страховщику на рассмотрение.
### Интерфейс
![Alt text](/serivce.png?raw=true "Optional Title")
С видеодемонстрацией функционала можно ознакомиться по <a href = "https://drive.google.com/drive/folders/1kl-88dxnAc4BYvnG4dUmA7bv-tbHWJF9?usp=sharing"> ссылке </href>

## Как внести вклад
<ul>
<li>Усовершенствование системы безопасности</li>
<li>Расширение функционала чат-бота</li>
<li>Переход на более совершенную СУБД</li>
</ul>
Мы открыты к предложениям по расширению функционала, особенно в области Machine Learning для адаптации бота к осмотру загородных домов. Для внесения предложений, пожалуйста, свяжитесь с нами.

## Контакты
Если у вас есть вопросы или предложения, свяжитесь с нами:


Telegram: 
- [@mishantique](https://t.me/mishantique) 
- [@ponyotyan](https://t.me/ponyotyan)
- [@ShallerMau](https://t.me/ShallerMau)

Email: michvitko@mail.ru
