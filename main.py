import json
import os
import sys
import urllib.error
import urllib.request

os.system("cls")


def fetch_github_activity(username):
    url = f"https://api.github.com/users/{username}/events"

    try:
        with urllib.request.urlopen(url) as response:
            data = response.read()
            events = json.loads(data)
            return events

    except urllib.error.HTTPError as e:
        if e.code == 404:
            print("user not found")
        else:
            print(f"http error: {e.code}")
        return None
    except urllib.error.URLError:
        print("failed to reach github, perhaps fix ur terrible internet?")
        return None
    except json.JSONDecodeError:
        print("failed to parse the response")
        return None


def display_activity(events):
    if not events:
        print("no recent activity found")
        return

    print("\nRecent github activity:\n")

    for event in events[:10]:
        event_type = event["type"]
        repo_name = event["repo"]["name"]

        if event_type == "PushEvent":
            commits = len(event["payload"]["commits"])
            print(f"- Pushed {commits} commit(s) to {repo_name}")
        elif event_type == "IssueEvent":
            action = event["payload"]["action"]
            print(f"- {action.capitalize()} an issue in {repo_name}")
        elif event_type == "WatchEvent":
            print(f"- starred {repo_name}")
        elif event_type == "ForkEvent":
            print(f"- forked {repo_name}")
        elif event_type == "CreateEvent":
            ref_type = event["payload"]["ref_type"]
            print(f"- created new {ref_type} in {repo_name}")
        else:
            print(f"- {event_type} in {repo_name}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <github username>")
        return

    username = sys.argv[1]
    events = fetch_github_activity(username)

    if events is not None:
        display_activity(events)


if __name__ == "__main__":
    main()
