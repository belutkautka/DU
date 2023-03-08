import datetime
from pathlib import Path
import argparse
from Disk_analyser import Disk_analyser

def parse():
    parser = argparse.ArgumentParser(description="Disk Usage")
    parser.add_argument("dir", type=str, help='Директория для измерения размера. '
                                              'Например: D:\Programs')
    parser.add_argument('-p', '--print', action='store_true', help='Напечатает файлы в директории и их размер')
    parser.add_argument('-unr', "--unread", action='store_true',
                        help='Напечатается список папок, размер которых не удалось посчитать')
    parser.add_argument('-e', '--ext', nargs='+', type=str, help='Посчитает только файлы с заданным расширением')
    parser.add_argument('-md', '--max_depth', type=int, default=2147483647,
                        help='Посчитает только те файлы, у которых глубина вложенности меньше или равна заданной')
    parser.add_argument('-d', '--dates', nargs='+', type=str,
                        help='Посчитает только файлы с указанными днями.'
                             'Необходимо указать день в формате день.месяц.год (цифрами)')
    parser.add_argument('-ow', '--owners', nargs='+', type=str, help='Посчитает только файлы с указанными владельцами.')
    return parser

def main():

    parser=parse()
    args = parser.parse_args()
    dates = args.dates

    if dates != None:
        dates = []
        for date in args.dates:
            try:
                d = datetime.datetime.strptime(date, '%d.%m.%Y')
                dates.append(d.date())
            except:
                print('Неправильный формат времени. Необходим формат: день.месяц.год (цифрами)')
                exit()
    analyser=Disk_analyser(Path(args.dir), args.max_depth, args.ext, args.print, dates, args.unread, args.owners)
    analyser.print_results()


if __name__ == '__main__':
    main()
