README: Переменные окружения для проекта

Этот документ предоставляет список необходимых переменных окружения для проекта. Настройте эти переменные в вашем файле .env или экспортируйте их в системные переменные окружения, чтобы приложение работало корректно.

Конфигурация базы данных PostgreSQL

Эти переменные используются для подключения к базе данных PostgreSQL:

PG_DRIVER: Драйвер базы данных для SQLAlchemy (например, postgresql+asyncpg).

PG_USERNAME: Имя пользователя для базы данных PostgreSQL.

PG_PASSWORD: Пароль для базы данных PostgreSQL.

PG_HOST: Хост, на котором запущена база данных (например, localhost).

PG_PORT: Порт, по которому доступна база данных (по умолчанию: 5432).

PG_DATABASE: Имя базы данных PostgreSQL.

Пример:

PG_DRIVER=postgresql+asyncpg
PG_USERNAME=postgres
PG_PASSWORD=ваш_пароль
PG_HOST=localhost
PG_PORT=5432
PG_DATABASE=ваша_база

Конфигурация безопасности

Эти переменные используются для аутентификации и шифрования:

SECRET_KEY: Секретный ключ для кодирования JWT-токенов.

ALGORITHM: Алгоритм, используемый для кодирования JWT (например, HS256).

Пример:

SECRET_KEY=ваш_секретный_ключ
ALGORITHM=HS256

Конфигурация электронной почты

Эти переменные необходимы для отправки писем:

MAIL: Электронная почта, с которой отправляются письма.

MAIL_PASSWORD: Пароль для указанной электронной почты.

MAIL_PORT: Порт почтового сервера (например, 465 для SSL).

MAIL_SERVER: Адрес SMTP-сервера.

Пример:

MAIL=ваш_email@example.com
MAIL_PASSWORD=ваш_пароль
MAIL_PORT=465
MAIL_SERVER=smtp.example.com

Конфигурация RabbitMQ

Эти переменные используются для настройки RabbitMQ:

RABBITMQ_HOST: Хост, на котором запущен RabbitMQ (например, localhost).

RABBITMQ_USER: Имя пользователя RabbitMQ.

RABBITMQ_PASSWORD: Пароль RabbitMQ.

RABBITMQ_VHOST: Виртуальный хост RabbitMQ (по умолчанию: /).

Пример:

RABBITMQ_HOST=localhost
RABBITMQ_USER=guest
RABBITMQ_PASSWORD=guest
RABBITMQ_VHOST=/

Конфигурация Redis

Эти переменные используются для настройки Redis:

REDIS_DOMAIN: Хост, на котором запущен Redis (например, localhost).

REDIS_PORT: Порт Redis (по умолчанию: 6379).

REDIS_PASSWORD: Пароль для Redis (оставьте пустым, если не требуется).

Пример:

REDIS_DOMAIN=localhost
REDIS_PORT=6379
REDIS_PASSWORD=

Примечания

Убедитесь, что такие чувствительные данные, как PG_PASSWORD, SECRET_KEY и MAIL_PASSWORD, находятся в безопасности.

Избегайте жёсткого кодирования этих переменных в исходном коде; используйте файл .env или переменные окружения в процессе деплоя.

Следуя этой настройке, другие разработчики получат чёткое представление о том, как настроить окружение для этого проекта.

