from mcp.server.fastmcp import FastMCP

mcp = FastMCP("keyword-search")

@mcp.tool()
def search_keyword_in_file(
    keyword: str,
    file_path: str = None,
    content: str = None,
    case_sensitive: bool = False
) -> str:
    try:

        if content:
            lines = content.splitlines()
        elif file_path:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.read().splitlines()
        else:
            return "Error: Either file_path or content must be provided"
        
        matches = []
        search_keyword = keyword if case_sensitive else keyword.lower()
        
        for line_num, line in enumerate(lines, start=1):
            search_line = line if case_sensitive else line.lower()
            if search_keyword in search_line:
                matches.append({
                    "line_number": line_num,
                    "content": line.rstrip()
                })
        
        source = file_path if file_path else "the provided text"
        if matches:
            result = f"Found {len(matches)} occurrence(s) of '{keyword}' in {source}:\n\n"
            for match in matches:
                result += f"Line {match['line_number']}: {match['content']}\n"
        else:
            result = f"No occurrences of '{keyword}' found in {source}"
        
        return result
        
    except FileNotFoundError:
        return f"Error: File not found: {file_path}"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    mcp.run()