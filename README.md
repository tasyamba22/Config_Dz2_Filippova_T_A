# Конфигурационное управление
Вариант 30<br/>
Задание № 2<br/>
Разработать инструмент командной строки для визуализации графа зависимостей, включая транзитивные зависимости. Сторонние средства для получения зависимостей использовать нельзя.<br/>
Зависимости определяются по имени пакета языка JavaScript (npm). Для описания графа зависимостей используется представление Graphviz.<br/>
Визуализатор должен выводить результат на экран в виде кода.<br/>
Ключами командной строки задаются:<br/>
• Путь к программе для визуализации графов.<br/>
• Имя анализируемого пакета.<br/>
• Путь к файлу-результату в виде кода.<br/>
• URL-адрес репозитория.<br/>
Все функции визуализатора зависимостей должны быть покрыты тестами.<br/>
***
## 1. Общее описание<br/>
Проект предназначен для визуализации зависимостей пакетов. Он автоматически строит граф 
зависимостей указанного пакета, используя API репозитория, в моем варианте nmp (Node Package 
Manager), и создает файл в формате Graphviz.<br/>
Файл можно использовать для генерации визуального графа с помощью утилиты Graphviz. Скрипт 
работает с транзитивными зависимостями (зависимости зависимостей) и генерирует наглядное 
представление всех связей между пакетами.<br/>
Мы запускаем Python-скрипт configgraf.py с указанием дополнительных параметров через 
командную строку. Эти аргументы передают скрипту необходимую информацию для его работы, в 
моем варианте, путь к Graphviz,имя пакета, путь к файлу-результату в виде кода и URL 
репозитория.<br/>
```
python configgraf.py 
--graphviz-path "Путь к Graphviz" 
--package-name "Имя пакета" 
--output-path "Путь к файлу-результату в виде кода"
--repo-url "Url репозитория"
```
## 2. Описание всех функций и настроек <br/> 
**Функции:**<br/>
1. `fetch_package_dependencies(pkg_name, api_url)`<br/>
Получает зависимости указанного пакета из API репозитория.<br/>
*Параметры:*
  -   `pkg_name`: Имя пакета. <br/>
  -   `api_url`: URL API репозитория.<br/>
*Возвращает:* Словарь с зависимостями пакета.<br/>
2. `generate_graphviz_content(dependency_map)`<br/>
Создает текстовое описание графа зависимостей в формате Graphviz.<br/>
*Параметры:*
  -  `dependency_map`: Словарь зависимостей пакета. <br/>
*Возвращает:* Строку с кодом Graphviz.<br/>
3. `build_dependency_graph`<br/>
Рекурсивно строит граф зависимостей, включая транзитивные зависимости.<br/>
*Параметры:*
  -  `pkg_name`: Имя пакета.<br/>
  -  `api_url`: URL API репозитория.<br/>
  -  `graph`: Граф зависимостей (по умолчанию пустой словарь).<br/>
  -  `processed`: Множество уже обработанных пакетов.<br/>
*Возвращает:* Словарь, представляющий граф зависимостей.<br/>
4. `save_to_file(filepath, content)`<br/>
Сохраняет текстовое содержание в указанный файл.<br/>
*Параметры:*
  -  `filepath`: Путь к файлу.<br/>
  -  `content`: Содержимое для сохранения.<br/>
*Исключения:*  Обрабатывает ошибки записи в файл.<br/>
5.  `parse_arguments()`<br/>
Обрабатывает аргументы командной строки.<br/>
*Возвращает:* Объект с аргументами.<br/>
## 3. Описание команд для сборки проекта.<br/>
Для работы проекта требуется Python и установленный Graphviz.<br/>
### Установка зависимостей:<br/>
1. Установите Python версии 3.7+<br/>
2. Установите Graphviz с официального сайта.<br/>
### Запуск программы:<br/>
Пример вызова программы через командную строку:<br/>
```
 python configgraf.py --graphviz-path "C:\Program Files\Graphviz\bin\dot.exe" --package-name "mongoose" --output-path "C:\Users\Taisi\PycharmProjects\Config_Dz2\dependencies_mongoose.dot" --repo-url "https://registry.npmjs.com"
```
### Сгенерировать граф<br/>
После запуска проекта результат будет сохранен в файл dependencies_mongoose.dot. <br/>
Чтобы преобразовать его в изображение, выполните: <br/>
```dot -Tpng dependencies_mongoose.dot -o dependencies_mongoose.png```<br/>
## 4. Примеры использования 
**Код зависимостей:** <br/>
![image](https://github.com/user-attachments/assets/999367ec-0fea-4713-9d38-1a7ccd5f3e54)
**Граф зависимостей:** <br/>
![dependencies_mongoose](https://github.com/user-attachments/assets/0949c6db-457f-4c32-a08f-56505f6d85c2)
**Вывод кода графа в терминал:** <br/>
![image](https://github.com/user-attachments/assets/65dcd8ba-f6ad-4327-9bd2-b53d733a9386)
## 5. Результаты тестов <br/>
Выполнение тестирования:<br/>
C:\Users\Taisi\PycharmProjects\Config_Dz2\.venv\Scripts\python.exe "D:/PyCharm Community Edition 2024.3/plugins/python-ce/helpers/pycharm/_jb_unittest_runner.py" --path C:\Users\Taisi\PycharmProjects\Config_Dz2\test.py 
Testing started at 23:05 ...
Launching unittests with arguments python -m unittest C:\Users\Taisi\PycharmProjects\Config_Dz2\test.py in C:\Users\Taisi\PycharmProjects\Config_Dz2
Результат сохранен в файл: test_output.dot

Ran 4 tests in 0.004s

OK

Process finished with exit code 0
![image](https://github.com/user-attachments/assets/0769bfbd-46a2-4f93-8d17-3332fbacdb22)
