[![package test](https://github.com/Vladimir-Titov/gitlab-async-client/actions/workflows/package-test.yml/badge.svg?branch=main)](https://github.com/Vladimir-Titov/gitlab-async-client/actions/workflows/package-test.yml)

```
import aiohttp
import asyncio
from gitlab_async_client.client import GitlabHTTPClient, GitlabAuthType

async def main():
    async with aiohttp.ClientSession() as session:
        client = GitlabHTTPClient(
            base_url="https://gitlab.com",
            access_token="your_access_token",
            session=session,
            auth_type=GitlabAuthType.header
        )

        projects = await client.get_projects()
        print(projects)


asyncio.run(main())
```

