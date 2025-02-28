from setuptools import setup

setup(
    name="Worzis_tools", # имя модуля, которое будет использоваться при установке в будущем
    version="1.218", # версия модуля при каждом обновлении (новой отправке надо версию увеличивать)
    description="", # описание (можно не использовать)
    packages=["Worzis_tools"], # список с названием папок которые нужно залить
    author_email="dag201011@gmail.com", # почта автора модуля
    zip_safe=False, # пароль
    install_requires=[
        'colorama',
        'pytz',
        'python-dotenv',
        'python-telegram-bot==13.7'
    ], # список названий модулей которые нужны для корректной работы вашего модуля
)