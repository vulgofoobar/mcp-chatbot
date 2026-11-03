from pydantic import Field
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

mcp = FastMCP("DocumentMCP", log_level="ERROR")

docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

# TODO: Write a tool to read a doc
@mcp.tool(
  name="read_doc_contents",
  description="Read the contents of a documente and return it as string."
)
def read_doc(
  doc_id: str = Field(description="Id of the document to read")
):
  if doc_id not in docs:
    raise ValueError(f"Doc with id {doc_id} not found")

  return docs[doc_id]

# TODO: Write a tool to edit a doc
@mcp.tool(
  name="edit_doc",
  description="Edit a document by replacing a string in the documents content with a new string."
)
def edit_doc(
  doc_id: str = Field(description="Id of the document what will be edited"),
  old_str: str = Field(description="The text to replace. Must match exactly, including whitespace."),
  new_str: str = Field(description="The new text to insert in place of the old text.")
):
  if doc_id not in docs:
    raise ValueError(f"Doc with id {doc_id} not found")

  docs[doc_id] = docs[doc_id].replace(old_str, new_str)

# TODO: Write a resource to return all doc id's
@mcp.resource(
  "docs://documents",
  mime_type="application/json"
)
def list_docs() -> list[str]:
  return list(docs.keys())

# TODO: Write a resource to return the contents of a particular doc
@mcp.resource(
  ("docs://documents/{doc_id}"),
  mime_type="text/plain"
) # ponytail: could be application/json if server returns structured data, upgrade when content-aware parsing needed
def fetch_doc(doc_id: str) -> str:
  if doc_id not in docs:
    raise ValueError(f"Doc with the {doc_id} not found")

  return docs[doc_id]

# TODO: Write a prompt to rewrite a doc in markdown format
@mcp.prompt(
  name="format",
  description="Rewrites the contents of the document in Markdonw format."
)
def format_doc(
  doc_id: str = Field(description="Id of the document to format")
) -> list[base.Message]:
  prompt = f"""
    Your goal is to reformat a document to be written with markdown syntax.

    The id of the document you need to reformat is:
    <document_id>
    {doc_id}
    </document_id>

    Add in headers, bullet points, tables, etc as necessary. Feel free to add in structure.
    Use the 'edit_doc' tool to edit the document. After the document has been reformatted...
  """

  return [base.UserMessage(prompt)]

# TODO: Write a prompt to summarize a doc
@mcp.prompt(
  name="summarize",
  description="Writes a summary of the contents of the document."
)
def summarize_doc(
  doc_id: str = Field(description="Id of the document to format")
) -> list[base.Message]:
  prompt = f"""
    Your goal is to summarize the contents of a document.

    The id of the document you need to reformat is:
    <document_id>
    {doc_id}
    </document_id>

    Focus on: key points.
    Format: write a `TLDR` section first then summarize the rest with bullet items.
    Length: word count max = 500 characters.

    Feel free to use the 'fetch_doc' tool to grab the contents of the given document.
  """

  return [base.UserMessage(prompt)]

if __name__ == "__main__":
    mcp.run(transport="stdio")
