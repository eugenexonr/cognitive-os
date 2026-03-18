#!/usr/bin/env bash
# Cognitive OS — Framework Update Script
# Updates framework files (templates, drivers, docs) WITHOUT touching user content.
#
# Usage:
#   ./cog-update.sh              # Interactive update
#   ./cog-update.sh --check      # Show available updates (no changes)
#   ./cog-update.sh --dry-run    # Preview changes without applying
#   ./cog-update.sh --force      # Apply without prompts
#
# Framework files (auto-updatable):
#   templates/          — kernel, decisions, insight, protocol templates
#   drivers/            — platform-specific skills (Claude Code, Cursor, Codex)
#   docs/               — documentation
#   examples/           — anonymized usage examples
#   README.md           — project readme
#   PROJECT-PLAN.md     — project plan
#   cog-update.sh       — this script
#
# User content (NEVER modified):
#   kernel.md           — user's personalized kernel
#   decisions.md        — user's decision history
#   insight.md          — user's insights
#   MEMORY.md           — user's memory index
#   inbox.md            — user's capture inbox
#   protocols/          — user's customized protocols

set -euo pipefail

COG_DIR="$(cd "$(dirname "$0")" && pwd)"
COG_VERSION_FILE="$COG_DIR/COG-VERSION"
REMOTE_URL="https://raw.githubusercontent.com/eugenexonr/cognitive-os/main"

# Colors (if terminal supports them)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Framework files that CAN be updated
FRAMEWORK_FILES=(
  "templates/kernel.template.md"
  "templates/decisions.template.md"
  "templates/insight.template.md"
  "templates/MEMORY.template.md"
  "templates/protocols/boris.md"
  "templates/protocols/anti-drift.md"
  "templates/protocols/boot.md"
  "drivers/claude-code/cos-boot/SKILL.md"
  "drivers/claude-code/cos-boris/SKILL.md"
  "drivers/claude-code/cos-careful/SKILL.md"
  "drivers/claude-code/cos-decide/SKILL.md"
  "drivers/claude-code/cos-insight/SKILL.md"
  "drivers/claude-code/cos-capture/SKILL.md"
  "drivers/cursor/.cursorrules.template"
  "docs/GETTING-STARTED.md"
  "docs/ARCHITECTURE.md"
  "README.md"
  "PROJECT-PLAN.md"
)

# User content files that MUST NOT be touched
USER_FILES=(
  "kernel.md"
  "decisions.md"
  "insight.md"
  "MEMORY.md"
  "inbox.md"
  "protocols/boris.md"
  "protocols/anti-drift.md"
)

current_version() {
  if [ -f "$COG_VERSION_FILE" ]; then
    cat "$COG_VERSION_FILE"
  else
    echo "0.0.0"
  fi
}

log_info() { echo -e "${GREEN}[cog-update]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[cog-update]${NC} $1"; }
log_error() { echo -e "${RED}[cog-update]${NC} $1"; }

# Safety check: verify we're in a Cognitive OS directory
verify_cog_dir() {
  if [ ! -f "$COG_DIR/README.md" ] || [ ! -d "$COG_DIR/templates" ]; then
    log_error "Not a Cognitive OS directory: $COG_DIR"
    log_error "Run this script from the cognitive-os/ root."
    exit 1
  fi
}

# Check for changes between local framework files and upstream
check_updates() {
  log_info "Current version: $(current_version)"
  log_info "Checking framework files for changes..."

  local changes=0
  for file in "${FRAMEWORK_FILES[@]}"; do
    local local_path="$COG_DIR/$file"
    if [ ! -f "$local_path" ]; then
      log_warn "  NEW: $file (not yet installed)"
      changes=$((changes + 1))
    fi
  done

  # If this is a git repo, use git status
  if [ -d "$COG_DIR/.git" ]; then
    local modified
    modified=$(cd "$COG_DIR" && git diff --name-only HEAD 2>/dev/null | grep -E '^(templates/|drivers/|docs/|README|PROJECT)' || true)
    if [ -n "$modified" ]; then
      log_warn "  Local modifications to framework files:"
      echo "$modified" | while read -r f; do
        log_warn "    MODIFIED: $f"
        changes=$((changes + 1))
      done
    fi
  fi

  if [ "$changes" -eq 0 ]; then
    log_info "All framework files are up to date."
  else
    log_warn "$changes file(s) have available updates."
  fi
}

# Verify user content is safe
verify_user_content() {
  log_info "Verifying user content is protected..."
  for file in "${USER_FILES[@]}"; do
    local path="$COG_DIR/$file"
    if [ -f "$path" ]; then
      log_info "  PROTECTED: $file ($(wc -l < "$path") lines)"
    fi
  done
}

# Update framework files from git
update_from_git() {
  local mode="${1:-interactive}"

  if [ ! -d "$COG_DIR/.git" ]; then
    log_error "Not a git repository. Use 'git clone' to set up, then run update."
    exit 1
  fi

  # Stash any user changes to framework files
  cd "$COG_DIR"

  # Fetch latest
  log_info "Fetching latest from remote..."
  git fetch origin main 2>/dev/null || {
    log_error "Could not fetch from remote. Check your network connection."
    exit 1
  }

  # Show what would change
  local diff_output
  diff_output=$(git diff origin/main -- "${FRAMEWORK_FILES[@]}" 2>/dev/null || true)

  if [ -z "$diff_output" ]; then
    log_info "No framework updates available."
    return
  fi

  log_info "Framework updates available:"
  git diff --stat origin/main -- "${FRAMEWORK_FILES[@]}" 2>/dev/null

  if [ "$mode" = "dry-run" ]; then
    log_info "(dry-run) No changes applied."
    return
  fi

  if [ "$mode" = "interactive" ]; then
    echo ""
    read -rp "Apply framework updates? User content will NOT be modified. [y/N] " confirm
    if [[ ! "$confirm" =~ ^[yY]$ ]]; then
      log_info "Update cancelled."
      return
    fi
  fi

  # Checkout only framework files from origin/main
  for file in "${FRAMEWORK_FILES[@]}"; do
    if git show "origin/main:$file" &>/dev/null; then
      git checkout origin/main -- "$file" 2>/dev/null && \
        log_info "  Updated: $file" || \
        log_warn "  Skipped: $file (not in remote)"
    fi
  done

  log_info "Framework update complete."
  log_info "User content untouched: kernel.md, decisions.md, insight.md, MEMORY.md"
}

# Main
verify_cog_dir

case "${1:-}" in
  --check)
    check_updates
    verify_user_content
    ;;
  --dry-run)
    check_updates
    verify_user_content
    update_from_git "dry-run"
    ;;
  --force)
    verify_user_content
    update_from_git "force"
    ;;
  *)
    verify_user_content
    update_from_git "interactive"
    ;;
esac
