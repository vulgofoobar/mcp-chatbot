# what's the code to define a tool w mcp sdk?

```python
@mcp.tool(
	name="add_ints"
	description="Add two integer together (this should be long and specific)",
)
def tool_fn(
	a=Field(description="First number to add")
	b=Field(description="Second number to add"),
) -> int:
	return a + b
```
