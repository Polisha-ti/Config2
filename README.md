Задание #2
Разработать инструмент командной строки для визуализации графа зависимостей, включая транзитивные зависимости. Сторонние средства для получения зависимостей использовать нельзя.
Зависимости определяются для git-репозитория. Для описания графа зависимостей используется представление PlantUML. Визуализатор должен выводить результат на экран в виде кода.
Построить граф зависимостей для коммитов, в узлах которого находятся связи с файлами и папками, представленными уникальными узлами. Граф 
Ключами командной строки задаются:
Путь к программе для визуализации графов. Путь к анализируемому репозиторию.
Путь к файлу-результату в виде кода.
Дата коммитов в репозитории.
Все функции визуализатора зависимостей должны быть покрыты тестами.
