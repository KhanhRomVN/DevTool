// main.go - Enhanced version with API key rotation support
package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"

	"dev_tool/ai"
	"dev_tool/config"
	"dev_tool/git"
	"dev_tool/messages"
	"dev_tool/ui"

	"github.com/spf13/cobra"
)

var (
	version = "2.0.6"
)

func main() {
	var rootCmd = &cobra.Command{
		Use:   "dev_tool",
		Short: "Dev Tool - AI-powered Git Commit Message Generator",
		Long: `🛠️  Dev Tool - AI-powered Git Commit Message Generator

Features:
- AI-powered commit message generation with multiple API key support
- Automatic API key rotation and fallback
- Multi-language support (English/Vietnamese)
- Multiple commit styles
- Account and API key management
- Cross-platform compatibility`,
		Version: version,
		Run: func(cmd *cobra.Command, args []string) {
			// Check if the first argument is "." - if so, run auto-commit
			if len(args) > 0 && args[0] == "." {
				cfg := config.LoadConfig()
				HandleAutoCommit(false, cfg)
				return
			}

			// If no arguments, show help
			if len(args) == 0 {
				cmd.Help()
				return
			}

			// For any other arguments, show help
			cmd.Help()
		},
	}

	rootCmd.AddCommand(
		newAutoCommitCmd(),
		newSettingsCmd(),
		newDotCmd(),
		newAccountCmd(), // New account management command
	)

	if err := rootCmd.Execute(); err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)
		os.Exit(1)
	}
}

func newAutoCommitCmd() *cobra.Command {
	var noPush bool

	cmd := &cobra.Command{
		Use:   "auto-commit",
		Short: "Generate and commit with AI message",
		Long: `Generate commit message using AI with automatic API key rotation.

The tool will automatically try different API keys if one fails due to:
- Rate limit exceeded
- Invalid API key
- Expired API key
- Quota exceeded`,
		Run: func(cmd *cobra.Command, args []string) {
			cfg := config.LoadConfig()
			HandleAutoCommit(noPush, cfg)
		},
	}

	cmd.Flags().BoolVar(&noPush, "no-push", false, "Skip automatic push after commit")
	return cmd
}

// Add explicit dot command for better help documentation
func newDotCmd() *cobra.Command {
	var noPush bool

	cmd := &cobra.Command{
		Use:   ".",
		Short: "Quick commit with AI-generated message (alias for auto-commit)",
		Long: `Quick commit with AI-generated message using automatic API key rotation.

This is a shortcut for the auto-commit command, allowing you to simply run:
  dev_tool .

Instead of:
  dev_tool auto-commit

Features automatic API key failover for reliability.`,
		Run: func(cmd *cobra.Command, args []string) {
			cfg := config.LoadConfig()
			HandleAutoCommit(noPush, cfg)
		},
	}

	cmd.Flags().BoolVar(&noPush, "no-push", false, "Skip automatic push after commit")
	return cmd
}

func newSettingsCmd() *cobra.Command {
	return &cobra.Command{
		Use:   "settings",
		Short: "Open settings menu",
		Long: `Open the interactive settings menu to configure:

- Account and API key management
- Language preferences (UI and commit messages)
- AI model selection
- Commit message styles
- Auto-push and auto-stage settings`,
		Run: func(cmd *cobra.Command, args []string) {
			cfg := config.LoadConfig()
			ShowSettingsMenu(cfg)
		},
	}
}

// New account management command
func newAccountCmd() *cobra.Command {
	return &cobra.Command{
		Use:   "accounts",
		Short: "Manage Gemini accounts and API keys",
		Long: `Interactive account and API key management.

Manage multiple Gemini accounts with multiple API keys per account:
- Add/remove accounts
- Add/remove API keys
- Set primary account
- View API key status and usage statistics
- Test API key functionality`,
		Run: func(cmd *cobra.Command, args []string) {
			cfg := config.LoadConfig()
			cfg = ui.ShowAccountManager(cfg)
			config.SaveConfig(cfg)
		},
	}
}

// Enhanced HandleAutoCommit with improved API key rotation support
func HandleAutoCommit(noPush bool, cfg config.Config) {
	// Check if we have any accounts configured
	primaryAccount := config.GetPrimaryAccountWithFallback(cfg)
	if primaryAccount == nil {
		messages.PrintError(messages.GetMessage("no_accounts", cfg))
		messages.PrintInfo("Run 'dev_tool settings' to configure your accounts.")
		return
	}

	// Check if we have any active API keys
	availableKeys := config.GetAllAvailableAPIKeys(cfg)
	if len(availableKeys) == 0 {
		messages.PrintError(messages.GetMessage("no_active_api_keys", cfg))
		messages.PrintInfo("Run 'dev_tool accounts' to manage your API keys.")
		return
	}

	messages.PrintInfo(fmt.Sprintf("🔑 Found %d available API key(s) across %d account(s)",
		len(availableKeys),
		countActiveAccounts(cfg)))

	// Auto-stage if enabled
	if cfg.AutoStage {
		messages.PrintInfo("📦 Auto-staging changes...")
		if err := git.StageAllChanges(); err != nil {
			messages.PrintError(fmt.Sprintf("%s: %v", messages.GetMessage("git_error", cfg), err))
			return
		}
		messages.PrintSuccess("✅ Changes staged successfully")
	}

	// Get git diff
	diff, err := git.GetGitDiff()
	if err != nil {
		messages.PrintError(fmt.Sprintf("%s: %v", messages.GetMessage("git_error", cfg), err))
		return
	}

	if strings.TrimSpace(diff) == "" {
		messages.PrintWarning(messages.GetMessage("no_changes", cfg))
		return
	}

	// Show analyzing message
	messages.PrintInfo(messages.GetMessage("analyzing_changes", cfg))

	// Generate commit message with API key rotation
	commitMessage, err := ai.GenerateCommitMessage(diff, cfg)
	if err != nil {
		messages.PrintError(fmt.Sprintf("%s: %v", messages.GetMessage("review_error", cfg), err))

		// Check if all API keys are exhausted
		remainingKeys := config.GetAllAvailableAPIKeys(cfg)
		if len(remainingKeys) == 0 {
			messages.PrintWarning("⚠️ All API keys are currently inactive.")
			messages.PrintInfo("Run 'dev_tool accounts' to:")
			messages.PrintInfo("  • Add new API keys")
			messages.PrintInfo("  • Reset error counts for existing keys")
			messages.PrintInfo("  • Check API key status")
		}
		return
	}

	// Display generated message
	messages.PrintSection(messages.GetMessage("generated_msg", cfg), "GREEN")
	fmt.Printf("\n%s\n", commitMessage)

	// Confirm commit if enabled
	if cfg.ConfirmBeforeCommit {
		fmt.Printf("\n%s ", messages.GetMessage("proceed_commit", cfg))
		reader := bufio.NewReader(os.Stdin)
		response, _ := reader.ReadString('\n')
		response = strings.TrimSpace(strings.ToLower(response))

		if response != "y" && response != "yes" && response != "có" {
			messages.PrintWarning(messages.GetMessage("commit_cancelled", cfg))
			return
		}
	}

	// Commit changes
	if err := git.CommitChanges(commitMessage, cfg); err != nil {
		messages.PrintError(fmt.Sprintf("%s: %v", messages.GetMessage("git_error", cfg), err))
		return
	}

	messages.PrintSuccess(messages.GetMessage("commit_success", cfg))

	// Push if enabled and not disabled by flag
	if cfg.AutoPush && !noPush {
		messages.PrintInfo("Pushing changes...")
		if err := git.PushChanges(cfg); err != nil {
			messages.PrintError(fmt.Sprintf("%s: %v", messages.GetMessage("git_error", cfg), err))
			return
		}
		messages.PrintSuccess(messages.GetMessage("push_success", cfg))
	}
}

func ShowSettingsMenu(cfg config.Config) {
	ui.ShowSettingsMenu(cfg)
}

// Helper function to count active accounts
func countActiveAccounts(cfg config.Config) int {
	count := 0
	for _, account := range cfg.Accounts {
		if len(account.APIKeys) > 0 {
			count++
		}
	}
	return count
}
