from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("AlvaroServer")

# Constants
POKE_API_BASE = "https://pokeapi.co"
USER_AGENT = "poke-app/1.0"

async def make_poke_request(url: str) -> dict[str, Any] | None:
    """Makes a request to Poke API."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=15.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

def format_pokemon_moves(moves: dict) -> str:
    """Formats a pokemon JSON into a readable string."""
    i=0
    s=""
    while moves[i].get('move','unknown')!='unknown':
        props = moves[i]
        s=s+f"""
Move: {props.get('name', 'Unknown')}
Url: {props.get('url', 'Unknown')}\n
"""
    return s

@mcp.tool()
async def get_moves(pokemon: str) -> str:
    """Get moves from a pokemon.

    Args:
        pokemon: full pokemon name, for instance, my favorite: Kadabra.
    """
    url = f"{POKE_API_BASE}/api/v2/pokemon/{pokemon}"
    data = await make_poke_request(url)

    if not data or "moves" not in data:
        return "Unable to fetch moves or that pokemon."

    if not data["moves"]:
        return "No moves for this pokemon."

    alerts = [format_pokemon_moves(moves) for moves in data["moves"]]
    return "\n---\n".join(alerts)

def main():
    # Initialize and run the server
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()