import requests
from database import get_db

USER_FILE = "user_data.json"

def fetch_daily_question():
    url = "https://leetcode.com/graphql"
    query = {
        "query": """
        query questionOfToday {
          activeDailyCodingChallengeQuestion {
            date
            link
            question {
              title
              titleSlug
              difficulty
            }
          }
        }
        """
    }
    response = requests.post(url, json = query).json()
    q = response["data"]["activeDailyCodingChallengeQuestion"]
    question = q["question"]
    return {
        "title": question["title"],
        "titleSlug": question["titleSlug"],
        "difficulty": question["difficulty"],
        "link": "https://leetcode.com" + q["link"]
    }

def load_links():
    """Load all user links - tries database first, falls back to JSON"""
    try:
        db = get_db()
        return db.get_all_links()
    except Exception as e:
        print(f"Database error, falling back to JSON: {e}")
        import json
        try:
            with open(USER_FILE, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
def save_links(dc_id, lc_username):
    """Save user link - uses database"""
    try:
        db = get_db()
        db.save_link(str(dc_id), lc_username)
        print(f"✓ Saved {dc_id} -> {lc_username} to database")
    except Exception as e:
        print(f"Database error, falling back to JSON: {e}")
        data = load_links()
        data[str(dc_id)] = lc_username
        import json
        with open(USER_FILE, "w") as f:
            json.dump(data, f)

def get_leetcode_username(dc_id):
    """Get LeetCode username for a Discord ID"""
    try:
        db = get_db()
        return db.get_link(str(dc_id))
    except Exception as e:
        print(f"Database error, falling back to JSON: {e}")
        links = load_links()
        return links.get(str(dc_id))

def fetch_lc_stats(leetcode_username):
    url = f"https://leetcode-stats-api.herokuapp.com/{leetcode_username}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def fetch_submission(leetcode_username, problem_slug):
    """
    Fetch submission data for a user and problem.
    Note: The 'code' field requires authentication and won't be available
    through the public API. We can only get submission metadata.
    """
    url = f"https://leetcode.com/graphql"
    query = """
    query recentAcSubmissions($username: String!, $limit: Int!){
      recentAcSubmissionList(username: $username, limit:$limit){
      title
      titleSlug
      timestamp
      statusDisplay
      lang
      runtime
      memory
      url
      }
        }
        """
    variables = {
        "username": leetcode_username,
        "limit": 100
    }
    
    response = requests.post(url, json={"query": query, "variables": variables})
    
    if response.status_code == 200:
        data = response.json()
        
        # Check for errors (like private profiles)
        if "errors" in data:
            print(f"⚠️  LeetCode API error: {data['errors']}")
            return []
        
        if data.get("data") and data["data"].get("recentAcSubmissionList"):
            submissions = data["data"]["recentAcSubmissionList"]
            print(f"📊 Found {len(submissions)} total submissions for {leetcode_username}")
            
            matching_submissions = []
            for s in submissions:
                if s["titleSlug"] == problem_slug:
                    matching_submissions.append(s)
                    print(f"✅ Found matching submission for {problem_slug}")
            
            if matching_submissions:
                return matching_submissions
            else:
                print(f"❌ No submissions found for problem: {problem_slug}")
                # Show what's available
                if submissions:
                    available = [s["titleSlug"] for s in submissions[:5]]
                    print(f"💡 Recent problems: {', '.join(available)}")
    return []
def fetch_hints(problem_slug):
    url = f"https://leetcode.com/graphql"
    query = """
    query getHints($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        hints
      }
    }
    """
    variables = {
        "titleSlug": problem_slug
    }
    response = requests.post(url, json={"query": query, "variables": variables})
    if response.status_code == 200:
        data = response.json()
        hints = data["data"]["question"]["hints"]
        return hints
    return []

def fetch_random_question():
    url = "https://leetcode.com/graphql"
    query = {
        "query": """
        query questionOfToday {
          activeDailyCodingChallengeQuestion {
            date
            link
            question {
              title
              titleSlug
              difficulty
            }
          }
        }
        """
    }
    response = requests.post(url, json = query).json()
    q = response["data"]["activeDailyCodingChallengeQuestion"]
    question = q["question"]
    return {
        "title": question["title"],
        "titleSlug": question["titleSlug"],
        "difficulty": question["difficulty"],
        "link": "https://leetcode.com" + q["link"]
    }