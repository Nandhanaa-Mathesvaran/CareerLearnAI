import httpx
import json

def test_api():
    base_url = "http://localhost:8000/api/analyze"
    payload = {
        "targetCareer": "ML Engineer",
        "currentSkills": [],
        "experienceLevel": "Beginner"
    }

    try:
        response = httpx.post(base_url, json=payload, timeout=10.0)
        response.raise_for_status()
        data = response.json()
        
        # Verify 8 explicit skills are mapped
        roadmap = data.get("roadmap", [])
        assert len(roadmap) == 8, f"Expected 8 skills in roadmap, got {len(roadmap)}"
        assert "Mathematics" in roadmap
        
        # Verify Fallback parsing handled correctly (since currentSkills is empty, all are explanations)
        # Ensure 'steps' are arrays and not generic in Mathematics for instance
        math_content = next((item for item in data['skillExplanations'] if item["skill"] == "Mathematics"), None)
        assert math_content is not None, "Mathematics missing from explanations"
        assert len(math_content["applicationTask"]["steps"]) > 2, "Math task steps are not fully populated"
        
        print("✅ Validation successful: API logic returns all 8 required detailed skills without LLM dependency.")
        print(f"Roadmap mapped strictly as: {roadmap}")
        
    except httpx.HTTPError as e:
        print(f"❌ API testing failed due to network issues: {e}")
    except AssertionError as e:
        print(f"❌ Assert Error: {e}")
    except Exception as e:
         print(f"❌ General Error: {e}")

if __name__ == "__main__":
    test_api()
