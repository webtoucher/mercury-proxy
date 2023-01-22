# Прокси сервер для счётчиков Инкотекс Меркурий

![License](https://img.shields.io/badge/License-BSD%203--Clause-green)
[![Downloads](https://img.shields.io/pypi/dm/mercury-proxy.svg?color=orange)](https://pypi.python.org/pypi/mercury-proxy)
[![Latest Version](https://img.shields.io/pypi/v/mercury-proxy.svg)](https://pypi.python.org/pypi/mercury-proxy)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/mercury-proxy.svg)](https://pypi.python.org/pypi/mercury-proxy)

Прокси сервер предназначен для подключения конфигуратора (либо другого программного
или аппаратного средства взаимодействия по внутренним протоколам) к счётчикам марки
Инкотекс Меркурий, подключенных к удалённому серверу на базе Linux через последовательную
шину (RS485).

## Установка

Для использования в качестве самостоятельного приложения установите при помощи pip:

```shell
$ pip install mercury-proxy
```

Либо добавьте в файл requirements.txt вашего проекта на python в качестве зависимости:

```
mercury-proxy~=1.0
```

## Использование

...

| :warning: Внимание! |
|:--------------------|
| Обратите внимание на то, что конфигуратор (по крайней мере до версии 1.8.05) не поддерживает подключение через TCP/IP счётчиков Меркурий 200, 201, 203 и 206. Тем не менее вы можете подключаться способом RS485/CAN к виртуальному COM порту, который будет пробрасывать все комманды через TCP/IP. Создать виртуальный порт на Windows можно при помощи утилиты [HW&nbsp;VSP3](https://www.hw-group.com/software/hw-vsp3-virtual-serial-port) |
