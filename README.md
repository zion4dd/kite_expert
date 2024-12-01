Сайт для экспертов кайт-сообщества.  
Авторы размещают на сайте полезную информацию о спортивном оборудовании.  
Автор проходит тест перед регистрацией.
После регистрации заполняет в профиле информацию о себе.
Далее он имеет возможность размещать информацию о спортинвентаре в соответствующих категориях.  


Проект реализован на фреймворке Django.  
API реализован с помощью DRF.  
Аутентификации по токенам - Djoser.  
Кэширование - Redis.  
Фоновые задачи сжатия изображений - Celery (broker=Redis).  

Deploy:  
https://kite-expert.ru/

API:  
https://kite-expert.ru/docs/swagger/


```
# .env
DEBUG="false"
USER_IS_ACTIVE="true"
DJANGO_LOG_LEVEL="WARNING"
SECRET_KEY="django-insecure-j@j+l*************************************"
MAX_IMAGE_SIZE="1200"
EMAIL_HOST_PASSWORD="password"
DOMAIN="localhost:5000"
URL="http://localhost:5000"
```
