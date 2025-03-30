import os

bearer_token = os.getenv("BEARER_TOKEN")

if bearer_token:
    print("✅ BEARER_TOKEN was successfully loaded!")
    print(f"Token length: {len(bearer_token)} characters")
else:
    print("❌ BEARER_TOKEN is missing! Check GitHub Secrets.")
