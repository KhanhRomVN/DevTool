// config/config.go
package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
	"path/filepath"
	"runtime"
	"strings"
)

type Account struct {
	Email     string `json:"email"`
	APIKey    string `json:"api_key"`
	Model     string `json:"model"`
	IsPrimary bool   `json:"is_primary"`
}

type Config struct {
	Accounts            []Account `json:"accounts"`
	UILanguage          string    `json:"ui_language"`
	CommitLanguage      string    `json:"commit_language"`
	AutoPush            bool      `json:"auto_push"`
	AutoStage           bool      `json:"auto_stage"`
	CommitStyle         string    `json:"commit_style"`
	MaxLineLength       int       `json:"max_line_length"`
	ShowDiffStats       bool      `json:"show_diff_stats"`
	ConfirmBeforeCommit bool      `json:"confirm_before_commit"`
}

var (
	GeminiModels = []string{
		"gemini-2.5-pro",
		"gemini-2.5-flash",
		"gemini-2.5-flash-lite",
		"gemini-2.0-flash",
	}

	DefaultConfig = Config{
		Accounts:            []Account{},
		UILanguage:          "en",
		CommitLanguage:      "en",
		AutoPush:            false,
		AutoStage:           false,
		CommitStyle:         "conventional",
		MaxLineLength:       72,
		ShowDiffStats:       true,
		ConfirmBeforeCommit: true,
	}
)

func GetConfigDir() string {
	switch runtime.GOOS {
	case "windows":
		return filepath.Join(os.Getenv("APPDATA"), "dev_tool")
	case "darwin":
		return filepath.Join(os.Getenv("HOME"), "Library", "Application Support", "dev_tool")
	default:
		return filepath.Join(os.Getenv("HOME"), ".config", "dev_tool")
	}
}

func GetConfigPath() string {
	return filepath.Join(GetConfigDir(), "config.json")
}

func LoadConfig() Config {
	configPath := GetConfigPath()

	if _, err := os.Stat(configPath); os.IsNotExist(err) {
		return CreateInitialConfig()
	}

	data, err := ioutil.ReadFile(configPath)
	if err != nil {
		fmt.Printf("Error reading config: %v\n", err)
		return CreateInitialConfig()
	}

	var config Config
	if err := json.Unmarshal(data, &config); err != nil {
		fmt.Printf("Error parsing config: %v\n", err)
		return CreateInitialConfig()
	}

	return config
}

func SaveConfig(config Config) error {
	configDir := GetConfigDir()
	if err := os.MkdirAll(configDir, 0755); err != nil {
		return err
	}

	data, err := json.MarshalIndent(config, "", "  ")
	if err != nil {
		return err
	}

	return ioutil.WriteFile(GetConfigPath(), data, 0644)
}

func CreateInitialConfig() Config {
	config := DefaultConfig
	ShowWelcomeBanner()

	// UI Language selection
	fmt.Println("\n🌐 Choose Interface Language")
	fmt.Println("1️⃣  English")
	fmt.Println("2️⃣  Tiếng Việt")

	var uiLangChoice string
	for {
		fmt.Print("\n🔤 Enter choice (1/2): ")
		fmt.Scanln(&uiLangChoice)
		if uiLangChoice == "1" || uiLangChoice == "2" {
			break
		}
		fmt.Println("❌ Invalid choice. Please try again.")
	}

	if uiLangChoice == "1" {
		config.UILanguage = "en"
	} else {
		config.UILanguage = "vi"
	}

	// Add first account
	fmt.Println("\n📧 Add your first Gemini account")

	account := Account{
		Email:     "",
		APIKey:    "",
		Model:     "gemini-2.0-flash",
		IsPrimary: true,
	}

	for account.Email == "" {
		fmt.Print("📧 Email: ")
		fmt.Scanln(&account.Email)
		if account.Email == "" {
			fmt.Println("❌ Email is required.")
		}
	}

	for account.APIKey == "" {
		fmt.Print("🔑 API Key: ")
		fmt.Scanln(&account.APIKey)
		if account.APIKey == "" {
			fmt.Println("❌ API Key is required.")
		}
	}

	// Model selection
	fmt.Println("\n🤖 Choose your preferred AI model")
	for i, model := range GeminiModels {
		fmt.Printf("%d️⃣  %s\n", i+1, model)
	}

	var modelChoice int
	for {
		fmt.Print("\n🤖 Enter choice (1-4): ")
		_, err := fmt.Scan(&modelChoice)
		if err == nil && modelChoice >= 1 && modelChoice <= 4 {
			break
		}
		fmt.Println("❌ Invalid choice. Please try again.")
	}
	account.Model = GeminiModels[modelChoice-1]

	config.Accounts = []Account{account}

	// Commit language selection
	fmt.Println("\n💬 Choose commit message language")
	fmt.Println("1️⃣  English")
	fmt.Println("2️⃣  Tiếng Việt")

	var commitLangChoice string
	for {
		fmt.Print("\n💬 Enter choice (1/2): ")
		fmt.Scanln(&commitLangChoice)
		if commitLangChoice == "1" || commitLangChoice == "2" {
			break
		}
		fmt.Println("❌ Invalid choice. Please try again.")
	}

	if commitLangChoice == "1" {
		config.CommitLanguage = "en"
	} else {
		config.CommitLanguage = "vi"
	}

	// Commit style selection
	fmt.Println("\n🎨 Choose commit message style")
	fmt.Println("1️⃣  Conventional Commits (feat: add new feature)")
	fmt.Println("2️⃣  Emoji Style (✨ add new feature)")
	fmt.Println("3️⃣  Descriptive (Add user authentication system)")

	var styleChoice string
	for {
		fmt.Print("\n🎨 Enter choice (1-3): ")
		fmt.Scanln(&styleChoice)
		if styleChoice == "1" || styleChoice == "2" || styleChoice == "3" {
			break
		}
		fmt.Println("❌ Invalid choice. Please try again.")
	}

	styles := map[string]string{"1": "conventional", "2": "emoji", "3": "descriptive"}
	config.CommitStyle = styles[styleChoice]

	// Auto-stage configuration
	fmt.Print("\n📦 Enable automatic staging (git add .)? (y/N): ")
	var autoStage string
	fmt.Scanln(&autoStage)
	config.AutoStage = autoStage == "y" || autoStage == "yes"

	// Auto-push configuration
	fmt.Print("\n🚀 Enable automatic push after commit? (y/N): ")
	var autoPush string
	fmt.Scanln(&autoPush)
	config.AutoPush = autoPush == "y" || autoPush == "yes"

	if err := SaveConfig(config); err != nil {
		fmt.Printf("Error saving config: %v\n", err)
	}

	fmt.Println("✅ Configuration saved successfully!")
	return config
}

func ShowWelcomeBanner() {
	banner := `
==================================================
              🛠️  DEV TOOL 2.0                
          AI-Powered Git Assistant            
                                                  
   🤖 Smart commit messages                       
   🌍 Multi-language support                      
   🎨 Multiple commit styles                      
   👥 Multi-account management                   
   ⚙️  Cross-platform compatibility              
==================================================
Welcome! Let's set up your AI git assistant.
	`
	fmt.Println(banner)
}

func ResetConfig() Config {
	configPath := GetConfigPath()
	if _, err := os.Stat(configPath); err == nil {
		os.Remove(configPath)
	}

	config := CreateInitialConfig()
	fmt.Println("🔄 Configuration reset successfully!")
	return config
}

func UninstallTool() {
	fmt.Println("⚠️  This will completely remove dev_tool and all its data!")
	fmt.Print("Are you sure you want to uninstall? (yes/no): ")
	var confirm string
	fmt.Scanln(&confirm)
	confirm = strings.ToLower(confirm)

	if confirm != "yes" && confirm != "y" {
		fmt.Println("Uninstall cancelled.")
		return
	}

	// Remove config directory
	configDir := GetConfigDir()
	if _, err := os.Stat(configDir); err == nil {
		err := os.RemoveAll(configDir)
		if err != nil {
			fmt.Printf("Error during uninstall: %v\n", err)
			return
		}
	}

	fmt.Println("✅ dev_tool has been uninstalled successfully!")
	fmt.Println("To reinstall, run: go install github.com/your-repo/dev_tool")
}

func GetPrimaryAccount(config Config) *Account {
	for i, account := range config.Accounts {
		if account.IsPrimary {
			return &config.Accounts[i]
		}
	}
	return nil
}
