// handlers.go
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
)

func HandleAutoCommit(noPush bool, cfg config.Config) {
	// Auto stage changes if enabled
	if cfg.AutoStage {
		if err := git.StageAllChanges(); err != nil {
			messages.PrintError(messages.GetMessage("git_error", cfg) + ": " + err.Error())
			os.Exit(1)
		}
	}

	diff, err := git.GetGitDiff()
	if err != nil {
		messages.PrintError(err.Error())
		os.Exit(1)
	}

	if diff == "" {
		messages.PrintError(messages.GetMessage("no_changes", cfg))
		os.Exit(1)
	}

	// Show diff summary
	messages.PrintSection(messages.GetMessage("analyzing_changes", cfg), "BLUE")
	linesAdded := strings.Count(diff, "\n+") - strings.Count(diff, "\n+++")
	linesRemoved := strings.Count(diff, "\n-") - strings.Count(diff, "\n---")
	fmt.Printf("📊 %d additions, %d deletions\n", linesAdded, linesRemoved)

	// Get primary account for generation
	primaryAccount := config.GetPrimaryAccount(cfg)
	if primaryAccount == nil {
		messages.PrintError("❌ No primary account configured. Please set up an account in settings.")
		os.Exit(1)
	}

	// Generate commit message
	commitMessage, err := ai.GenerateCommitMessage(
		diff,
		primaryAccount.APIKey,
		primaryAccount.Model,
		cfg.CommitStyle,
		cfg.CommitLanguage,
	)
	if err != nil {
		messages.PrintError(fmt.Sprintf("❌ Error generating commit message: %v", err))
		messages.PrintError("💡 Please check your API key and internet connection.")
		os.Exit(1)
	}

	messages.PrintSection(messages.GetMessage("generated_msg", cfg), "BLUE")
	fmt.Printf("\n%s\n\n", commitMessage)

	// Ask for confirmation if enabled
	if cfg.ConfirmBeforeCommit {
		fmt.Printf("%s ", messages.GetMessage("proceed_commit", cfg))

		reader := bufio.NewReader(os.Stdin)
		proceed, _ := reader.ReadString('\n')
		proceed = strings.TrimSpace(strings.ToLower(proceed))

		if proceed != "y" && proceed != "yes" && proceed != "có" {
			messages.PrintError(messages.GetMessage("commit_cancelled", cfg))
			os.Exit(0)
		}
	}

	// Commit changes
	if err := git.CommitChanges(commitMessage, cfg); err != nil {
		messages.PrintError(fmt.Sprintf("%s: %v", messages.GetMessage("git_error", cfg), err))
		os.Exit(1)
	}

	messages.PrintSuccess(messages.GetMessage("commit_success", cfg))

	// Push changes if enabled
	if !noPush && cfg.AutoPush {
		if err := git.PushChanges(cfg); err != nil {
			messages.PrintError(fmt.Sprintf("%s: %v", messages.GetMessage("git_error", cfg), err))
			os.Exit(1)
		}
		messages.PrintSuccess(messages.GetMessage("push_success", cfg))
	}
}

func ShowSettingsMenu(config config.Config) {
	// This will use the UI package to show the settings menu
	ui.ShowSettingsMenu(config)
}
