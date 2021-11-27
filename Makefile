# target: db-run - runs container with database
db-run:
	docker rm -f postgresdb-container || exit 0
	docker run -d \
		--name postgresdb-container \
		-e POSTGRES_USER=${POSTGRES_USER} \
		-e POSTGRES_PASSWORD=${POSTGRES_PASSWORD} \
		-e POSTGRES_DB=${POSTGRES_DB} \
		-e POSTGRES_HOST=${POSTGRES_HOST} \
		-p ${POSTGRES_PORT}:5432 postgres:latest

# target: db-revision - make new migration revision
db-revision:
	alembic -c "src/database/alembic.ini" revision --autogenerate -m "$(MSG)"

# target: db-upgrade - upgrades database to the latest revision
db-upgrade:
	alembic -c "src/database/alembic.ini" upgrade head

# target: db-downgrade - downgrades database to the previous revision
db-downgrade:
	alembic -c "src/database/alembic.ini" downgrade -1

# target: db-populate - populates database with some data
db-populate:
	python src/database
