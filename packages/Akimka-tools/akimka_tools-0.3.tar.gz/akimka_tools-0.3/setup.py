from setuptools import setup

setup(
    name= "Akimka_tools", #имя модуля которое будет использоваться при установке в будуйщем
    version="0.3", # версия модуля.при каждом обновлении(новой отправке) надо увеличивать версию 
    description="Мои инструменты", # описание. Можно не использовать 
    packages=["Akimka_001"], #Список с названием папки которые нужно залить
    author_email="akimov.konstantin.2024@gmail.com", # Почта модуля 
    zip_safe= False , # Пароль
    install_reguires=[
        "pytz"
        "python-dotenv"
        "python-telegram-bot==13.7"

    ] , #список название модулей которые нужны для корректной работы этого модуля 
    

)