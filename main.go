// main.go
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
	version = "2.0.4"
)

func main() {
	var rootCmd = &cobra.Command{
		Use:   "dev_tool",
		Short: "Dev Tool - AI-powered Git Commit Message Generator",
		Long: `🛠️  Dev Tool - AI-powered Git Commit Message Generator

Features:
- AI-powered commit message generation
- Multi-language support (English/Vietnamese)
- Multiple commit styles
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
		newDotCmd(), // Add the explicit dot command
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
		Long: `Quick commit with AI-generated message.

This is a shortcut for the auto-commit command, allowing you to simply run:
  dev_tool .

Instead of:
  dev_tool auto-commit`,
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
		Run: func(cmd *cobra.Command, args []string) {
			cfg := config.LoadConfig()
			ShowSettingsMenu(cfg)
		},
	}
}

func HandleAutoCommit(noPush bool, cfg config.Config) {
	// Check if we have a primary account configured
	primaryAccount := config.GetPrimaryAccount(cfg)
	if primaryAccount == nil || primaryAccount.APIKey == "" {
		messages.PrintError(messages.GetMessage("no_accounts", cfg))
		return
	}

	// Auto-stage if enabled
	if cfg.AutoStage {
		messages.PrintInfo("Auto-staging changes...")
		if err := git.StageAllChanges(); err != nil {
			messages.PrintError(fmt.Sprintf("%s: %v", messages.GetMessage("git_error", cfg), err))
			return
		}
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

	// Generate commit message
	commitMessage, err := ai.GenerateCommitMessage(
		diff,
		primaryAccount.APIKey,
		primaryAccount.Model,
		cfg.CommitStyle,
		cfg.CommitLanguage,
	)
	if err != nil {
		messages.PrintError(fmt.Sprintf("%s: %v", messages.GetMessage("review_error", cfg), err))
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
