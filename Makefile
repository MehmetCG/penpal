build:
	docker-compose build
up:
	docker-compose up
restart:
	docker-compose restart
stop:
	docker-compose stop
destroy:
	docker-compose down
ps:
	docker-compose ps
django-shell:
	docker-compose exec web python manage.py shell
createsuperuser:
	docker-compose exec web python manage.py createsuperuser
psql:
	docker-compose exec db psql -U myuser mydb
migrate:
	docker-compose exec web python manage.py migrate
makemigrations:
	docker-compose exec web python manage.py makemigrations
showmigrations:
	docker-compose exec web python manage.py showmigrations
test:
	docker-compose exec web python manage.py test
