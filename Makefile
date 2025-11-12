# General tasks.
# --------------------------------------------------------------------------------------
format:
	ruff check --select I --fix . \
	ruff format .

format-entrypoint:
	dos2unix entrypoint.sh

create-migration:
	beanie new-migration -n $(MIGRATION_NAME) -p beanie/migrations

# App tasks.
# --------------------------------------------------------------------------------------
launch-app:
	uv run launch_app.py

test-app:
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf tests/reports
	pytest tests/ -v -o junit_family=xunit1 --cov=app --cov-report xml:tests/reports/coverage/report.xml --cov-report html:tests/reports/html --junitxml=tests/reports/xunit/report.xml

# MongoDB tasks.
# --------------------------------------------------------------------------------------
migrate-beanie:
	uv run migrate_beanie.py

# Application and MongoDB containers tasks.
# --------------------------------------------------------------------------------------
startup-app:
	docker-compose up --build -d app

shutdown-app:
	docker-compose down -v app

startup-mongodb:
	docker-compose up --build -d mongodb

shutdown-mongodb:
	docker-compose down -v mongodb