// git/git.go
package main

import (
	"fmt"
	"os/exec"
	"strings"
)

func GetGitDiff() (string, error) {
	cmd := exec.Command("git", "diff", "--cached")
	output, err := cmd.Output()
	if err != nil {
		return "", fmt.Errorf("failed to get git diff: %v", err)
	}
	return string(output), nil
}

func StageAllChanges() error {
	cmd := exec.Command("git", "add", ".")
	return cmd.Run()
}

func CommitChanges(commitMessage string, config Config) error {
	// Format the message based on style
	formattedMessage := FormatCommitMessage(commitMessage, config.CommitStyle)

	cmd := exec.Command("git", "commit", "-m", formattedMessage)
	return cmd.Run()
}

func PushChanges(config Config) error {
	cmd := exec.Command("git", "push")
	return cmd.Run()
}

// FormatCommitMessage formats the commit message with emoji based on style
func FormatCommitMessage(message string, style string) string {
	lines := strings.Split(strings.TrimSpace(message), "\n")
	if len(lines) == 0 {
		return message
	}

	// Extended commit type emojis
	commitTypes := map[string]string{
		"feat":      "✨",  // New feature
		"fix":       "🐛",  // Bug fix
		"docs":      "📚",  // Documentation
		"style":     "💎",  // Code style/formatting
		"refactor":  "♻️", // Code refactoring
		"perf":      "⚡️", // Performance improvements
		"test":      "🧪",  // Tests
		"chore":     "🔧",  // Maintenance
		"ci":        "👷",  // CI/CD
		"build":     "📦",  // Build system
		"revert":    "⏪",  // Revert changes
		"security":  "🔒",  // Security related
		"config":    "⚙️", // Configuration changes
		"database":  "🗄️", // Database changes
		"ui":        "🎨",  // User interface changes
		"i18n":      "🌐",  // Internationalization
		"access":    "♿",  // Accessibility
		"analytics": "📊",  // Analytics tracking
		"deprecate": "🗑️", // Deprecation notices
	}

	// Handle different commit styles
	if style == "emoji" {
		// For emoji style, add emoji to the beginning
		title := lines[0]
		if strings.Contains(title, ": ") {
			typePart := strings.Split(title, ":")[0]
			if emoji, exists := commitTypes[strings.ToLower(typePart)]; exists {
				lines[0] = fmt.Sprintf("%s %s", emoji, strings.TrimSpace(strings.SplitN(title, ":", 2)[1]))
			}
		} else {
			// Try to detect type from first word
			firstWord := strings.ToLower(strings.Fields(title)[0])
			if _, exists := commitTypes[firstWord]; exists {
				// Already has emoji or type word
			} else {
				// Add generic emoji if no type detected
				lines[0] = fmt.Sprintf("📝 %s", title)
			}
		}
	}

	// Clean up any backticks from bullet points
	for i, line := range lines {
		lines[i] = strings.ReplaceAll(line, "`", "")
	}

	return strings.Join(lines, "\n")
}
