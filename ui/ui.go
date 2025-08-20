// ui/ui.go
package ui

import (
	"bufio"
	"dev_tool/config"
	"dev_tool/messages"
	"fmt"
	"os"
	"strings"
)

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
	styleDisplay := styleMap[config.CommitStyle]

	// Model display
	modelDisplay := "Unknown"
	if len(cfg.Accounts) > 0 {
		modelDisplay = map[string]string{
			"gemini-2.0-flash":      "🚀 Gemini 2.0 Flash",
			"gemini-2.0-flash-lite": "⚡ Gemini 2.0 Flash-Lite",
			"gemini-2.5-pro":        "🚀 Gemini 2.5 Pro",
			"gemini-2.5-flash":      "⚡ Gemini 2.5 Flash",
			"gemini-2.5-flash-lite": "💡 Gemini 2.5 Flash-Lite",
		}[cfg.Accounts[0].Model]
	}

	// Get account info
	primaryAccount := GetPrimaryAccount(cfg)
	accountInfo := ""
	if primaryAccount != nil {
		email := primaryAccount.Email
		model := primaryAccount.Model
		accountInfo = fmt.Sprintf("%s📧 Primary Account: %s\n%s🤖 Account Model:   %s\n",
			Colors["YELLOW"], email, Colors["YELLOW"], model)
	}

	fmt.Printf(`
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
		Colors["CYAN"],
		CenterText(messages.GetMessage("current_config", cfg), 51),
		Colors["CYAN"],
		Colors["YELLOW"], messages.GetMessage("ui_lang", cfg), uiLangDisplay,
		Colors["YELLOW"], messages.GetMessage("commit_lang", cfg), commitLangDisplay,
		Colors["YELLOW"], messages.GetMessage("commit_style", cfg), styleDisplay,
		accountInfo,
		Colors["YELLOW"], messages.GetMessage("auto_push", cfg), GetStatusDisplay(cfg.AutoPush, cfg),
		Colors["YELLOW"], messages.GetMessage("auto_stage", cfg), GetStatusDisplay(cfg.AutoStage, cfg),
		Colors["CYAN"],
	)
}

func GetStatusDisplay(enabled bool, cfg config.Config) string {
	if enabled {
		return fmt.Sprintf("%s✅ %s", Colors["GREEN"], messages.GetMessage("enabled", config))
	}
	return fmt.Sprintf("%s❌ %s", Colors["RED"], messages.GetMessage("disabled", config))
}

func ShowSettingsMenu(cfg config.Config) {
	for {
		PrintHeader(messages.GetMessage("settings_menu", cfg))
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
			Colors["BLUE"],
			CenterText(messages.GetMessage("options", config), 51),
			Colors["BLUE"],
			Colors["GREEN"], Colors["END"], messages.GetMessage("edit_config", config),
			Colors["YELLOW"], Colors["END"], messages.GetMessage("reset_defaults", config),
			Colors["RED"], Colors["END"], messages.GetMessage("uninstall_tool", config),
			Colors["CYAN"], Colors["END"], messages.GetMessage("help_info", config),
			Colors["WHITE"], Colors["END"], messages.GetMessage("exit", config),
			Colors["BLUE"],
		)
		fmt.Println(optionsText)

		fmt.Printf("\n%s🎯 %s (0-4): %s", Colors["BOLD"], messages.GetMessage("select_option", config), Colors["END"])

		reader := bufio.NewReader(os.Stdin)
		choice, _ := reader.ReadString('\n')
		choice = strings.TrimSpace(choice)

		switch choice {
		case "1":
			config = ShowConfigurationInterface(config)
			SaveConfig(config)
		case "2":
			if ConfirmAction(messages.GetMessage("reset_confirm", config), config) {
				config = ResetConfig()
			}
		case "3":
			if ConfirmAction(messages.GetMessage("uninstall_confirm", config), config) {
				UninstallTool()
				return
			}
		case "4":
			ShowHelp(config)
		case "0":
			PrintSuccess("👋 " + messages.GetMessage("exit", config))
			return
		default:
			PrintError(messages.GetMessage("invalid_option", config))
		}
	}
}

func ShowConfigurationInterface(config Config) Config {
	for {
		PrintHeader("⚙️  " + messages.GetMessage("edit_config", config))
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
			Colors["BLUE"],
			CenterText(messages.GetMessage("edit_options", config), 51),
			Colors["BLUE"],
			Colors["GREEN"], Colors["END"], messages.GetMessage("change_ui_lang", config),
			Colors["GREEN"], Colors["END"], messages.GetMessage("change_commit_lang", config),
			Colors["GREEN"], Colors["END"], messages.GetMessage("update_api_key", config),
			Colors["GREEN"], Colors["END"], messages.GetMessage("change_ai_model", config),
			Colors["GREEN"], Colors["END"], messages.GetMessage("change_commit_style", config),
			Colors["GREEN"], Colors["END"], messages.GetMessage("toggle_auto_push", config),
			Colors["CYAN"], Colors["END"], messages.GetMessage("save_back", config),
			Colors["WHITE"], Colors["END"], messages.GetMessage("back_no_save", config),
			Colors["BLUE"],
		)
		fmt.Println(editOptions)

		fmt.Printf("\n%s🎯 %s (0-7): %s", Colors["BOLD"], messages.GetMessage("select_option", config), Colors["END"])

		reader := bufio.NewReader(os.Stdin)
		choice, _ := reader.ReadString('\n')
		choice = strings.TrimSpace(choice)

		switch choice {
		case "1":
			config = ChangeUILanguage(config)
		case "2":
			config = ChangeCommitLanguage(config)
		case "3":
			config = UpdateAPIKey(config)
		case "4":
			config = ChangeAIModel(config)
		case "5":
			config = ChangeCommitStyle(config)
		case "6":
			config = ToggleAutoPush(config)
		case "7":
			SaveConfig(config)
			PrintSuccess(messages.GetMessage("save_exit", config))
			return config
		case "0":
			return config
		default:
			PrintError(messages.GetMessage("invalid_option", config))
		}
	}
}

func ChangeUILanguage(config Config) Config {
	PrintSection("🌐 " + messages.GetMessage("change_ui_lang", config))
	fmt.Printf(`
%s%s:
1️⃣  🇺🇸 %s
2️⃣  🇻🇳 %s
	`,
		Colors["BLUE"], messages.GetMessage("available_langs", config),
		messages.GetMessage("lang_1", config),
		messages.GetMessage("lang_2", config),
	)

	for {
		fmt.Printf("\n%s%s (1-2): %s", Colors["BOLD"], messages.GetMessage("select_lang", config), Colors["END"])

		reader := bufio.NewReader(os.Stdin)
		choice, _ := reader.ReadString('\n')
		choice = strings.TrimSpace(choice)

		if choice == "1" {
			config.UILanguage = "en"
			successMsg := "Interface language changed to English!"
			if config.UILanguage == "vi" {
				successMsg = "Đã thay đổi ngôn ngữ giao diện sang Tiếng Anh!"
			}
			PrintSuccess("✅ " + successMsg)
			break
		} else if choice == "2" {
			config.UILanguage = "vi"
			successMsg := "Interface language changed to Vietnamese!"
			if config.UILanguage == "vi" {
				successMsg = "Đã thay đổi ngôn ngữ giao diện sang Tiếng Việt!"
			}
			PrintSuccess("✅ " + successMsg)
			break
		} else {
			PrintError(messages.GetMessage("invalid_choice", config))
		}
	}

	return config
}

func ChangeCommitLanguage(config Config) Config {
	PrintSection("💬 " + messages.GetMessage("change_commit_lang", config))
	fmt.Printf(`
%s%s:
1️⃣  🇺🇸 %s (feat: add user authentication)
2️⃣  🇻🇳 %s (feat: thêm xác thực người dùng)
	`,
		Colors["BLUE"], messages.GetMessage("available_langs", config),
		messages.GetMessage("lang_1", config),
		messages.GetMessage("lang_2", config),
	)

	for {
		fmt.Printf("\n%s%s (1-2): %s", Colors["BOLD"], messages.GetMessage("select_lang", config), Colors["END"])

		reader := bufio.NewReader(os.Stdin)
		choice, _ := reader.ReadString('\n')
		choice = strings.TrimSpace(choice)

		if choice == "1" {
			config.CommitLanguage = "en"
			successMsg := "Commit language changed to English!"
			if config.UILanguage == "vi" {
				successMsg = "Đã thay đổi ngôn ngữ commit sang Tiếng Anh!"
			}
			PrintSuccess("✅ " + successMsg)
			break
		} else if choice == "2" {
			config.CommitLanguage = "vi"
			successMsg := "Commit language changed to Vietnamese!"
			if config.UILanguage == "vi" {
				successMsg = "Đã thay đổi ngôn ngữ commit sang Tiếng Việt!"
			}
			PrintSuccess("✅ " + successMsg)
			break
		} else {
			PrintError(messages.GetMessage("invalid_choice", config))
		}
	}

	return config
}

func UpdateAPIKey(config Config) Config {
	PrintSection("🔑 " + messages.GetMessage("update_api_key", config))

	// Get primary account
	primaryAccount := GetPrimaryAccount(config)

	if primaryAccount != nil {
		currentKey := primaryAccount.APIKey
		if currentKey != "" {
			maskedKey := currentKey[:8] + strings.Repeat("*", len(currentKey)-12) + currentKey[len(currentKey)-4:]
			if len(currentKey) <= 12 {
				maskedKey = strings.Repeat("*", len(currentKey))
			}
			fmt.Printf("Current API key: %s%s%s\n", Colors["DIM"], maskedKey, Colors["END"])
		}
	}

	fmt.Printf("\n%s%s: %s", Colors["BOLD"], messages.GetMessage("enter_api_key_prompt", config), Colors["END"])

	reader := bufio.NewReader(os.Stdin)
	newKey, _ := reader.ReadString('\n')
	newKey = strings.TrimSpace(newKey)

	if newKey != "" {
		if primaryAccount != nil {
			for i := range config.Accounts {
				if config.Accounts[i].IsPrimary {
					config.Accounts[i].APIKey = newKey
					break
				}
			}
		} else {
			// Create new account if none exists
			config.Accounts = []Account{{
				Email:     "primary@example.com",
				APIKey:    newKey,
				Model:     "gemini-2.0-flash",
				IsPrimary: true,
			}}
		}
		successMsg := "API key updated successfully!"
		if config.UILanguage == "vi" {
			successMsg = "Đã cập nhật API key thành công!"
		}
		PrintSuccess("✅ " + successMsg)
	} else {
		infoMsg := "API key unchanged."
		if config.UILanguage == "vi" {
			infoMsg = "API key không thay đổi."
		}
		PrintInfo("ℹ️  " + infoMsg)
	}

	return config
}

func ChangeAIModel(config Config) Config {
	PrintSection("🤖 " + messages.GetMessage("change_ai_model", config))
	fmt.Printf(`
%s%s:
1️⃣  🚀 Gemini 2.5 Pro - %sRecommended%s (Best quality)
2️⃣  ⚡ Gemini 2.5 Flash - %sFast%s (Good quality, fast)
3️⃣  💡 Gemini 2.5 Flash-Lite - %sEfficient%s (Lightweight)
4️⃣  🚀 Gemini 2.0 Flash - %sLegacy%s (Compatible)
	`,
		Colors["BLUE"], messages.GetMessage("available_models", config),
		Colors["GREEN"], Colors["END"],
		Colors["YELLOW"], Colors["END"],
		Colors["BLUE"], Colors["END"],
		Colors["DIM"], Colors["END"],
	)

	// Get primary account model
	primaryModel := "gemini-2.0-flash"
	primaryAccount := GetPrimaryAccount(config)
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
		fmt.Printf("%s%s (1-4): %s", Colors["BOLD"], messages.GetMessage("select_model", config), Colors["END"])

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
			for i := range config.Accounts {
				if config.Accounts[i].IsPrimary {
					config.Accounts[i].Model = newModel
					break
				}
			}

			successMsgs := map[string]string{
				"1": "🚀 Changed to Gemini 2.5 Pro!",
				"2": "⚡ Changed to Gemini 2.5 Flash!",
				"3": "💡 Changed to Gemini 2.5 Flash-Lite!",
				"4": "🚀 Changed to Gemini 2.0 Flash!",
			}
			PrintSuccess(successMsgs[choice])
			break
		} else {
			PrintError(messages.GetMessage("invalid_choice", config))
		}
	}

	return config
}

func ChangeCommitStyle(config Config) Config {
	PrintSection("🎨 " + messages.GetMessage("change_commit_style", config))
	fmt.Printf(`
%s%s:

1️⃣  📋 %sConventional Commits%s
    Example: %sfeat: add user authentication system%s
    
2️⃣  😄 %sEmoji Style%s  
    Example: %s✨ add user authentication system%s
    
3️⃣  📝 %sDescriptive%s
    Example: %sAdd comprehensive user authentication system%s
	`,
		Colors["BLUE"], messages.GetMessage("available_styles", config),
		Colors["BOLD"], Colors["END"], Colors["GREEN"], Colors["END"],
		Colors["BOLD"], Colors["END"], Colors["GREEN"], Colors["END"],
		Colors["BOLD"], Colors["END"], Colors["GREEN"], Colors["END"],
	)

	currentStyle := config.CommitStyle
	styleMap := map[string]string{"conventional": "1", "emoji": "2", "descriptive": "3"}
	fmt.Printf("Current selection: %s\n", styleMap[currentStyle])

	for {
		fmt.Printf("%s%s (1-3): %s", Colors["BOLD"], messages.GetMessage("select_style", config), Colors["END"])

		reader := bufio.NewReader(os.Stdin)
		choice, _ := reader.ReadString('\n')
		choice = strings.TrimSpace(choice)

		if choice == "1" {
			config.CommitStyle = "conventional"
			successMsg := "Changed to Conventional Commits!"
			if config.UILanguage == "vi" {
				successMsg = "Đã đổi sang Conventional Commits!"
			}
			PrintSuccess("📋 " + successMsg)
			break
		} else if choice == "2" {
			config.CommitStyle = "emoji"
			successMsg := "Changed to Emoji Style!"
			if config.UILanguage == "vi" {
				successMsg = "Đã đổi sang Emoji Style!"
			}
			PrintSuccess("😄 " + successMsg)
			break
		} else if choice == "3" {
			config.CommitStyle = "descriptive"
			successMsg := "Changed to Descriptive Style!"
			if config.UILanguage == "vi" {
				successMsg = "Đã đổi sang Descriptive Style!"
			}
			PrintSuccess("📝 " + successMsg)
			break
		} else {
			PrintError(messages.GetMessage("invalid_choice", config))
		}
	}

	return config
}

func ToggleAutoPush(config Config) Config {
	PrintSection("🚀 " + messages.GetMessage("toggle_auto_push", config))

	currentStatus := config.AutoPush
	statusText := messages.GetMessage("enabled", config)
	if !currentStatus {
		statusText = messages.GetMessage("disabled", config)
	}
	newStatus := !currentStatus
	actionText := messages.GetMessage("enable", config)
	if !newStatus {
		actionText = messages.GetMessage("disable", config)
	}

	fmt.Printf("%s %s %s%s%s\n", messages.GetMessage("auto_push", config), messages.GetMessage("is_currently", config), Colors["BOLD"], statusText, Colors["END"])

	fmt.Printf("%s %s %s? (y/N): ", messages.GetMessage("confirm_toggle", config), Colors["BOLD"], actionText)

	reader := bufio.NewReader(os.Stdin)
	confirm, _ := reader.ReadString('\n')
	confirm = strings.TrimSpace(strings.ToLower(confirm))

	if confirm == "y" || confirm == "yes" || confirm == "có" {
		config.AutoPush = newStatus
		emoji := "✅"
		if !newStatus {
			emoji = "❌"
		}
		status := messages.GetMessage("enabled", config)
		if !newStatus {
			status = messages.GetMessage("disabled", config)
		}
		PrintSuccess(fmt.Sprintf("%s %s %s!", emoji, messages.GetMessage("auto_push", config), status))
	} else {
		infoMsg := "Auto push setting unchanged."
		if config.UILanguage == "vi" {
			infoMsg = "Cài đặt auto push không thay đổi."
		}
		PrintInfo("ℹ️  " + infoMsg)
	}

	return config
}

func ShowHelp(config Config) {
	PrintHeader("❓ " + messages.GetMessage("help_info", config))
	fmt.Println(messages.GetMessage("help_text", config))

	fmt.Printf("\n%s%s...%s", Colors["DIM"], messages.GetMessage("press_enter_continue", config), Colors["END"])

	reader := bufio.NewReader(os.Stdin)
	reader.ReadString('\n')
}

func ConfirmAction(message string, config Config) bool {
	PrintWarning(message)
	fmt.Print(messages.GetMessage("type_yes_confirm", config))

	reader := bufio.NewReader(os.Stdin)
	confirm, _ := reader.ReadString('\n')
	confirm = strings.TrimSpace(strings.ToLower(confirm))

	return confirm == "yes"
}
