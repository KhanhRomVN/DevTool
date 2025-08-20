// main.go
package main

import (
	"fmt"
	"os"
	"strings"

	"github.com/spf13/cobra"
)

var (
	version = "2.0.0"
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
	}

	rootCmd.AddCommand(
		newAutoCommitCmd(),
		newSettingsCmd(),
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
			config := LoadConfig()
			HandleAutoCommit(noPush, config)
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
			config := LoadConfig()
			ShowSettingsMenu(config)
		},
	}
}

// HandleAutoCommit handles the auto-commit functionality
func HandleAutoCommit(noPush bool, config Config) {
	// Auto stage changes if enabled
	if config.AutoStage {
		if err := StageAllChanges(); err != nil {
			PrintError(GetMessage("git_error", config) + ": " + err.Error())
			os.Exit(1)
		}
	}

	diff, err := GetGitDiff()
	if err != nil {
		PrintError(GetMessage("git_error", config) + ": " + err.Error())
		os.Exit(1)
	}

	if diff == "" {
		PrintError(GetMessage("no_changes", config))
		os.Exit(1)
	}

	// Show diff summary
	PrintSection(GetMessage("analyzing_changes", config))
	linesAdded := strings.Count(diff, "\n+") - strings.Count(diff, "\n+++")
	linesRemoved := strings.Count(diff, "\n-") - strings.Count(diff, "\n---")
	fmt.Printf("📊 %d additions, %d deletions\n", linesAdded, linesRemoved)

	// Get primary account for generation
	var primaryAccount *Account
	for i, account := range config.Accounts {
		if account.IsPrimary {
			primaryAccount = &config.Accounts[i]
			break
		}
	}

	if primaryAccount == nil {
		PrintError("❌ No primary account configured. Please set up an account in settings.")
		os.Exit(1)
	}

	// Generate commit message
	commitMessage, err := GenerateCommitMessage(
		diff,
		primaryAccount.APIKey,
		primaryAccount.Model,
		config.CommitStyle,
		config.CommitLanguage,
	)
	if err != nil {
		PrintError("❌ Error generating commit message: " + err.Error())
		PrintError("💡 Please check your API key and internet connection.")
		os.Exit(1)
	}

	PrintSection(GetMessage("generated_msg", config))
	fmt.Printf("\n%s\n\n", commitMessage)

	// Ask for confirmation if enabled
	if config.ConfirmBeforeCommit {
		for {
			fmt.Print(GetMessage("proceed_commit", config) + " ")
			var proceed string
			fmt.Scanln(&proceed)
			proceed = strings.ToLower(proceed)

			if proceed == "y" || proceed == "yes" || proceed == "có" {
				break
			} else if proceed == "n" || proceed == "no" || proceed == "không" || proceed == "" {
				PrintError(GetMessage("commit_cancelled", config))
				os.Exit(0)
			}
		}
	}

	// Commit changes
	if err := CommitChanges(commitMessage, config); err != nil {
		PrintError(GetMessage("git_error", config) + ": " + err.Error())
		os.Exit(1)
	}

	PrintSuccess(GetMessage("commit_success", config))

	if !noPush && config.AutoPush {
		if err := PushChanges(config); err != nil {
			PrintError(GetMessage("git_error", config) + ": " + err.Error())
			os.Exit(1)
		}
		PrintSuccess(GetMessage("push_success", config))
	}
}

// ResetConfig resets configuration to defaults
func ResetConfig() Config {
	configPath := GetConfigPath()
	if _, err := os.Stat(configPath); err == nil {
		os.Remove(configPath)
	}

	config := CreateInitialConfig()
	PrintSuccess("🔄 Configuration reset successfully!")
	return config
}

// UninstallTool completely removes the tool
func UninstallTool() {
	PrintWarning("⚠️  This will completely remove dev_tool and all its data!")
	fmt.Print("Are you sure you want to uninstall? (yes/no): ")
	var confirm string
	fmt.Scanln(&confirm)
	confirm = strings.ToLower(confirm)

	if confirm != "yes" && confirm != "y" {
		PrintError("Uninstall cancelled.")
		return
	}

	// Remove config directory
	configDir := GetConfigDir()
	if _, err := os.Stat(configDir); err == nil {
		err := os.RemoveAll(configDir)
		if err != nil {
			PrintError("Error during uninstall: " + err.Error())
			return
		}
	}

	PrintSuccess("✅ dev_tool has been uninstalled successfully!")
	fmt.Println("To reinstall, run: go install github.com/your-repo/dev_tool")
}
