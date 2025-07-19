up:
	docker-compose down
	docker-compose up --build

fe:
	cd frontend && yarn docker
