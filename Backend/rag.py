import json
import os
from typing import List, Tuple, Dict, Any

THIS_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(THIS_DIR, "..", "data", "employees.json")

def load_employees() -> List[Dict[str, Any]]:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        db = json.load(f)
    return db.get("employees", [])

class RAGEngine:
    def __init__(self, employees: List[Dict[str, Any]] = None):
        self.employees = employees or load_employees()

    def _match_skill(self, emp: dict, skill: str) -> bool:
        return any(skill.lower() == s.lower() or skill.lower() in s.lower() for s in emp.get("skills", []))

    def _match_project(self, emp: dict, project: str) -> bool:
        return any(project.lower() == p.lower() or project.lower() in p.lower() for p in emp.get("projects", []))

    def search(self, query: str) -> List[dict]:
        """
        Naive retrieval: parse tokens and return candidates from JSON.
        Supports:
          - skill matching (if token matches a skill string)
          - project matching
          - name matching
          - experience filter like '3+' or '3 years'
        This function only returns employees from the JSON.
        """
        q = query.lower().strip()
        tokens = [t.strip() for t in q.replace("+", " +").split() if t.strip()]
        results = []

        # Extract numeric experience requirement if present (e.g., "3+", "5 years", "5 years experience")
        min_exp = None
        for t in tokens:
            try:
                if t.endswith("+"):
                    min_exp = int(t[:-1])
                elif t.isdigit():
                    min_exp = int(t)
                elif t.replace("years", "").strip().isdigit():
                    min_exp = int(t.replace("years", "").strip())
            except:
                pass

        # search logic: look for any token in skills, projects or name
        for emp in self.employees:
            matched = False

            # experience filter
            if min_exp is not None and emp.get("experience_years", 0) < min_exp:
                continue

            # check name
            if any(tok in emp.get("name", "").lower() for tok in tokens):
                matched = True

            # check skills
            for tok in tokens:
                if any(tok == s.lower() or tok in s.lower() for s in emp.get("skills", [])):
                    matched = True
                    break

            # check projects
            if not matched:
                for tok in tokens:
                    if any(tok == p.lower() or tok in p.lower() for p in emp.get("projects", [])):
                        matched = True
                        break

            if matched:
                results.append(emp)

        # dedupe and return
        unique = []
        seen_ids = set()
        for r in results:
            if r["id"] not in seen_ids:
                unique.append(r)
                seen_ids.add(r["id"])
        return unique

    def generate_response(self, query: str, employees: List[dict]) -> str:
        """Simple template-based natural response (no external LLM)."""
        if not employees:
            return f"Sorry — I couldn't find any employees matching: '{query}'."

        lines = [f"Based on your query '{query}', I found {len(employees)} candidate(s):\n"]
        for emp in employees:
            lines.append(
                f"• {emp['name']} — {emp.get('role','')}, {emp.get('department','')}\n"
                f"  Experience: {emp.get('experience_years', '?')} years\n"
                f"  Skills: {', '.join(emp.get('skills', []))}\n"
                f"  Projects: {', '.join(emp.get('projects', []))}\n"
                f"  Availability: {emp.get('availability', 'unknown')}\n"
            )
        lines.append("\nWould you like more details about any candidate (e.g., 'More about Alice Johnson')?")
        return "\n".join(lines)

# instantiate engine (module-level)
engine = RAGEngine()
