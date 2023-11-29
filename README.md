# Курсовой проект по защите информации. 
# Разработка децентрализованной системы учебных дипломов на блокчейне для борьбы с поддельными дипломами и улучшения верификации образования

Проект выполнен командой: Мишин Александр Б01-008, Конопля Максим Б01-008, Лирисман Карина Б01-008

## Описание проекта (еще будет дополнено)

Проект основан на блокчейне, системе Ethereum.

Имеется возможность аутентификации как ВУЗ - внесение данных о выданных учебным заведением дипломов.

Войдите как пользователь/работодатель - проверяйте наличие диплома по данным, предоставленным человеком для приема на работу.

<image src="readme_wall.png">

## Как запустить

1. Усановите miniconda: https://docs.conda.io/projects/miniconda/en/latest/
2. 
```
conda create -n <имя>
conda activate <имя>
conda install flask
conda install -c conda-forge web3
conda install -c conda-forge pdfminer
conda install nltk
```
3.
``` 
git clone https://github.com/TheRedHotHabanero/projectPI.git
cd projectPI
```
4.
Настраиваем блокчейн аккаунты и запускаем контракт:
Устанавливаем ganache:
```
sudo apt-get install npm
npm install ganache --global
ganache
```
Теперь на 127.0.0.1:8545 живут 10 аккаунтов с 100 ETH! Копируем адрес и ключ одного их них и вставляем в deploy.py:
<image src="deploy.png">
Запускаем контракт:
pip install py-solc-x
puthon deploy.py
Получаем адрес, а также abi нашего контракта из CompiledCode.json и вставляем их в contractDetails или передаем в качестве аргументов при создании контракта.
Теперь можно запускать проект:
python app.py

Вылезет в консоли url: открываем его в браузере и наслаждаемся видом
