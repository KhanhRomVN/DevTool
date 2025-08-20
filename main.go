// main.go
package main

import (
	"fmt"
	"os"

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
