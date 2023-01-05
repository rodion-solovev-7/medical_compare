help:        ## Показывает все команды из Makefile
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

ps:          ## Показывает состояние сервисов
	docker compose ps

local:       ## Поднимает БД и др. необходимые сервисы из docker-compose.yml (и .override.yml). Сам сервер и пр. нужно запускать руками
	docker compose up --build -d postgres

tor:         ## Поднимает БД и др. необходимые сервисы из docker-compose.yml (и .override.yml). Сам сервер и пр. нужно запускать руками
	docker compose up --build -d http-socks5-proxy

up:          ## Поднимает ВСЕ сервисы из docker-compose.yml (и .override.yml)
	docker compose up --build -d web jobs scraper

down:        ## Отключает ВСЕ сервисы из docker-compose.yml
	docker compose down --remove-orphans

destroy:     ## Отключает ВСЕ сервисы из docker-compose.yml и чистит их Volumes (например обнуляет БД)
	docker compose down --volumes

runweb:      ## Запускает веб-сервер локально (не в контейнере). Подразумевается, что БД и другие сервисы уже запущены
	PYTHONPATH=. python3.10 __entry_points__/server.py

runjobs:     ## Запускает обработчик периодических задач локально (не в контейнере). Подразумевается, что БД и другие сервисы уже запущены
	PYTHONPATH=. python3.10 __entry_points__/periodic_tasks.py

runscraper:  ## Запускает парсер локально (не в контейнере). Подразумевается, что БД и другие сервисы уже запущены
	PYTHONPATH=. python3.10 __entry_points__/scraper.py
