from mcp.server.fastmcp import FastMCP
import os

mcp = FastMCP("GSANE Memory Compressor")

@mcp.tool()
def gsane_fetch_compressed_memory(query: str) -> str:
    """
    Searches through GSANE memory files and returns a summarized, compressed string relevant ONLY to the query to avoid prompt bloat.
    """
    memory_dir = "_gsane/_memory"
    results = []
    
    for root, dirs, files in os.walk(memory_dir):
        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)
                try:
                    content = open(path, "r", encoding="utf-8").read()
                    if query.lower() in content.lower():
                        idx = content.lower().find(query.lower())
                        start = max(0, idx - 150)
                        end = min(len(content), idx + 150)
                        results.append(f"[{file}] ...{content[start:end]}...")
                except Exception:
                    pass
                    
    if not results:
        return "No memory found for this query."
        
    return "COMPRESSED SUMMARY: \n" + "\n---\n".join(results[:5])

if __name__ == "__main__":
    mcp.run()
