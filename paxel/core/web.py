"""
Je réalise ici les recherches web simples via DuckDuckGo.
Je n'utilise pas d'API payante, juste une recherche lite accessible à tous.
"""

import urllib.request
import urllib.parse
import urllib.error
import json
import re


def search_duckduckgo(query: str, max_results: int = 5) -> str:
    """
    Je lance une recherche DuckDuckGo et je retourne les résultats formatés.
    J'utilise l'API lite de DDG qui ne nécessite aucune clé.
    """
    if not query or not query.strip():
        return "❌ Requête de recherche vide."

    try:
        params = urllib.parse.urlencode({
            "q": query,
            "format": "json",
            "no_html": 1,
            "skip_disambig": 1,
        })
        url = f"https://api.duckduckgo.com/?{params}"

        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Paxel/0.1 (Linux assistant)"}
        )

        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))

        return _parse_ddg_results(data, query, max_results)

    except urllib.error.URLError:
        return "❌ Impossible d'accéder à DuckDuckGo. Vérifie ta connexion."
    except json.JSONDecodeError:
        return "❌ Erreur lors de la lecture des résultats."
    except Exception as e:
        return f"❌ Erreur de recherche : {e}"


def _parse_ddg_results(data: dict, query: str, max_results: int) -> str:
    """Je parse et formate les résultats de l'API DuckDuckGo."""
    lines = []

    # Je récupère d'abord la réponse instantanée si disponible
    abstract = data.get("Abstract", "").strip()
    abstract_url = data.get("AbstractURL", "").strip()

    if abstract:
        lines.append(f"💡 {abstract}")
        if abstract_url:
            lines.append(f"   🔗 {abstract_url}")
        lines.append("")

    # Je récupère les résultats connexes
    related = data.get("RelatedTopics", [])
    count = 0
    for topic in related:
        if count >= max_results:
            break
        if isinstance(topic, dict) and "Text" in topic:
            text = _clean_html(topic.get("Text", ""))
            url = topic.get("FirstURL", "")
            if text:
                lines.append(f"• {text}")
                if url:
                    lines.append(f"  🔗 {url}")
                count += 1

    if not lines:
        search_url = f"https://duckduckgo.com/?q={urllib.parse.quote(query)}"
        return (
            f"🔍 Aucun résultat instantané trouvé pour « {query} ».\n"
            f"🌐 Recherche complète : {search_url}"
        )

    return "\n".join(lines)


def _clean_html(text: str) -> str:
    """Je nettoie les balises HTML des résultats."""
    clean = re.sub(r"<[^>]+>", "", text)
    return clean.strip()
