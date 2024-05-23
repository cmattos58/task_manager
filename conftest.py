from django.db import OperationalError, connections
import pytest
from django.core.management import call_command

@pytest.fixture(scope='session')
def django_db_setup():
    """Ensure the test schema exists."""
    from django.conf import settings
    test_db_name = settings.DATABASES['default']['NAME']
    test_db_user = settings.DATABASES['default']['USER']
    
    with connections['default'].cursor() as cursor:
        try:
            cursor.execute(f"CREATE SCHEMA IF NOT EXISTS test_task_manager AUTHORIZATION {test_db_user};")
        except OperationalError as e:
            print(f"Error creating schema: {e}")

@pytest.fixture(scope='session')
def setup_test_environment():
    """
    Apply migrations in the test database.
    """
    call_command('migrate')

@pytest.fixture(autouse=True)
def apply_migrations(setup_test_environment):
    pass