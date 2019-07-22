# reportOnPopProducts
Function (and tests for it) - report on popular products with a small technical task

Из базы загружены заказы клиентов магазина в форме двух pandas.DataFrame’ов: orders и order_lines. Описание таблиц: https://docs.google.com/document/d/14rqbFnuhAi8DI4TOW0h-0z9wYAykmeH-_VsKVIhndsQ/edit
1. Строиться отчёт по популярным продуктами - функция, возвращающая pandas.DataFrame, где видны:
- самые популярные за последний месяц продукты;
- суммарная выручка по каждому такому продукту;
- средний чек заказов, в которых есть такие продукты.
2. Написаны юнит-тесты на отчёт.
