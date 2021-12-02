# target: db-run - runs container with database
db-run:
	docker rm -f postgresdb-container || exit 0
	docker run -d \
		--name postgresdb-container \
		-e POSTGRES_USER=${POSTGRES_USER} \
		-e POSTGRES_PASSWORD=${POSTGRES_PASSWORD} \
		-e POSTGRES_DB=${POSTGRES_DB} \
		-e POSTGRES_HOST=${POSTGRES_HOST} \
		-p ${POSTGRES_PORT}:5432 \
		postgres:latest postgres -c log_statement=all

# target: db-revision - make new migration revision
db-revision:
	alembic -c "src/database/migrations/alembic.ini" revision --autogenerate -m "$(msg)"

# target: db-upgrade - upgrades database to the latest revision
db-upgrade:
	alembic -c "src/database/migrations/alembic.ini" upgrade head

# target: db-downgrade - downgrades database to the previous revision
db-downgrade:
	alembic -c "src/database/migrations/alembic.ini" downgrade -1

# target: db-populate - populates database with some data
db-populate:
	python src/database

# target: db-logs - gets logs from container
db-logs:
	docker logs postgresdb-container

# target: test - run tests from tests/ folder
test:
	pytest --cov-report term-missing --cov