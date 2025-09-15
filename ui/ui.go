// ui/ui.go
package ui

import (
	"bufio"
	"dev_tool/config"
	"dev_tool/messages"
	"fmt"
	"os"
	"strconv"
	"strings"

	"github.com/fatih/color"
)

var Colors = map[string]*color.Color{
	"BLUE":      color.New(color.FgBlue),
	"GREEN":     color.New(color.FgGreen),
	"YELLOW":    color.New(color.FgYellow),
	"RED":       color.New(color.FgRed),
	"PURPLE":    color.New(color.FgMagenta),
	"CYAN":      color.New(color.FgCyan),
	"WHITE":     color.New(color.FgWhite),
	"BOLD":      color.New(color.Bold),
	"UNDERLINE": color.New(color.Underline),
	"DIM":       color.New(color.Faint),
	"END":       color.New(color.Reset),
}

func PrintHeader(text string, colorName string) {
	c := Colors[colorName]
	if c == nil {
		c = Colors["CYAN"]
	}

	width := max(len(text)+4, 50)
	border := strings.Repeat("=", width)

	c.Printf("\n%s\n", border)
	c.Printf("%s\n", CenterText(text, width))
	c.Printf("%s\n", border)
}

func PrintSection(text string, colorName string) {
	c := Colors[colorName]
	if c == nil {
		c = Colors["BLUE"]
	}

	c.Printf("\n▶ %s\n", text)
}

func PrintError(text string) {
	Colors["RED"].Add(color.Bold).Printf("❌ %s\n", text)
}

func PrintSuccess(text string) {
	Colors["GREEN"].Add(color.Bold).Printf("✅ %s\n", text)
}

func PrintWarning(text string) {
	Colors["YELLOW"].Add(color.Bold).Printf("⚠️  %s\n", text)
}

func PrintInfo(text string) {
	Colors["CYAN"].Printf("ℹ️  %s\n", text)
}

func CenterText(text string, width int) string {
	padding := (width - len(text)) / 2
	if padding < 0 {
		padding = 0
	}
	return fmt.Sprintf("%*s%s%*s", padding, "", text, padding, "")
}

func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}

// Enhanced ShowCurrentConfig to display account information
func ShowCurrentConfig(cfg config.Config) {
	messages.PrintSection(messages.GetMessage("current_config", cfg), "PURPLE")

	// Count active accounts and API keys
	activeAccounts := 0
	activeAPIKeys := 0
	for _, account := range cfg.Accounts {
		if account.IsActive {
			activeAccounts++
			activeAPIKeys += len(account.GetActiveAPIKeys())
		}
	}

	// Language settings
	uiLangDisplay := messages.GetMessage("lang_1", cfg)
	if cfg.UILanguage == "vi" {
		uiLangDisplay = messages.GetMessage("lang_2", cfg)
	}

	commitLangDisplay := messages.GetMessage("lang_1", cfg)
	if cfg.CommitLanguage == "vi" {
		commitLangDisplay = messages.GetMessage("lang_2", cfg)
	}

	// Commit style display
	styleMap := map[string]string{
		"conventional": "📋 Conventional Commits",
		"emoji":        "😄 Emoji Style",
		"descriptive":  "📝 Descriptive",
	}
	styleDisplay := styleMap[cfg.CommitStyle]

	// Get account info
	primaryAccount := config.GetPrimaryAccount(cfg)
	accountInfo := ""
	if primaryAccount != nil {
		email := primaryAccount.Email
		model := primaryAccount.Model
		accountInfo = fmt.Sprintf("%s📧 Primary Account: %s\n%s🤖 Account Model:   %s\n",
			Colors["YELLOW"].Sprint(""), email, Colors["YELLOW"].Sprint(""), model)
	}

	configDisplay := fmt.Sprintf(`
%s===================================================
%s
%s---------------------------------------------------
%s🌐 %s: %s
%s💬 %s: %s
%s🎨 %s: %s
%s👥 Active Accounts: %d
%s🔑 Available API Keys: %d
%s%s🚀 %s: %s
%s📦 %s: %s
%s===================================================
	`,
		Colors["CYAN"].Sprint(""),
		messages.CenterText(messages.GetMessage("current_config", cfg), 51),
		Colors["CYAN"].Sprint(""),
		Colors["YELLOW"].Sprint(""), messages.GetMessage("ui_lang", cfg), uiLangDisplay,
		Colors["YELLOW"].Sprint(""), messages.GetMessage("commit_lang", cfg), commitLangDisplay,
		Colors["YELLOW"].Sprint(""), messages.GetMessage("commit_style", cfg), styleDisplay,
		Colors["YELLOW"].Sprint(""), activeAccounts,
		Colors["YELLOW"].Sprint(""), activeAPIKeys,
		accountInfo,
		Colors["YELLOW"].Sprint(""), messages.GetMessage("auto_push", cfg), GetStatusDisplay(cfg.AutoPush, cfg),
		Colors["YELLOW"].Sprint(""), messages.GetMessage("auto_stage", cfg), GetStatusDisplay(cfg.AutoStage, cfg),
		Colors["CYAN"].Sprint(""),
	)

	fmt.Print(configDisplay)
}

func GetStatusDisplay(enabled bool, cfg config.Config) string {
	if enabled {
		return fmt.Sprintf("%s✅ %s", Colors["GREEN"].Sprint(""), messages.GetMessage("enabled", cfg))
	}
	return fmt.Sprintf("%s❌ %s", Colors["RED"].Sprint(""), messages.GetMessage("disabled", cfg))
}

func ShowSettingsMenu(cfg config.Config) config.Config {
	for {
		messages.PrintHeader(messages.GetMessage("settings_menu", cfg), "CYAN")
		ShowCurrentConfig(cfg)

		optionsText := fmt.Sprintf(`
%s===================================================
%s
%s---------------------------------------------------
%s1%s │ ⚙️  %s
%s2%s │ 🔄 %s
%s3%s │ 🗑️  %s
%s4%s │ ❓ %s
%s5%s │ 👥 %s
%s0%s │ 🚪 %s
%s===================================================
		`,
			Colors["BLUE"].Sprint(""),
			messages.CenterText(messages.GetMessage("options", cfg), 51),
			Colors["BLUE"].Sprint(""),
			Colors["GREEN"].Sprint(""), Colors["END"].Sprint(""), messages.GetMessage("edit_config", cfg),
			Colors["YELLOW"].Sprint(""), Colors["END"].Sprint(""), messages.GetMessage("reset_defaults", cfg),
			Colors["RED"].Sprint(""), Colors["END"].Sprint(""), messages.GetMessage("uninstall_tool", cfg),
			Colors["CYAN"].Sprint(""), Colors["END"].Sprint(""), messages.GetMessage("help_info", cfg),
			Colors["PURPLE"].Sprint(""), Colors["END"].Sprint(""), messages.GetMessage("account_manager", cfg),
			Colors["WHITE"].Sprint(""), Colors["END"].Sprint(""), messages.GetMessage("exit", cfg),
			Colors["BLUE"].Sprint(""),
		)
		fmt.Println(optionsText)

		fmt.Printf("\n%s🎯 %s (0-5): %s", Colors["BOLD"].Sprint(""), messages.GetMessage("select_option", cfg), Colors["END"].Sprint(""))

		reader := bufio.NewReader(os.Stdin)
		choice, _ := reader.ReadString('\n')
		choice = strings.TrimSpace(choice)

		switch choice {
		case "1":
			cfg = ShowConfigurationInterface(cfg)
			config.SaveConfig(cfg)
		case "2":
			if ConfirmAction(messages.GetMessage("reset_confirm", cfg), cfg) {
				cfg = config.ResetConfig()
			}
		case "3":
			if ConfirmAction(messages.GetMessage("uninstall_confirm", cfg), cfg) {
				// UninstallTool() will handle exit, so this should not return
				config.UninstallTool()
				// This line should never be reached due to os.Exit(0) in UninstallTool()
				return cfg
			}
		case "4":
			ShowHelp(cfg)
		case "5":
			cfg = ShowAccountManager(cfg)
		case "0":
			messages.PrintSuccess("👋 " + messages.GetMessage("exit", cfg))
			return cfg
		default:
			messages.PrintError(messages.GetMessage("invalid_option", cfg))
		}
	}
}

// Show Account Manager Menu
func ShowAccountManager(cfg config.Config) config.Config {
	for {
		messages.PrintHeader(messages.GetMessage("account_manager", cfg), "CYAN")
		ShowAccountList(cfg)

		optionsText := fmt.Sprintf(`
%s===================================================
%s
%s---------------------------------------------------
%s1%s │ ➕ %s
%s2%s │ ✏️  %s
%s3%s │ 🗑️  %s
%s4%s │ ⭐ %s
%s5%s │ 🔑 %s
%s0%s │ ⬅️  %s
%s===================================================
		`,
			Colors["BLUE"].Sprint(""),
			messages.CenterText(messages.GetMessage("options", cfg), 51),
			Colors["BLUE"].Sprint(""),
			Colors["GREEN"].Sprint(""), Colors["END"].Sprint(""), messages.GetMessage("add_account", cfg),
			Colors["YELLOW"].Sprint(""), Colors["END"].Sprint(""), messages.GetMessage("edit_account", cfg),
			Colors["RED"].Sprint(""), Colors["END"].Sprint(""), messages.GetMessage("delete_account", cfg),
			Colors["PURPLE"].Sprint(""), Colors["END"].Sprint(""), messages.GetMessage("set_primary", cfg),
			Colors["CYAN"].Sprint(""), Colors["END"].Sprint(""), messages.GetMessage("manage_api_keys", cfg),
			Colors["WHITE"].Sprint(""), Colors["END"].Sprint(""), messages.GetMessage("back_to_menu", cfg),
			Colors["BLUE"].Sprint(""),
		)
		fmt.Println(optionsText)

		fmt.Printf("\n%s🎯 %s (0-5): %s", Colors["BOLD"].Sprint(""), messages.GetMessage("select_option", cfg), Colors["END"].Sprint(""))

		reader := bufio.NewReader(os.Stdin)
		choice, _ := reader.ReadString('\n')
		choice = strings.TrimSpace(choice)

		switch choice {
		case "1":
			cfg = AddNewAccount(cfg)
		case "2":
			cfg = EditAccount(cfg)
		case "3":
			cfg = DeleteAccount(cfg)
		case "4":
			cfg = SetPrimaryAccount(cfg)
		case "5":
			cfg = ManageAPIKeys(cfg)
		case "0":
			return cfg
		default:
			messages.PrintError(messages.GetMessage("invalid_option", cfg))
		}

		if choice != "0" {
			config.SaveConfig(cfg)
		}
	}
}

// Show Account List with details
func ShowAccountList(cfg config.Config) {
	messages.PrintSection(messages.GetMessage("account_list", cfg), "PURPLE")

	if len(cfg.Accounts) == 0 {
		fmt.Printf("%s📭 %s\n", Colors["YELLOW"].Sprint(""), messages.GetMessage("no_accounts", cfg))
		return
	}

	for i, account := range cfg.Accounts {
		statusIcon := "🔑"
		statusText := messages.GetMessage("secondary", cfg)
		if account.IsPrimary {
			statusIcon = "⭐"
			statusText = messages.GetMessage("primary", cfg)
		}

		activeIcon := "✅"
		if !account.IsActive {
			activeIcon = "❌"
		}

		// Count active API keys
		activeKeys := len(account.GetActiveAPIKeys())
		totalKeys := len(account.APIKeys)

		accountInfo := fmt.Sprintf(`
%s---------------------------------------------------
%s%d. %s📧 %s: %s
%s   🤖 %s: %s
%s   %s %s: %s %s
%s   🔑 API Keys: %d/%d active
%s   📅 Created: %s
		`,
			Colors["DIM"].Sprint(""),
			Colors["BOLD"].Sprint(""), i+1, statusIcon, messages.GetMessage("account_email", cfg), account.Email,
			Colors["YELLOW"].Sprint(""), messages.GetMessage("account_model", cfg), account.Model,
			Colors["YELLOW"].Sprint(""), statusIcon, messages.GetMessage("account_status", cfg), statusText, activeIcon,
			Colors["YELLOW"].Sprint(""), activeKeys, totalKeys,
			Colors["DIM"].Sprint(""), account.CreatedAt.Format("2006-01-02 15:04"),
		)

		fmt.Print(accountInfo)

		// Show API key details if any
		if totalKeys > 0 {
			fmt.Printf("%s   🔑 API Keys:\n", Colors["CYAN"].Sprint(""))
			for j, apiKey := range account.APIKeys {
				maskedKey := maskAPIKey(apiKey.Key)

				fmt.Printf("%s      %d. %s (%s)\n",
					Colors["DIM"].Sprint(""),
					j+1,
					apiKey.Description,
					maskedKey)
			}
		}
	}
	fmt.Printf("%s---------------------------------------------------\n", Colors["DIM"].Sprint(""))
}

// Add New Account
func AddNewAccount(cfg config.Config) config.Config {
	messages.PrintSection("➕ "+messages.GetMessage("add_account", cfg), "GREEN")

	var email, apiKey, description string

	// Get email
	for {
		fmt.Printf("\n%s📧 %s: %s", Colors["BOLD"].Sprint(""), messages.GetMessage("account_email", cfg), Colors["END"].Sprint(""))
		reader := bufio.NewReader(os.Stdin)
		email, _ = reader.ReadString('\n')
		email = strings.TrimSpace(email)

		if email == "" {
			messages.PrintError(messages.GetMessage("email_required", cfg))
			continue
		}

		// Check if email already exists
		if cfg.FindAccount(email) != nil {
			messages.PrintError(messages.GetMessage("email_exists", cfg))
			continue
		}

		break
	}

	// Get API key
	for {
		fmt.Printf("%s🔑 %s: %s", Colors["BOLD"].Sprint(""), messages.GetMessage("enter_api_key_prompt", cfg), Colors["END"].Sprint(""))
		reader := bufio.NewReader(os.Stdin)
		apiKey, _ = reader.ReadString('\n')
		apiKey = strings.TrimSpace(apiKey)

		if apiKey == "" {
			messages.PrintError(messages.GetMessage("api_key_required", cfg))
			continue
		}
		break
	}

	// Get description
	fmt.Printf("%s📝 API Key Description [Primary API Key]: %s", Colors["BOLD"].Sprint(""), Colors["END"].Sprint(""))
	reader := bufio.NewReader(os.Stdin)
	description, _ = reader.ReadString('\n')
	description = strings.TrimSpace(description)
	if description == "" {
		description = "Primary API Key"
	}

	// Choose model
	fmt.Println("\n🤖 " + messages.GetMessage("choose_model", cfg))
	for i, model := range config.GeminiModels {
		fmt.Printf("%d️⃣  %s\n", i+1, model)
	}

	var modelChoice int
	for {
		fmt.Printf("\n%s🤖 %s (1-%d): %s", Colors["BOLD"].Sprint(""), messages.GetMessage("select_model", cfg), len(config.GeminiModels), Colors["END"].Sprint(""))
		_, err := fmt.Scan(&modelChoice)
		if err == nil && modelChoice >= 1 && modelChoice <= len(config.GeminiModels) {
			break
		}
		messages.PrintError(messages.GetMessage("invalid_choice", cfg))
	}

	selectedModel := config.GeminiModels[modelChoice-1]

	// Ask if primary (only if no primary exists)
	isPrimary := false
	primaryExists := false
	for _, acc := range cfg.Accounts {
		if acc.IsPrimary {
			primaryExists = true
			break
		}
	}

	if !primaryExists {
		isPrimary = true
		messages.PrintInfo(messages.GetMessage("first_account_primary", cfg))
	} else {
		fmt.Printf("\n%s⭐ %s? (y/N): %s", Colors["BOLD"].Sprint(""), messages.GetMessage("set_as_primary", cfg), Colors["END"].Sprint(""))
		reader := bufio.NewReader(os.Stdin)
		response, _ := reader.ReadString('\n')
		response = strings.TrimSpace(strings.ToLower(response))
		isPrimary = (response == "y" || response == "yes" || response == "có")
	}

	// Add account
	cfg.AddAccount(email, apiKey, selectedModel, description, isPrimary)

	messages.PrintSuccess(fmt.Sprintf("✅ %s: %s", messages.GetMessage("account_added", cfg), email))
	return cfg
}

// Edit Account
func EditAccount(cfg config.Config) config.Config {
	if len(cfg.Accounts) == 0 {
		messages.PrintWarning(messages.GetMessage("no_accounts", cfg))
		return cfg
	}

	messages.PrintSection("✏️ "+messages.GetMessage("edit_account", cfg), "YELLOW")
	ShowAccountList(cfg)

	fmt.Printf("\n%s📧 %s (1-%d): %s", Colors["BOLD"].Sprint(""), messages.GetMessage("select_account", cfg), len(cfg.Accounts), Colors["END"].Sprint(""))

	reader := bufio.NewReader(os.Stdin)
	choice, _ := reader.ReadString('\n')
	choice = strings.TrimSpace(choice)

	accountIndex, err := strconv.Atoi(choice)
	if err != nil || accountIndex < 1 || accountIndex > len(cfg.Accounts) {
		messages.PrintError(messages.GetMessage("invalid_choice", cfg))
		return cfg
	}

	account := &cfg.Accounts[accountIndex-1]

	// Edit account menu
	for {
		fmt.Printf(`
%s===== Edit Account: %s =====
1️⃣  Change Model (Current: %s)
2️⃣  Toggle Active Status (Current: %s)
3️⃣  Set as Primary
0️⃣  Back
		`,
			Colors["CYAN"].Sprint(""),
			account.Email,
			account.Model,
			GetStatusDisplay(account.IsActive, cfg))

		fmt.Printf("\n%s🎯 %s (0-3): %s", Colors["BOLD"].Sprint(""), messages.GetMessage("select_option", cfg), Colors["END"].Sprint(""))

		editChoice, _ := reader.ReadString('\n')
		editChoice = strings.TrimSpace(editChoice)

		switch editChoice {
		case "1":
			// Change model
			fmt.Println("\n🤖 " + messages.GetMessage("available_models", cfg))
			for i, model := range config.GeminiModels {
				indicator := ""
				if model == account.Model {
					indicator = " (current)"
				}
				fmt.Printf("%d️⃣  %s%s\n", i+1, model, indicator)
			}

			var modelChoice int
			fmt.Printf("\n%s🤖 %s (1-%d): %s", Colors["BOLD"].Sprint(""), messages.GetMessage("select_model", cfg), len(config.GeminiModels), Colors["END"].Sprint(""))
			_, err := fmt.Scan(&modelChoice)
			if err == nil && modelChoice >= 1 && modelChoice <= len(config.GeminiModels) {
				account.Model = config.GeminiModels[modelChoice-1]
				messages.PrintSuccess(fmt.Sprintf("✅ Model updated to: %s", account.Model))
			} else {
				messages.PrintError(messages.GetMessage("invalid_choice", cfg))
			}

		case "2":
			// Toggle active status
			account.IsActive = !account.IsActive
			status := messages.GetMessage("activated", cfg)
			if !account.IsActive {
				status = messages.GetMessage("deactivated", cfg)
			}
			messages.PrintSuccess(fmt.Sprintf("✅ Account %s: %s", status, account.Email))

		case "3":
			// Set as primary
			if account.IsPrimary {
				messages.PrintInfo(messages.GetMessage("already_primary", cfg))
			} else {
				// Unset other primary accounts
				for i := range cfg.Accounts {
					cfg.Accounts[i].IsPrimary = false
				}
				account.IsPrimary = true
				messages.PrintSuccess(fmt.Sprintf("✅ %s set as primary account", account.Email))
			}

		case "0":
			return cfg

		default:
			messages.PrintError(messages.GetMessage("invalid_option", cfg))
		}
	}
}

// Delete Account
func DeleteAccount(cfg config.Config) config.Config {
	if len(cfg.Accounts) == 0 {
		messages.PrintWarning(messages.GetMessage("no_accounts", cfg))
		return cfg
	}

	messages.PrintSection("🗑️ "+messages.GetMessage("delete_account", cfg), "RED")
	ShowAccountList(cfg)

	fmt.Printf("\n%s📧 %s (1-%d): %s", Colors["BOLD"].Sprint(""), messages.GetMessage("select_account", cfg), len(cfg.Accounts), Colors["END"].Sprint(""))

	reader := bufio.NewReader(os.Stdin)
	choice, _ := reader.ReadString('\n')
	choice = strings.TrimSpace(choice)

	accountIndex, err := strconv.Atoi(choice)
	if err != nil || accountIndex < 1 || accountIndex > len(cfg.Accounts) {
		messages.PrintError(messages.GetMessage("invalid_choice", cfg))
		return cfg
	}

	account := cfg.Accounts[accountIndex-1]

	// Confirmation
	fmt.Printf("\n%s⚠️ %s: %s? %s",
		Colors["RED"].Sprint(""),
		messages.GetMessage("confirm_delete_account", cfg),
		account.Email,
		messages.GetMessage("type_yes_confirm", cfg))

	confirm, _ := reader.ReadString('\n')
	confirm = strings.TrimSpace(strings.ToLower(confirm))

	if confirm == "yes" {
		cfg.RemoveAccount(account.Email)
		messages.PrintSuccess(fmt.Sprintf("✅ %s: %s", messages.GetMessage("account_deleted", cfg), account.Email))

		// If deleted account was primary, set another as primary
		if account.IsPrimary && len(cfg.Accounts) > 0 {
			cfg.Accounts[0].IsPrimary = true
			messages.PrintInfo(fmt.Sprintf("ℹ️ %s set as new primary account", cfg.Accounts[0].Email))
		}
	} else {
		messages.PrintInfo(messages.GetMessage("deletion_cancelled", cfg))
	}

	return cfg
}

// Set Primary Account
func SetPrimaryAccount(cfg config.Config) config.Config {
	if len(cfg.Accounts) == 0 {
		messages.PrintWarning(messages.GetMessage("no_accounts", cfg))
		return cfg
	}

	messages.PrintSection("⭐ "+messages.GetMessage("set_primary", cfg), "PURPLE")
	ShowAccountList(cfg)

	fmt.Printf("\n%s📧 %s (1-%d): %s", Colors["BOLD"].Sprint(""), messages.GetMessage("select_account", cfg), len(cfg.Accounts), Colors["END"].Sprint(""))

	reader := bufio.NewReader(os.Stdin)
	choice, _ := reader.ReadString('\n')
	choice = strings.TrimSpace(choice)

	accountIndex, err := strconv.Atoi(choice)
	if err != nil || accountIndex < 1 || accountIndex > len(cfg.Accounts) {
		messages.PrintError(messages.GetMessage("invalid_choice", cfg))
		return cfg
	}

	// Set new primary
	for i := range cfg.Accounts {
		cfg.Accounts[i].IsPrimary = (i == accountIndex-1)
	}

	messages.PrintSuccess(fmt.Sprintf("✅ %s set as primary account", cfg.Accounts[accountIndex-1].Email))
	return cfg
}

// Manage API Keys for selected account
func ManageAPIKeys(cfg config.Config) config.Config {
	if len(cfg.Accounts) == 0 {
		messages.PrintWarning(messages.GetMessage("no_accounts", cfg))
		return cfg
	}

	messages.PrintSection("🔑 "+messages.GetMessage("manage_api_keys", cfg), "CYAN")
	ShowAccountList(cfg)

	fmt.Printf("\n%s📧 %s (1-%d): %s", Colors["BOLD"].Sprint(""), messages.GetMessage("select_account", cfg), len(cfg.Accounts), Colors["END"].Sprint(""))

	reader := bufio.NewReader(os.Stdin)
	choice, _ := reader.ReadString('\n')
	choice = strings.TrimSpace(choice)

	accountIndex, err := strconv.Atoi(choice)
	if err != nil || accountIndex < 1 || accountIndex > len(cfg.Accounts) {
		messages.PrintError(messages.GetMessage("invalid_choice", cfg))
		return cfg
	}

	account := &cfg.Accounts[accountIndex-1]
	cfg = ManageAccountAPIKeys(cfg, account)
	return cfg
}

// Manage API Keys for specific account
func ManageAccountAPIKeys(cfg config.Config, account *config.Account) config.Config {
	for {
		messages.PrintHeader(fmt.Sprintf("🔑 API Keys for %s", account.Email), "CYAN")
		ShowAPIKeyList(*account)

		optionsText := fmt.Sprintf(`
%s===================================================
%s
%s---------------------------------------------------
%s1%s │ ➕ %s
%s2%s │ ✏️  %s
%s3%s │ 🗑️  %s
%s0%s │ ⬅️  %s
%s===================================================
		`,
			Colors["BLUE"].Sprint(""),
			messages.CenterText(messages.GetMessage("api_key_options", cfg), 51),
			Colors["BLUE"].Sprint(""),
			Colors["GREEN"].Sprint(""), Colors["END"].Sprint(""), messages.GetMessage("add_api_key", cfg),
			Colors["YELLOW"].Sprint(""), Colors["END"].Sprint(""), messages.GetMessage("edit_api_key", cfg),
			Colors["RED"].Sprint(""), Colors["END"].Sprint(""), messages.GetMessage("delete_api_key", cfg),
			Colors["WHITE"].Sprint(""), Colors["END"].Sprint(""), messages.GetMessage("back_to_menu", cfg),
			Colors["BLUE"].Sprint(""),
		)
		fmt.Println(optionsText)

		fmt.Printf("\n%s🎯 %s (0-3): %s", Colors["BOLD"].Sprint(""), messages.GetMessage("select_option", cfg), Colors["END"].Sprint(""))

		reader := bufio.NewReader(os.Stdin)
		choice, _ := reader.ReadString('\n')
		choice = strings.TrimSpace(choice)

		switch choice {
		case "1":
			account = AddAPIKey(account)
		case "2":
			account = EditAPIKey(account)
		case "3":
			account = DeleteAPIKey(account)
		case "0":
			return cfg
		default:
			messages.PrintError(messages.GetMessage("invalid_option", cfg))
		}

		if choice != "0" {
			config.SaveConfig(cfg)
		}
	}
}

// Helper function to mask API key
func maskAPIKey(apiKey string) string {
	if len(apiKey) <= 8 {
		return strings.Repeat("*", len(apiKey))
	}
	return apiKey[:4] + strings.Repeat("*", len(apiKey)-8) + apiKey[len(apiKey)-4:]
}

// Show API Key List for account
func ShowAPIKeyList(account config.Account) {
	if len(account.APIKeys) == 0 {
		fmt.Printf("%s📭 No API keys found for this account\n", Colors["YELLOW"].Sprint(""))
		return
	}

	for i, apiKey := range account.APIKeys {
		maskedKey := maskAPIKey(apiKey.Key)

		fmt.Printf(`
%s---------------------------------------------------
%s%d. 🔑 %s (%s)
%s   📝 Description: %s
%s   📅 Created: %s
		`,
			Colors["DIM"].Sprint(""),
			Colors["BOLD"].Sprint(""), i+1, maskedKey, apiKey.Description,
			Colors["YELLOW"].Sprint(""), apiKey.Description,
			Colors["DIM"].Sprint(""), apiKey.CreatedAt.Format("2006-01-02 15:04"),
		)
	}
	fmt.Printf("%s---------------------------------------------------\n", Colors["DIM"].Sprint(""))
}

// Add API Key to account
func AddAPIKey(account *config.Account) *config.Account {
	messages.PrintSection("➕ Add API Key", "GREEN")

	var apiKey, description string

	// Get API key
	for {
		fmt.Printf("\n%s🔑 Enter new API Key: %s", Colors["BOLD"].Sprint(""), Colors["END"].Sprint(""))
		reader := bufio.NewReader(os.Stdin)
		apiKey, _ = reader.ReadString('\n')
		apiKey = strings.TrimSpace(apiKey)

		if apiKey == "" {
			messages.PrintError("API key is required")
			continue
		}
		break
	}

	// Get description
	fmt.Printf("%s📝 API Key Description: %s", Colors["BOLD"].Sprint(""), Colors["END"].Sprint(""))
	reader := bufio.NewReader(os.Stdin)
	description, _ = reader.ReadString('\n')
	description = strings.TrimSpace(description)
	if description == "" {
		description = "Additional API Key"
	}

	// Add API key
	account.AddAPIKey(apiKey, description)
	messages.PrintSuccess("✅ API key added successfully")

	return account
}

// Edit API Key
func EditAPIKey(account *config.Account) *config.Account {
	if len(account.APIKeys) == 0 {
		messages.PrintWarning("No API keys found for this account")
		return account
	}

	messages.PrintSection("✏️ Edit API Key", "YELLOW")
	ShowAPIKeyList(*account)

	fmt.Printf("\n%s🔑 Select API Key to edit (1-%d): %s", Colors["BOLD"].Sprint(""), len(account.APIKeys), Colors["END"].Sprint(""))

	reader := bufio.NewReader(os.Stdin)
	choice, _ := reader.ReadString('\n')
	choice = strings.TrimSpace(choice)

	keyIndex, err := strconv.Atoi(choice)
	if err != nil || keyIndex < 1 || keyIndex > len(account.APIKeys) {
		messages.PrintError("Invalid choice")
		return account
	}

	apiKey := &account.APIKeys[keyIndex-1]

	// Edit API key menu - only allow changing description
	fmt.Printf(`
%s===== Edit API Key: %s =====
1️⃣  Change Description (Current: %s)
0️⃣  Back
		`,
		Colors["CYAN"].Sprint(""),
		maskAPIKey(apiKey.Key),
		apiKey.Description)

	fmt.Printf("\n%s🎯 Select option (0-1): %s", Colors["BOLD"].Sprint(""), Colors["END"].Sprint(""))

	editChoice, _ := reader.ReadString('\n')
	editChoice = strings.TrimSpace(editChoice)

	switch editChoice {
	case "1":
		// Change description
		fmt.Printf("\n%s📝 New Description: %s", Colors["BOLD"].Sprint(""), Colors["END"].Sprint(""))
		newDesc, _ := reader.ReadString('\n')
		newDesc = strings.TrimSpace(newDesc)
		if newDesc != "" {
			apiKey.Description = newDesc
			messages.PrintSuccess("✅ Description updated")
		}
	case "0":
		// Back
	default:
		messages.PrintError("Invalid option")
	}

	return account
}

// Delete API Key
func DeleteAPIKey(account *config.Account) *config.Account {
	if len(account.APIKeys) == 0 {
		messages.PrintWarning("No API keys found for this account")
		return account
	}

	messages.PrintSection("🗑️ Delete API Key", "RED")
	ShowAPIKeyList(*account)

	fmt.Printf("\n%s🔑 Select API Key to delete (1-%d): %s", Colors["BOLD"].Sprint(""), len(account.APIKeys), Colors["END"].Sprint(""))

	reader := bufio.NewReader(os.Stdin)
	choice, _ := reader.ReadString('\n')
	choice = strings.TrimSpace(choice)

	keyIndex, err := strconv.Atoi(choice)
	if err != nil || keyIndex < 1 || keyIndex > len(account.APIKeys) {
		messages.PrintError("Invalid choice")
		return account
	}

	apiKey := account.APIKeys[keyIndex-1]

	// Confirmation
	fmt.Printf("\n%s⚠️ Confirm delete API Key: %s? Type 'yes' to confirm: %s",
		Colors["RED"].Sprint(""),
		maskAPIKey(apiKey.Key),
		Colors["END"].Sprint(""))

	confirm, _ := reader.ReadString('\n')
	confirm = strings.TrimSpace(strings.ToLower(confirm))

	if confirm == "yes" {
		account.RemoveAPIKey(apiKey.Key)
		messages.PrintSuccess("✅ API key deleted successfully")
	} else {
		messages.PrintInfo("Deletion cancelled")
	}

	return account
}

func changeUILanguage(cfg config.Config, reader *bufio.Reader) config.Config {
	fmt.Println("\n" + messages.GetMessage("available_langs", cfg))
	fmt.Println("1. " + messages.GetMessage("lang_1", cfg))
	fmt.Println("2. " + messages.GetMessage("lang_2", cfg))

	fmt.Print("\n" + messages.GetMessage("select_lang", cfg) + " (1-2): ")
	langChoice, _ := reader.ReadString('\n')
	langChoice = strings.TrimSpace(langChoice)

	switch langChoice {
	case "1":
		cfg.UILanguage = "en"
	case "2":
		cfg.UILanguage = "vi"
	default:
		messages.PrintError(messages.GetMessage("invalid_choice", cfg))
		return cfg
	}

	messages.PrintSuccess(fmt.Sprintf("UI Language changed to %s", cfg.UILanguage))
	return cfg
}

func changeCommitLanguage(cfg config.Config, reader *bufio.Reader) config.Config {
	fmt.Println("\n" + messages.GetMessage("available_langs", cfg))
	fmt.Println("1. " + messages.GetMessage("lang_1", cfg))
	fmt.Println("2. " + messages.GetMessage("lang_2", cfg))

	fmt.Print("\n" + messages.GetMessage("select_lang", cfg) + " (1-2): ")
	langChoice, _ := reader.ReadString('\n')
	langChoice = strings.TrimSpace(langChoice)

	switch langChoice {
	case "1":
		cfg.CommitLanguage = "en"
	case "2":
		cfg.CommitLanguage = "vi"
	default:
		messages.PrintError(messages.GetMessage("invalid_choice", cfg))
		return cfg
	}

	messages.PrintSuccess(fmt.Sprintf("Commit Language changed to %s", cfg.CommitLanguage))
	return cfg
}

func changeCommitStyle(cfg config.Config, reader *bufio.Reader) config.Config {
	fmt.Println("\n" + messages.GetMessage("available_styles", cfg))
	fmt.Println("1. Conventional Commits")
	fmt.Println("2. Emoji Style")
	fmt.Println("3. Descriptive")

	fmt.Print("\n" + messages.GetMessage("select_style", cfg) + " (1-3): ")
	styleChoice, _ := reader.ReadString('\n')
	styleChoice = strings.TrimSpace(styleChoice)

	styles := map[string]string{
		"1": "conventional",
		"2": "emoji",
		"3": "descriptive",
	}

	if newStyle, ok := styles[styleChoice]; ok {
		cfg.CommitStyle = newStyle
		messages.PrintSuccess(fmt.Sprintf("Commit style changed to: %s", newStyle))
	} else {
		messages.PrintError(messages.GetMessage("invalid_choice", cfg))
	}

	return cfg
}

func ShowConfigurationInterface(cfg config.Config) config.Config {
	reader := bufio.NewReader(os.Stdin)

	for {
		messages.PrintHeader("⚙️  "+messages.GetMessage("edit_config", cfg), "CYAN")

		options := []string{
			"1. " + messages.GetMessage("change_ui_lang", cfg),
			"2. " + messages.GetMessage("change_commit_lang", cfg),
			"3. " + messages.GetMessage("change_ai_model", cfg),
			"4. " + messages.GetMessage("change_commit_style", cfg),
			"5. " + messages.GetMessage("toggle_auto_push", cfg),
			"6. " + messages.GetMessage("toggle_auto_stage", cfg),
			"0. " + messages.GetMessage("back_to_menu", cfg),
		}

		for _, option := range options {
			fmt.Println(option)
		}

		fmt.Print("\n" + messages.GetMessage("select_option", cfg) + " (0-6): ")
		choice, _ := reader.ReadString('\n')
		choice = strings.TrimSpace(choice)

		switch choice {
		case "1":
			cfg = changeUILanguage(cfg, reader)
		case "2":
			cfg = changeCommitLanguage(cfg, reader)
		case "3":
			cfg = changeAIModel(cfg, reader)
		case "4":
			cfg = changeCommitStyle(cfg, reader)
		case "5":
			cfg.AutoPush = !cfg.AutoPush
			status := messages.GetMessage("disabled", cfg)
			if cfg.AutoPush {
				status = messages.GetMessage("enabled", cfg)
			}
			messages.PrintSuccess(fmt.Sprintf("Auto Push %s", status))
		case "6":
			cfg.AutoStage = !cfg.AutoStage
			status := messages.GetMessage("disabled", cfg)
			if cfg.AutoStage {
				status = messages.GetMessage("enabled", cfg)
			}
			messages.PrintSuccess(fmt.Sprintf("Auto Stage %s", status))
		case "0":
			return cfg
		default:
			messages.PrintError(messages.GetMessage("invalid_option", cfg))
		}

		fmt.Println("\n" + messages.GetMessage("press_enter_continue", cfg))
		reader.ReadString('\n')
	}
}

func changeAIModel(cfg config.Config, reader *bufio.Reader) config.Config {
	// Get primary account
	primaryAccount := config.GetPrimaryAccountWithFallback(cfg)
	if primaryAccount == nil {
		messages.PrintError(messages.GetMessage("no_accounts", cfg))
		return cfg
	}

	fmt.Println("\n" + messages.GetMessage("available_models", cfg))
	for i, model := range config.GeminiModels {
		currentIndicator := ""
		if model == primaryAccount.Model {
			currentIndicator = " (" + messages.GetMessage("current", cfg) + ")"
		}
		fmt.Printf("%d. %s%s\n", i+1, model, currentIndicator)
	}

	var modelChoice int
	for {
		fmt.Printf("\n%s%s (1-%d): %s", Colors["BOLD"].Sprint(), messages.GetMessage("select_model", cfg), len(config.GeminiModels), Colors["END"].Sprint())
		input, _ := reader.ReadString('\n')
		input = strings.TrimSpace(input)
		choice, err := strconv.Atoi(input)
		if err == nil && choice >= 1 && choice <= len(config.GeminiModels) {
			modelChoice = choice
			break
		}
		messages.PrintError(messages.GetMessage("invalid_choice", cfg))
	}

	selectedModel := config.GeminiModels[modelChoice-1]

	// Update the primary account's model
	for i := range cfg.Accounts {
		if cfg.Accounts[i].Email == primaryAccount.Email {
			cfg.Accounts[i].Model = selectedModel
			break
		}
	}

	messages.PrintSuccess(fmt.Sprintf("Model updated to: %s", selectedModel))
	return cfg
}

// ConfirmAction prompts for user confirmation
func ConfirmAction(message string, cfg config.Config) bool {
	fmt.Printf("%s (y/N): ", message)
	reader := bufio.NewReader(os.Stdin)
	response, _ := reader.ReadString('\n')
	response = strings.TrimSpace(strings.ToLower(response))
	return response == "y" || response == "yes"
}

// ShowHelp displays help information
func ShowHelp(cfg config.Config) {
	messages.PrintHeader("📖 Help & Information", "CYAN")
	fmt.Println(messages.GetMessage("help_text", cfg))
	fmt.Println("\nPress Enter to continue...")
	bufio.NewReader(os.Stdin).ReadString('\n')
}
