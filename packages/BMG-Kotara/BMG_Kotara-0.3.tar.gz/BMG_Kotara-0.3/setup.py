from setuptools import setup


setup(
    name="BMG_Kotara",  # имя модуля которое будет использоваться при устоновке модуля в будущем
    version="0.3", # версия модуля, при каждом обновление(отправке) версию нужно увеличевать
    description="мои инструменты", # описание можно не использовать
    packages=["BMG_NFS"], #название папок которые надо залить
    author_email="miniindra7@gmail.com",
    zip_safe=False, # пароль
    install_requires=[
        "pytz",
        "python-dotenv",
        "python-telegram-bot==13.7"
    ] # для коректной работы модуля
)