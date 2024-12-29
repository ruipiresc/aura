import sys
import subprocess
from datetime import datetime

# File paths
VERSION_FILE = "VERSION"
CHANGELOG_FILE = "CHANGELOG.md"

# Read current version
with open(VERSION_FILE, "r") as f:
    current_version = f.read().strip()

# Split the version into major, minor, patch
major, minor, patch = map(int, current_version.split("."))

# Check bump type and ensure changelog message is provided
if len(sys.argv) < 3:
    print("Usage: python bump_version.py <bump_type> <changelog_message>")
    print("Valid bump types: patch, minor, major")
    sys.exit(1)

bump_type = sys.argv[1]
changelog_message = sys.argv[2]

# Apply the bump
if bump_type == "patch":
    patch += 1
elif bump_type == "minor":
    minor += 1
    patch = 0
elif bump_type == "major":
    major += 1
    minor = 0
    patch = 0
else:
    print("Invalid bump type. Use 'patch', 'minor', or 'major'.")
    sys.exit(1)

# Generate new version string
new_version = f"{major}.{minor}.{patch}"

# Update the VERSION file
with open(VERSION_FILE, "w") as f:
    f.write(new_version)

# Update CHANGELOG file with the provided message
with open(CHANGELOG_FILE, "a") as f:
    f.write(f"\n## [{new_version}] - {datetime.today().strftime('%Y-%m-%d')}\n")
    f.write(f"- {changelog_message}\n")

# Add all changes (staged or unstaged)
subprocess.run(["git", "add", "."])

# Commit the changes
subprocess.run(["git", "commit", "-m", f"v{new_version}: {changelog_message}"])

# Create a new Git tag for the updated version
subprocess.run(["git", "tag", f"v{new_version}"])

# Push all changes and the new tag to the repository
subprocess.run(["git", "push", "--follow-tags"])

print(f"Version bumped to {new_version}, changelog updated, and tag created.")