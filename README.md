# Classic Snake AI

Моя попытка научить змейку находить яблоки. Максимальный рекод 66 яблок.

## Книги которые помогли мне

1. Тарик Рашид - Создаём нейронную сеть
2. Эйял Вирсански - Генетические алгоритмы на Python
3. Эндрю Траск - Грокаем глубокое обучение

## Скриншоты

### На пути к рекоду

<img src="https://github.com/exynil/files/blob/master/classic-snake-ai/screenshots/screenshot-0.jpg">

### Видимые секторы змейки

<img src="https://github.com/exynil/files/blob/master/classic-snake-ai/screenshots/screenshot-1.jpg">

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
virtualenv classic-snake-ai
~~~~

~~~~
cd classic-snake-ai
~~~~

~~~~
source ./bin/activate
~~~~

~~~~
pip install -r requirements.txt
~~~~

~~~~
python main.py
~~~~