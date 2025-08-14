from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp import ClientSession
import asyncio
import json

server = StdioServerParameters(
    command='copy-ai-mcp',  # Replace with the actual path to your Python interpreter
    args=[
    ],
    env={
        "COPY_AI_API_KEY": "your copy.ai api key here",  # Replace with your actual Copy.ai API key
    }
)


async def main():
    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            try:
                response = await session.list_tools()
                tools = response.model_dump()['tools']
                print(len(tools), "tools found:")
                print(json.dumps(tools, indent=4, ensure_ascii=False))
            except Exception as e:
                print(f"Error listing tools: {e}")

            try:
                response = await session.list_prompts()
                prompts = response.model_dump()['prompts']
                print(json.dumps(prompts, indent=4, ensure_ascii=False))
            except Exception as e:
                print(f"Error listing prompts: {e}")

            try:
                response = await session.list_resources()
                resources = response.model_dump()['resources']
                print(json.dumps(resources, indent=4, ensure_ascii=False, default=str))
            except Exception as e:
                print(f"Error listing resources: {e}")

            try:
                response = await session.list_resource_templates()
                resource_templates = []
                for res in response.model_dump()['resourceTemplates']:
                    res['uri'] = res['uriTemplate']
                    resource_templates.append(res)
                print(json.dumps(resource_templates, indent=4, ensure_ascii=False))
            except Exception as e:
                print(f"Error listing resource templates: {e}")

            try:
                response = await session.call_tool(
                    'get_workflow_run',
                    arguments={
                        'workflow_id': "111",
                        'run_id': "222"
                    }
                )
                result = response.model_dump()['content']
                print(json.dumps(result, indent=4, ensure_ascii=False))
            except Exception as e:
                print(f"Error calling tool : {e}")


if __name__ == "__main__":
    asyncio.run(main())
