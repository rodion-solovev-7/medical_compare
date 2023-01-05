"""
Точка входа для запуска scraper'а (парсер для внешних источников проекта)
"""
import subprocess


def main():
    spider = 'invitro_analysis'
    # spider = 'quotes'
    run_line = f'scrapy crawl {spider}'
    process = subprocess.Popen(run_line.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()


if __name__ == '__main__':
    main()
