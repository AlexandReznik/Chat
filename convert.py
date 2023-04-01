import subprocess
import locale
import codecs

# задаем строки
word1 = "разработка"
word2 = "сокет"
word3 = "декоратор"

# выводим тип и содержание переменных
print(type(word1), word1)
print(type(word2), word2)
print(type(word3), word3)

# преобразуем строки в формат Unicode
unicode_word1 = word1.encode('unicode_escape').decode()
unicode_word2 = word2.encode('unicode_escape').decode()
unicode_word3 = word3.encode('unicode_escape').decode()

# выводим тип и содержание переменных в формате Unicode
print(type(unicode_word1), unicode_word1)
print(type(unicode_word2), unicode_word2)
print(type(unicode_word3), unicode_word3)


# записываем слова в байтовом типе
word1 = b"class"
word2 = b"function"
word3 = b"method"

# определяем тип, содержимое и длину соответствующих переменных
print(type(word1), word1, len(word1))
print(type(word2), word2, len(word2))
print(type(word3), word3, len(word3))


# слова, которые нужно проверить
words = ["attribute", "класс", "функция", "type"]

# проверяем каждое слово
for word in words:
    try:
        # пытаемся записать слово в байтовом типе
        b_word = bytes(word, "ascii")
        print(f"'{word}' possible in bytes")
    except UnicodeEncodeError:
        print(f"'{word}' impossibli in bytes")


# слова в строковом представлении
words = ["разработка", "администрирование", "protocol", "standard"]

# преобразуем слова в байтовое представление и обратно
for word in words:
    # преобразование в байты
    b_word = word.encode("utf-8")
    # обратное преобразование в строку
    decoded_word = b_word.decode("utf-8")
    # выводим результаты
    print(f"'{word}' byte: {b_word}")
    print(f"'{word}' string: {decoded_word}")


# список адресов для пинга
addresses = ['google.com', 'youtube.com']

# проходим по каждому адресу и выполняем пинг
for address in addresses:
    # выполняем пинг адреса и получаем результат
    result = subprocess.run(
        ['ping', '-c', '4', address], stdout=subprocess.PIPE)
    # преобразуем результат из байтовового в строковый тип на кириллице
    decoded_result = result.stdout.decode(
        'cp866').encode('utf-8').decode('utf-8')
    # выводим результат
    print(f'Пинг ресурса {address}:\n{decoded_result}')


with open('test_file.txt', 'w') as f:
    f.write('сетевое программирование\n')
    f.write('сокет\n')
    f.write('декоратор\n')

print(locale.getpreferredencoding())

with codecs.open('test_file.txt', 'r', encoding='cp1251') as f:
    contents = f.read()

print(contents)
