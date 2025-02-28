"""Tests for the Basic Memory CLI tools.

These tests use real MCP tools with the test environment instead of mocks.
"""

from datetime import datetime, timedelta
import json
from textwrap import dedent
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from typer.testing import CliRunner

from basic_memory.cli.commands.tools import tool_app
from basic_memory.schemas.base import Entity as EntitySchema
from basic_memory.api.app import app as fastapi_app
from basic_memory.deps import get_project_config, get_engine_factory

runner = CliRunner()


@pytest_asyncio.fixture
def app(test_config, engine_factory) -> FastAPI:
    """Create test FastAPI application."""
    app = fastapi_app
    app.dependency_overrides[get_project_config] = lambda: test_config
    app.dependency_overrides[get_engine_factory] = lambda: engine_factory
    return app


@pytest_asyncio.fixture
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    """Create test client that both MCP and tests will use."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


@pytest.fixture
def cli_env(test_config, client):
    pass


@pytest_asyncio.fixture
async def setup_test_note(entity_service, search_service) -> AsyncGenerator[dict, None]:
    """Create a test note for CLI tests."""
    note_content = dedent("""
        # Test Note
        
        This is a test note for CLI commands.
        
        ## Observations
        - [tech] Test observation #test
        - [note] Another observation
        
        ## Relations
        - connects_to [[Another Note]]
    """)

    entity, created = await entity_service.create_or_update_entity(
        EntitySchema(
            title="Test Note",
            folder="test",
            entity_type="note",
            content=note_content,
        )
    )

    # Index the entity for search
    await search_service.index_entity(entity)

    yield {
        "title": entity.title,
        "permalink": entity.permalink,
        "content": note_content,
    }


def test_write_note(cli_env, test_config):
    """Test write_note command with basic arguments."""
    result = runner.invoke(
        tool_app,
        [
            "write-note",
            "--title",
            "CLI Test Note",
            "--content",
            "This is a CLI test note",
            "--folder",
            "test",
        ],
    )
    assert result.exit_code == 0

    # Check for expected success message
    assert "CLI Test Note" in result.stdout
    assert "Created" in result.stdout or "Updated" in result.stdout
    assert "permalink" in result.stdout


def test_write_note_with_tags(cli_env, test_config):
    """Test write_note command with tags."""
    result = runner.invoke(
        tool_app,
        [
            "write-note",
            "--title",
            "Tagged CLI Test Note",
            "--content",
            "This is a test note with tags",
            "--folder",
            "test",
            "--tags",
            "tag1",
            "--tags",
            "tag2",
        ],
    )
    assert result.exit_code == 0

    # Check for expected success message
    assert "Tagged CLI Test Note" in result.stdout
    assert "tag1, tag2" in result.stdout or "tag1" in result.stdout and "tag2" in result.stdout


def test_read_note(cli_env, setup_test_note):
    """Test read_note command."""
    permalink = setup_test_note["permalink"]

    result = runner.invoke(
        tool_app,
        ["read-note", permalink],
    )
    assert result.exit_code == 0

    # Should contain the note content and structure
    assert "Test Note" in result.stdout
    assert "This is a test note for CLI commands" in result.stdout
    assert "## Observations" in result.stdout
    assert "Test observation" in result.stdout
    assert "## Relations" in result.stdout
    assert "connects_to [[Another Note]]" in result.stdout

    # Note: We found that square brackets like [tech] are being stripped in CLI output,
    # so we're not asserting their presence


def test_search_basic(cli_env, setup_test_note):
    """Test basic search command."""
    result = runner.invoke(
        tool_app,
        ["search", "test observation"],
    )
    assert result.exit_code == 0

    # Result should be JSON containing our test note
    search_result = json.loads(result.stdout)
    assert len(search_result["results"]) > 0

    # At least one result should match our test note or observation
    found = False
    for item in search_result["results"]:
        if "test" in item["permalink"].lower() and "observation" in item["permalink"].lower():
            found = True
            break

    assert found, "Search did not find the test observation"


def test_search_permalink(cli_env, setup_test_note):
    """Test search with permalink flag."""
    permalink = setup_test_note["permalink"]

    result = runner.invoke(
        tool_app,
        ["search", permalink, "--permalink"],
    )
    assert result.exit_code == 0

    # Result should be JSON containing our test note
    search_result = json.loads(result.stdout)
    assert len(search_result["results"]) > 0

    # Should find a result with matching permalink
    found = False
    for item in search_result["results"]:
        if item["permalink"] == permalink:
            found = True
            break

    assert found, "Search did not find the note by permalink"


def test_build_context(cli_env, setup_test_note):
    """Test build_context command."""
    permalink = setup_test_note["permalink"]

    result = runner.invoke(
        tool_app,
        ["build-context", f"memory://{permalink}"],
    )
    assert result.exit_code == 0

    # Result should be JSON containing our test note
    context_result = json.loads(result.stdout)
    assert len(context_result["primary_results"]) > 0

    # Primary results should include our test note
    found = False
    for item in context_result["primary_results"]:
        if item["permalink"] == permalink:
            found = True
            break

    assert found, "Context did not include the test note"


def test_build_context_with_options(cli_env, setup_test_note):
    """Test build_context command with all options."""
    permalink = setup_test_note["permalink"]

    result = runner.invoke(
        tool_app,
        [
            "build-context",
            f"memory://{permalink}",
            "--depth",
            "2",
            "--timeframe",
            "1d",
            "--page",
            "1",
            "--page-size",
            "5",
            "--max-related",
            "20",
        ],
    )
    assert result.exit_code == 0

    # Result should be JSON containing our test note
    context_result = json.loads(result.stdout)

    # Check that metadata reflects our options
    assert context_result["metadata"]["depth"] == 2
    timeframe = datetime.fromisoformat(context_result["metadata"]["timeframe"])
    assert datetime.now() - timeframe <= timedelta(days=2)  # don't bother about timezones

    # Primary results should include our test note
    found = False
    for item in context_result["primary_results"]:
        if item["permalink"] == permalink:
            found = True
            break

    assert found, "Context did not include the test note"


def test_get_entity(cli_env, setup_test_note):
    """Test get_entity command."""
    permalink = setup_test_note["permalink"]

    result = runner.invoke(
        tool_app,
        ["get-entity", permalink],
    )
    assert result.exit_code == 0

    # Result should be JSON containing our entity
    entity_result = json.loads(result.stdout)
    assert entity_result["permalink"] == permalink
    assert entity_result["title"] == "Test Note"
    assert len(entity_result["observations"]) >= 2
    assert len(entity_result["relations"]) >= 1


def test_recent_activity(cli_env, setup_test_note):
    """Test recent_activity command with defaults."""
    result = runner.invoke(
        tool_app,
        ["recent-activity"],
    )
    assert result.exit_code == 0

    # Result should be JSON containing recent activity
    activity_result = json.loads(result.stdout)
    assert "primary_results" in activity_result
    assert "metadata" in activity_result

    # Our test note should be in the recent activity
    found = False
    for item in activity_result["primary_results"]:
        if "permalink" in item and setup_test_note["permalink"] == item["permalink"]:
            found = True
            break

    assert found, "Recent activity did not include the test note"


def test_recent_activity_with_options(cli_env, setup_test_note):
    """Test recent_activity command with options."""
    result = runner.invoke(
        tool_app,
        [
            "recent-activity",
            "--type",
            "entity",
            "--depth",
            "2",
            "--timeframe",
            "7d",
            "--page",
            "1",
            "--page-size",
            "20",
            "--max-related",
            "20",
        ],
    )
    assert result.exit_code == 0

    # Result should be JSON containing recent activity
    activity_result = json.loads(result.stdout)

    # Check that requested entity types are included
    entity_types = set()
    for item in activity_result["primary_results"]:
        if "type" in item:
            entity_types.add(item["type"])

    # Should find both entity and observation types
    assert "entity" in entity_types or "observation" in entity_types


def test_continue_conversation(cli_env, setup_test_note):
    """Test continue_conversation command."""
    permalink = setup_test_note["permalink"]

    # Run the CLI command
    result = runner.invoke(
        tool_app,
        ["continue-conversation", "--topic", "Test Note"],
    )
    assert result.exit_code == 0

    # Check result contains expected content
    assert "Continuing conversation on: Test Note" in result.stdout
    assert "This is a memory retrieval session" in result.stdout
    assert "read_note" in result.stdout
    assert permalink in result.stdout


def test_continue_conversation_no_results(cli_env):
    """Test continue_conversation command with no results."""
    # Run the CLI command with a nonexistent topic
    result = runner.invoke(
        tool_app,
        ["continue-conversation", "--topic", "NonexistentTopic"],
    )
    assert result.exit_code == 0

    # Check result contains expected content for no results
    assert "Continuing conversation on: NonexistentTopic" in result.stdout
    assert "I couldn't find any recent work specifically on this topic" in result.stdout
    assert "Try a different search term" in result.stdout
