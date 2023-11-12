#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import json
import os.path
import sys
from datetime import date
def add_worker(staff, name, post, year):
   """
  Добавить данные о работнике.
  """
   staff.append(
      {
           "name": name,
           "post": post,
           "year": year
      }
  )
   return staff
def display_workers(staff):
   """
  Отобразить список работников.
  """
   # Проверить, что список работников не пуст.
   if staff:
       # Заголовок таблицы.
       line = '+-{}-+-{}-+-{}-+-{}-+'.format(
           '-' * 4,
           '-' * 30,
           '-' * 20,
           '-' * 8
      )
       print(line)
       print(
           '| {:^4} | {:^30} | {:^20} | {:^8} |'.format(
               "№",
               "Ф.И.О.",
               "Должность",
               "Год"
           )
       )
       print(line)
       # Вывести данные о всех сотрудниках.
       for idx, worker in enumerate(staff, 1):
           print(
               '| {:>4} | {:<30} | {:<20} | {:>8} |'.format(
                   idx,
                   worker.get('name', ''),
                   worker.get('post', ''),
                   worker.get('year', 0)
               )
           )
           print(line)
   else:
       print("Список работников пуст.")

   def select_workers(staff, period):
       """
      Выбрать работников с заданным стажем.
      """
       # Получить текущую дату.
       today = date.today()
       # Сформировать список работников.
       result = []
       for employee in staff:
           if today.year - employee.get('year', today.year) >= period:
               result.append(employee)
           # Возвратить список выбранных работников.
           return result

   def save_workers(file_name, staff):
       """
      Сохранить всех работников в файл JSON.
      """
       # Открыть файл с заданным именем для записи.
       with open(file_name, "w", encoding="utf-8") as fout:
           # Выполнить сериализацию данных в формат JSON.
           # Для поддержки кирилицы установим ensure_ascii=False
           json.dump(staff, fout, ensure_ascii=False, indent=4)

   def load_workers(file_name):
       """
      Загрузить всех работников из файла JSON.
         """
       # Открыть файл с заданным именем для чтения.
       with open(file_name, "r", encoding="utf-8") as fin:
           return json.load(fin)

   def main(command_line=None):
       # Создать родительский парсер для определения имени файла.
       file_parser = argparse.ArgumentParser(add_help=False)
       file_parser.add_argument(
           "filename",
           action="store",
           help="The data file name"
       )
       # Создать основной парсер командной строки.
       parser = argparse.ArgumentParser("workers")
       parser.add_argument(
           "--version",
           action="version",
           version="%(prog)s 0.1.0"
       )
       subparsers = parser.add_subparsers(dest="command")
       # Создать субпарсер для добавления работника.
       add = subparsers.add_parser(
           "add",
           parents=[file_parser],
           help="Add a new worker"
       )
       add.add_argument(
           "-n",
           "--name",
           action="store",
           required=True,
           help="The worker's name"
       )
       add.add_argument(
           "-p",
           "--post",
           action="store",
           help="The worker's post"
       )
       add.add_argument(
           "-y",
           "--year",
           action="store",
           type=int,
           required=True,
           help="The year of hiring"
       )
       # Создать субпарсер для отображения всех работников.
       _ = subparsers.add_parser(
           "display",
           parents=[file_parser],
           help="Display all workers"
       )
       # Создать субпарсер для выбора работников.
       select = subparsers.add_parser(
           "select",
           parents=[file_parser],
           help="Select the workers"
       )
       select.add_argument(
           "-P",
           "--period",
           action="store",
           type=int,
           required=True,
           help="The required period"
       )
       # Выполнить разбор аргументов командной строки.
       args = parser.parse_args(command_line)
       # Загрузить всех работников из файла, если файл существует.
       is_dirty = false
       if os.path.exists(args.filename):
           workers = load_workers(args.filename)
       else:
           workers = []
       # Добавить работника.
       if args.command == "add":
           workers = add_worker(
               workers,
               args.name,
               args.post,
               args.year
           )
           is_dirty = true
       # Отобразить всех работников.
       elif args.command == "display":
           display_workers(workers)
       # Выбрать требуемых рааботников.
       elif args.command == "select":
           selected = select_workers(workers, args.period)
           display_workers(selected)
       # Сохранить данные в файл, если список работников был изменен.
       if is_dirty:
           save_workers(args.filename, workers)

   if __name__ == "__main__":
       main()