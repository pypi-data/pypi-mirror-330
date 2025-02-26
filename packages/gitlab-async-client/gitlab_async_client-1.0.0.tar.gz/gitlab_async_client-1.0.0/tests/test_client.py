from urllib.parse import urljoin

import pytest

from aiohttp import ClientSession
from aioresponses import aioresponses
from src.gitlab_async_client.client import GitlabHTTPClient, GitlabAuthType
from src.gitlab_async_client.types import ProjectList
from . import mock_data


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'expected_response',
    [mock_data.get_project_list_mock],
)
async def test_get_projects(expected_response):
    base_url = 'https://gitlab.example.com/'
    access_token = 'fake_token'
    async with ClientSession() as session:
        client = GitlabHTTPClient(
            base_url, access_token, session, GitlabAuthType.header
        )

        with aioresponses() as m:
            m.get(f'{base_url}api/v4/projects', payload=expected_response)

            projects = await client.get_projects()
            assert projects == ProjectList.model_validate(expected_response)
            m.assert_called_with(
                url=urljoin(base_url, 'api/v4/projects'),
                method='GET',
                headers={'PRIVATE-TOKEN': access_token},
                params=None,
            )
