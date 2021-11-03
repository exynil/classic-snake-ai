# Classic Snake AI

Моя попытка научить змейку находить яблоки. Максимальный рекод 66 яблок.

## Книги которые помогли мне

1. Тарик Рашид - Создаём нейронную сеть
2. Эйял Вирсански - Генетические алгоритмы на Python
3. Эндрю Траск - Грокаем глубокое обучение

## Скриншоты

<img src="https://github.com/exynil/files/blob/master/classic-snake-ai/demo/1.gif">

### На пути к рекоду

<img src="https://github.com/exynil/files/blob/master/classic-snake-ai/screenshots/1.jpg">

### Видимые секторы змейки

<img src="https://github.com/exynil/files/blob/master/classic-snake-ai/screenshots/2.jpg">

## Управление

| Клавиши | Действие                                           |
|---------|----------------------------------------------------|
| a       | Анимация                                           |
| s       | Скорость змейки                                    |
| m       | Замедление скорости змейки, при длинее более чем 5 |
| f       | След змейки                                        |
| v       | Векторы                                            |
| g       | Сетка                                              |
| i       | Информационная панель                              |

## Зависимости

1. deap
2. numpy
3. pygame

## Запуск

~~~~
git clone https://github.com/exynil/classic-snake-ai.git
~~~~

~~~~
cd classic-snake-ai
~~~~

~~~~
poetry shell
~~~~

~~~~
poetry install
~~~~

~~~~
python main.py
~~~~