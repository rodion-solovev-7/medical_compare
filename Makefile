help:             ## Показывает все команды из Makefile
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

check:            ## Показывает состояние сервисов
	docker compose -f ./docker-compose.yml ps

local:            ## Поднимает БД и др. необходимые сервисы из docker-compose.yml. Сам сервер и пр. нужно запускать руками
	docker compose -f ./docker-compose.yml up --build -d postgres

down:             ## Отключает ВСЕ сервисы из docker-compose.yml
	docker compose -f ./docker-compose.yml down

volumes:          ## Отключает ВСЕ сервисы из docker-compose.yml и чистит их Volumes (например обнуляет БД)
	docker compose -f ./docker-compose.yml down --volumes
