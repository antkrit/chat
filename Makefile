# target: db - runs container with database
db-run:
	docker rm -f postgresdb-container || exit 0
	docker run -d \
		--name postgresdb-container \
		-e POSTGRES_USER=${POSTGRES_USER} \
		-e POSTGRES_PASSWORD=${POSTGRES_PASSWORD} \
		-e POSTGRES_DB=${POSTGRES_DB} \
		-p ${POSTGRES_PORT}:5432 postgres:latest

db-revision:
	alembic -c "src/database/alembic.ini" revision --autogenerate -m "chat table"

db-upgrade:
	alembic -c "src/database/alembic.ini" upgrade head
