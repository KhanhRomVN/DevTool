// ui/ui.go
package ui

import (
	"bufio"
	"dev_tool/config"
	"dev_tool/messages"
	"fmt"
	"os"
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

func ShowCurrentConfig(cfg config.Config) {
	messages.PrintSection(messages.GetMessage("current_config", cfg), "PURPLE")

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
			Colors["WHITE"].Sprint(""), Colors["END"].Sprint(""), messages.GetMessage("exit", cfg),
			Colors["BLUE"].Sprint(""),
		)
		fmt.Println(optionsText)

		fmt.Printf("\n%s🎯 %s (0-4): %s", Colors["BOLD"].Sprint(""), messages.GetMessage("select_option", cfg), Colors["END"].Sprint(""))

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
				config.UninstallTool()
				return cfg
			}
		case "4":
			ShowHelp(cfg)
		case "0":
			messages.PrintSuccess("👋 " + messages.GetMessage("exit", cfg))
			return cfg
		default:
			messages.PrintError(messages.GetMessage("invalid_option", cfg))
		}
	}
}

func ShowConfigurationInterface(cfg config.Config) config.Config {
	for {
		messages.PrintHeader("⚙️  "+messages.GetMessage("edit_config", cfg), "CYAN")
		ShowCurrentConfig(cfg)

		editOptions := fmt.Sprintf(`
%s===================================================
%s
%s---------------------------------------------------
%s1%s │ 🌐 %s
%s2%s │ 💬 %s
%s3%s │ 🔑 %s
%s4%s │ 🤖 %s
%s5%s │ 🎨 %s
%s6%s │ 🚀 %s
%s7%s │ 💾 %s
%s0%s │ ⬅️  %s
%s===================================================
		`,
			Colors["BLUE"].Sprint(""),
			messages.CenterText(messages.GetMessage("edit_options", cfg), 51),
			Colors["BLUE"].Sprint(""),
			Colors["GREEN"].Sprint(""), Colors["END"].Sprint(""), messages.GetMessage("change_ui_lang", cfg),
			Colors["GREEN"].Sprint(""), Colors["END"].Sprint(""), messages.GetMessage("change_commit_lang", cfg),
			Colors["GREEN"].Sprint(""), Colors["END"].Sprint(""), messages.GetMessage("update_api_key", cfg),
			Colors["GREEN"].Sprint(""), Colors["END"].Sprint(""), messages.GetMessage("change_ai_model", cfg),
			Colors["GREEN"].Sprint(""), Colors["END"].Sprint(""), messages.GetMessage("change_commit_style", cfg),
			Colors["GREEN"].Sprint(""), Colors["END"].Sprint(""), messages.GetMessage("toggle_auto_push", cfg),
			Colors["CYAN"].Sprint(""), Colors["END"].Sprint(""), messages.GetMessage("save_back", cfg),
			Colors["WHITE"].Sprint(""), Colors["END"].Sprint(""), messages.GetMessage("back_no_save", cfg),
			Colors["BLUE"].Sprint(""),
		)
		fmt.Println(editOptions)

		fmt.Printf("\n%s🎯 %s (0-7): %s", Colors["BOLD"].Sprint(""), messages.GetMessage("select_option", cfg), Colors["END"].Sprint(""))

		reader := bufio.NewReader(os.Stdin)
		choice, _ := reader.ReadString('\n')
		choice = strings.TrimSpace(choice)

		switch choice {
		case "1":
			cfg = ChangeUILanguage(cfg)
		case "2":
			cfg = ChangeCommitLanguage(cfg)
		case "3":
			cfg = UpdateAPIKey(cfg)
		case "4":
			cfg = ChangeAIModel(cfg)
		case "5":
			cfg = ChangeCommitStyle(cfg)
		case "6":
			cfg = ToggleAutoPush(cfg)
		case "7":
			config.SaveConfig(cfg)
			messages.PrintSuccess(messages.GetMessage("save_exit", cfg))
			return cfg
		case "0":
			return cfg
		default:
			messages.PrintError(messages.GetMessage("invalid_option", cfg))
		}
	}
}

func ChangeUILanguage(cfg config.Config) config.Config {
	messages.PrintSection("🌐 "+messages.GetMessage("change_ui_lang", cfg), "BLUE")
	fmt.Printf(`
%s%s:
1️⃣  🇺🇸 %s
2️⃣  🇻🇳 %s
	`,
		Colors["BLUE"].Sprint(""), messages.GetMessage("available_langs", cfg),
		messages.GetMessage("lang_1", cfg),
		messages.GetMessage("lang_2", cfg),
	)

	for {
		fmt.Printf("\n%s%s (1-2): %s", Colors["BOLD"].Sprint(""), messages.GetMessage("select_lang", cfg), Colors["END"].Sprint(""))

		reader := bufio.NewReader(os.Stdin)
		choice, _ := reader.ReadString('\n')
		choice = strings.TrimSpace(choice)

		if choice == "1" {
			cfg.UILanguage = "en"
			successMsg := "Interface language changed to English!"
			if cfg.UILanguage == "vi" {
				successMsg = "Đã thay đổi ngôn ngữ giao diện sang Tiếng Anh!"
			}
			messages.PrintSuccess("✅ " + successMsg)
			break
		} else if choice == "2" {
			cfg.UILanguage = "vi"
			successMsg := "Interface language changed to Vietnamese!"
			if cfg.UILanguage == "vi" {
				successMsg = "Đã thay đổi ngôn ngữ giao diện sang Tiếng Việt!"
			}
			messages.PrintSuccess("✅ " + successMsg)
			break
		} else {
			messages.PrintError(messages.GetMessage("invalid_choice", cfg))
		}
	}

	return cfg
}

func ChangeCommitLanguage(cfg config.Config) config.Config {
	messages.PrintSection("💬 "+messages.GetMessage("change_commit_lang", cfg), "BLUE")
	fmt.Printf(`
%s%s:
1️⃣  🇺🇸 %s (feat: add user authentication)
2️⃣  🇻🇳 %s (feat: thêm xác thực người dùng)
	`,
		Colors["BLUE"].Sprint(""), messages.GetMessage("available_langs", cfg),
		messages.GetMessage("lang_1", cfg),
		messages.GetMessage("lang_2", cfg),
	)

	for {
		fmt.Printf("\n%s%s (1-2): %s", Colors["BOLD"].Sprint(""), messages.GetMessage("select_lang", cfg), Colors["END"].Sprint(""))

		reader := bufio.NewReader(os.Stdin)
		choice, _ := reader.ReadString('\n')
		choice = strings.TrimSpace(choice)

		if choice == "1" {
			cfg.CommitLanguage = "en"
			successMsg := "Commit language changed to English!"
			if cfg.UILanguage == "vi" {
				successMsg = "Đã thay đổi ngôn ngữ commit sang Tiếng Anh!"
			}
			messages.PrintSuccess("✅ " + successMsg)
			break
		} else if choice == "2" {
			cfg.CommitLanguage = "vi"
			successMsg := "Commit language changed to Vietnamese!"
			if cfg.UILanguage == "vi" {
				successMsg = "Đã thay đổi ngôn ngữ commit sang Tiếng Việt!"
			}
			messages.PrintSuccess("✅ " + successMsg)
			break
		} else {
			messages.PrintError(messages.GetMessage("invalid_choice", cfg))
		}
	}

	return cfg
}

func UpdateAPIKey(cfg config.Config) config.Config {
	messages.PrintSection("🔑 "+messages.GetMessage("update_api_key", cfg), "BLUE")

	// Get primary account
	primaryAccount := config.GetPrimaryAccount(cfg)

	if primaryAccount != nil {
		currentKey := primaryAccount.APIKey
		if currentKey != "" {
			maskedKey := currentKey[:8] + strings.Repeat("*", len(currentKey)-12) + currentKey[len(currentKey)-4:]
			if len(currentKey) <= 12 {
				maskedKey = strings.Repeat("*", len(currentKey))
			}
			fmt.Printf("Current API key: %s%s%s\n", Colors["DIM"].Sprint(""), maskedKey, Colors["END"].Sprint(""))
		}
	}

	fmt.Printf("\n%s%s: %s", Colors["BOLD"].Sprint(""), messages.GetMessage("enter_api_key_prompt", cfg), Colors["END"].Sprint(""))

	reader := bufio.NewReader(os.Stdin)
	newKey, _ := reader.ReadString('\n')
	newKey = strings.TrimSpace(newKey)

	if newKey != "" {
		if primaryAccount != nil {
			for i := range cfg.Accounts {
				if cfg.Accounts[i].IsPrimary {
					cfg.Accounts[i].APIKey = newKey
					break
				}
			}
		} else {
			// Create new account if none exists
			cfg.Accounts = []config.Account{{
				Email:     "primary@example.com",
				APIKey:    newKey,
				Model:     "gemini-2.0-flash",
				IsPrimary: true,
			}}
		}
		successMsg := "API key updated successfully!"
		if cfg.UILanguage == "vi" {
			successMsg = "Đã cập nhật API key thành công!"
		}
		messages.PrintSuccess("✅ " + successMsg)
	} else {
		infoMsg := "API key unchanged."
		if cfg.UILanguage == "vi" {
			infoMsg = "API key không thay đổi."
		}
		messages.PrintInfo("ℹ️  " + infoMsg)
	}

	return cfg
}

func ChangeAIModel(cfg config.Config) config.Config {
	messages.PrintSection("🤖 "+messages.GetMessage("change_ai_model", cfg), "BLUE")
	fmt.Printf(`
%s%s:
1️⃣  🚀 Gemini 2.5 Pro - %sRecommended%s (Best quality)
2️⃣  ⚡ Gemini 2.5 Flash - %sFast%s (Good quality, fast)
3️⃣  💡 Gemini 2.5 Flash-Lite - %sEfficient%s (Lightweight)
4️⃣  🚀 Gemini 2.0 Flash - %sLegacy%s (Compatible)
	`,
		Colors["BLUE"].Sprint(""), messages.GetMessage("available_models", cfg),
		Colors["GREEN"].Sprint(""), Colors["END"].Sprint(""),
		Colors["YELLOW"].Sprint(""), Colors["END"].Sprint(""),
		Colors["BLUE"].Sprint(""), Colors["END"].Sprint(""),
		Colors["DIM"].Sprint(""), Colors["END"].Sprint(""),
	)

	// Get primary account model
	primaryModel := "gemini-2.0-flash"
	primaryAccount := config.GetPrimaryAccount(cfg)
	if primaryAccount != nil {
		primaryModel = primaryAccount.Model
	}

	modelMap := map[string]string{
		"gemini-2.5-pro":        "1",
		"gemini-2.5-flash":      "2",
		"gemini-2.5-flash-lite": "3",
		"gemini-2.0-flash":      "4",
	}

	currentChoice := modelMap[primaryModel]
	fmt.Printf("Current selection: %s\n", currentChoice)

	for {
		fmt.Printf("%s%s (1-4): %s", Colors["BOLD"].Sprint(""), messages.GetMessage("select_model", cfg), Colors["END"].Sprint(""))

		reader := bufio.NewReader(os.Stdin)
		choice, _ := reader.ReadString('\n')
		choice = strings.TrimSpace(choice)

		if choice == "1" || choice == "2" || choice == "3" || choice == "4" {
			modelChoices := map[string]string{
				"1": "gemini-2.5-pro",
				"2": "gemini-2.5-flash",
				"3": "gemini-2.5-flash-lite",
				"4": "gemini-2.0-flash",
			}
			newModel := modelChoices[choice]

			// Update primary account model
			for i := range cfg.Accounts {
				if cfg.Accounts[i].IsPrimary {
					cfg.Accounts[i].Model = newModel
					break
				}
			}

			successMsgs := map[string]string{
				"1": "🚀 Changed to Gemini 2.5 Pro!",
				"2": "⚡ Changed to Gemini 2.5 Flash!",
				"3": "💡 Changed to Gemini 2.5 Flash-Lite!",
				"4": "🚀 Changed to Gemini 2.0 Flash!",
			}
			messages.PrintSuccess(successMsgs[choice])
			break
		} else {
			messages.PrintError(messages.GetMessage("invalid_choice", cfg))
		}
	}

	return cfg
}

func ChangeCommitStyle(cfg config.Config) config.Config {
	messages.PrintSection("🎨 "+messages.GetMessage("change_commit_style", cfg), "BLUE")
	fmt.Printf(`
%s%s:

1️⃣  📋 %sConventional Commits%s
    Example: %sfeat: add user authentication system%s
    
2️⃣  😄 %sEmoji Style%s  
    Example: %s✨ add user authentication system%s
    
3️⃣  📝 %sDescriptive%s
    Example: %sAdd comprehensive user authentication system%s
	`,
		Colors["BLUE"].Sprint(""), messages.GetMessage("available_styles", cfg),
		Colors["BOLD"].Sprint(""), Colors["END"].Sprint(""), Colors["GREEN"].Sprint(""), Colors["END"].Sprint(""),
		Colors["BOLD"].Sprint(""), Colors["END"].Sprint(""), Colors["GREEN"].Sprint(""), Colors["END"].Sprint(""),
		Colors["BOLD"].Sprint(""), Colors["END"].Sprint(""), Colors["GREEN"].Sprint(""), Colors["END"].Sprint(""),
	)

	currentStyle := cfg.CommitStyle
	styleMap := map[string]string{"conventional": "1", "emoji": "2", "descriptive": "3"}
	fmt.Printf("Current selection: %s\n", styleMap[currentStyle])

	for {
		fmt.Printf("%s%s (1-3): %s", Colors["BOLD"].Sprint(""), messages.GetMessage("select_style", cfg), Colors["END"].Sprint(""))

		reader := bufio.NewReader(os.Stdin)
		choice, _ := reader.ReadString('\n')
		choice = strings.TrimSpace(choice)

		if choice == "1" {
			cfg.CommitStyle = "conventional"
			successMsg := "Changed to Conventional Commits!"
			if cfg.UILanguage == "vi" {
				successMsg = "Đã đổi sang Conventional Commits!"
			}
			messages.PrintSuccess("📋 " + successMsg)
			break
		} else if choice == "2" {
			cfg.CommitStyle = "emoji"
			successMsg := "Changed to Emoji Style!"
			if cfg.UILanguage == "vi" {
				successMsg = "Đã đổi sang Emoji Style!"
			}
			messages.PrintSuccess("😄 " + successMsg)
			break
		} else if choice == "3" {
			cfg.CommitStyle = "descriptive"
			successMsg := "Changed to Descriptive Style!"
			if cfg.UILanguage == "vi" {
				successMsg = "Đã đổi sang Descriptive Style!"
			}
			messages.PrintSuccess("📝 " + successMsg)
			break
		} else {
			messages.PrintError(messages.GetMessage("invalid_choice", cfg))
		}
	}

	return cfg
}

func ToggleAutoPush(cfg config.Config) config.Config {
	messages.PrintSection("🚀 "+messages.GetMessage("toggle_auto_push", cfg), "BLUE")

	currentStatus := cfg.AutoPush
	statusText := messages.GetMessage("enabled", cfg)
	if !currentStatus {
		statusText = messages.GetMessage("disabled", cfg)
	}
	newStatus := !currentStatus
	actionText := messages.GetMessage("enable", cfg)
	if !newStatus {
		actionText = messages.GetMessage("disable", cfg)
	}

	fmt.Printf("%s is currently %s%s%s\n", messages.GetMessage("auto_push", cfg), Colors["BOLD"].Sprint(""), statusText, Colors["END"].Sprint(""))

	fmt.Printf("%s %s %s? (y/N): ", messages.GetMessage("confirm_toggle", cfg), Colors["BOLD"].Sprint(""), actionText)

	reader := bufio.NewReader(os.Stdin)
	confirm, _ := reader.ReadString('\n')
	confirm = strings.TrimSpace(strings.ToLower(confirm))

	if confirm == "y" || confirm == "yes" || confirm == "có" {
		cfg.AutoPush = newStatus
		emoji := "✅"
		if !newStatus {
			emoji = "❌"
		}
		status := messages.GetMessage("enabled", cfg)
		if !newStatus {
			status = messages.GetMessage("disabled", cfg)
		}
		messages.PrintSuccess(fmt.Sprintf("%s %s %s!", emoji, messages.GetMessage("auto_push", cfg), status))
	} else {
		infoMsg := "Auto push setting unchanged."
		if cfg.UILanguage == "vi" {
			infoMsg = "Cài đặt auto push không thay đổi."
		}
		messages.PrintInfo("ℹ️  " + infoMsg)
	}

	return cfg
}

func ShowHelp(cfg config.Config) {
	messages.PrintHeader("❓ "+messages.GetMessage("help_info", cfg), "CYAN")
	fmt.Println(messages.GetMessage("help_text", cfg))

	fmt.Printf("\n%s%s...%s", Colors["DIM"].Sprint(""), messages.GetMessage("press_enter_continue", cfg), Colors["END"].Sprint(""))

	reader := bufio.NewReader(os.Stdin)
	reader.ReadString('\n')
}

func ConfirmAction(message string, cfg config.Config) bool {
	messages.PrintWarning(message)
	fmt.Print("Type 'yes' to confirm: ")

	reader := bufio.NewReader(os.Stdin)
	confirm, _ := reader.ReadString('\n')
	confirm = strings.TrimSpace(strings.ToLower(confirm))

	return confirm == "yes"
}
