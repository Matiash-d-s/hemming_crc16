# hemming_crc16
Global nets lab 2

Матяш Дмитрий 81 CRC-16

Вычислить контрольную сумму передаваемого сообщения.
Закодировать передаваемое сообщение кодом Хемминга с определенной длиной слова. (по вариантам)
Иметь возможность добавлять в сообщение не более n ошибок на каждое слово.
Раскодировать сообщение, исправить одиночные ошибки и определить наличие множественных ошибок (>1) в словах.
Собрать статистику с информацией о количестве исправленных ошибок, количество правильно и неправильно "доставленных" слов.
Сравнить эту информацию с внесенными ошибками из п.3
Сообщение должно быть длиной порядка 2000-3000 знаков и пробелов и содержать цифры, латинские и кириллические символы, знаки препинания. (Возьмите русскую статью с английскими терминами из Wikipedia, habr.com и т.д.)

Для проверки корректности работы нужно 3 раза отправить сообщение:

Без ошибок
С возможными ошибками (не более 1 на слово)
С множественными ошибками (более 1 на слово, но не обязательно во всех словах)

Текст использованный в алгоритме лежит в файле sample.txt (src:https://ru.wikipedia.org/wiki/Циклический_избыточный_код)

Алгоритм реализован в task.py (hemming encoder and decoder source code: https://gist.github.com/baskiton/6d361f4155f41e91c4be1dce897f7431)
