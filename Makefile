# target: db - runs container with database
db-run:
	docker rm -f postgresdb-container || exit 0
	docker run -d \
		--name postgresdb-container \
		-e POSTGRES_USER=${POSTGRES_USER} \
		-e POSTGRES_PASSWORD=${POSTGRES_PASSWORD} \
		-e POSTGRES_DB=${POSTGRES_DB} \
		-e POSTGRES_HOST=${POSTGRES_HOST} \
		-p ${POSTGRES_PORT}:5432 postgres:latest

db-revision:
	alembic -c "src/database/alembic.ini" revision --autogenerate -m "$(MSG)"

db-upgrade:
	alembic -c "src/database/alembic.ini" upgrade head

db-downgrade:
	alembic -c "src/database/alembic.ini" downgrade -1

db-populate:
	python src/database
