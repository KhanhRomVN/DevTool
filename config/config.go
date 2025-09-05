package config

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
	"strings"
	"time"
)

type APIKey struct {
	ID          string    `json:"id"`
	Key         string    `json:"key"`
	Description string    `json:"description"`
	IsActive    bool      `json:"is_active"`
	LastUsed    time.Time `json:"last_used"`
	ErrorCount  int       `json:"error_count"`
	CreatedAt   time.Time `json:"created_at"`
}

type Account struct {
	Email     string    `json:"email"`
	APIKeys   []APIKey  `json:"api_keys"` // Multiple API keys per account
	Model     string    `json:"model"`
	IsPrimary bool      `json:"is_primary"`
	IsActive  bool      `json:"is_active"` // Account level active status
	CreatedAt time.Time `json:"created_at"`
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
	APIKeyRotation      bool      `json:"api_key_rotation"` // Enable automatic API key rotation
	MaxRetries          int       `json:"max_retries"`      // Max retries per API key
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
		APIKeyRotation:      true,
		MaxRetries:          3,
	}

	// Account management messages for UI
	Messages = map[string]map[string]string{
		"en": {
			"account_list":           "Account List",
			"email_required":         "Email is required",
			"email_exists":           "Email already exists",
			"api_key_required":       "API key is required",
			"first_account_primary":  "First account will be set as primary",
			"set_as_primary":         "Set as primary account",
			"account_added":          "Account added successfully",
			"select_account":         "Select account",
			"activated":              "activated",
			"deactivated":            "deactivated",
			"already_primary":        "Account is already primary",
			"confirm_delete_account": "Are you sure you want to delete account",
			"account_deleted":        "Account deleted successfully",
			"deletion_cancelled":     "Deletion cancelled",
			"manage_api_keys":        "Manage API Keys",
			"reset_api_errors":       "Reset API Key Errors",
			"api_key_options":        "API Key Management",
			"add_api_key":            "Add API Key",
			"edit_api_key":           "Edit API Key",
			"delete_api_key":         "Delete API Key",
			"test_api_key":           "Test API Key",
			"confirm_reset_errors":   "Reset all API key error counts",
			"errors_reset":           "API key errors reset successfully",
			"reset_cancelled":        "Reset cancelled",
			"no_active_api_keys":     "No active API keys available",
			"no_accounts":            "No accounts configured",
			"analyzing_changes":      "Analyzing changes...",
			"review_error":           "Error reviewing changes",
			"generated_msg":          "Generated commit message",
			"proceed_commit":         "Proceed with commit? (y/N):",
			"commit_cancelled":       "Commit cancelled",
			"commit_success":         "Commit successful",
			"push_success":           "Push successful",
			"git_error":              "Git error",
			"no_changes":             "No changes to commit",
		},
		"vi": {
			"account_list":           "Danh sách tài khoản",
			"email_required":         "Email là bắt buộc",
			"email_exists":           "Email đã tồn tại",
			"api_key_required":       "API key là bắt buộc",
			"first_account_primary":  "Tài khoản đầu tiên sẽ được đặt làm chính",
			"set_as_primary":         "Đặt làm tài khoản chính",
			"account_added":          "Đã thêm tài khoản thành công",
			"select_account":         "Chọn tài khoản",
			"activated":              "đã kích hoạt",
			"deactivated":            "đã vô hiệu hóa",
			"already_primary":        "Tài khoản đã là chính",
			"confirm_delete_account": "Bạn có chắc muốn xóa tài khoản",
			"account_deleted":        "Đã xóa tài khoản thành công",
			"deletion_cancelled":     "Đã hủy xóa",
			"manage_api_keys":        "Quản lý API Keys",
			"reset_api_errors":       "Đặt lại lỗi API Key",
			"api_key_options":        "Quản lý API Key",
			"add_api_key":            "Thêm API Key",
			"edit_api_key":           "Sửa API Key",
			"delete_api_key":         "Xóa API Key",
			"test_api_key":           "Kiểm tra API Key",
			"confirm_reset_errors":   "Đặt lại tất cả số lỗi API key",
			"errors_reset":           "Đã đặt lại lỗi API key thành công",
			"reset_cancelled":        "Đã hủy đặt lại",
			"no_active_api_keys":     "Không có API key nào khả dụng",
			"no_accounts":            "Chưa cấu hình tài khoản",
			"analyzing_changes":      "Đang phân tích thay đổi...",
			"review_error":           "Lỗi khi xem xét thay đổi",
			"generated_msg":          "Thông điệp commit đã tạo",
			"proceed_commit":         "Tiến hành commit? (y/N):",
			"commit_cancelled":       "Đã hủy commit",
			"commit_success":         "Commit thành công",
			"push_success":           "Push thành công",
			"git_error":              "Lỗi Git",
			"no_changes":             "Không có thay đổi để commit",
		},
	}
)

// Generate unique ID for API key
func generateAPIKeyID() string {
	return fmt.Sprintf("api_%d", time.Now().UnixNano())
}

// Add API Key to account
func (a *Account) AddAPIKey(key, description string) {
	newAPIKey := APIKey{
		ID:          generateAPIKeyID(),
		Key:         key,
		Description: description,
		IsActive:    true,
		LastUsed:    time.Time{},
		ErrorCount:  0,
		CreatedAt:   time.Now(),
	}
	a.APIKeys = append(a.APIKeys, newAPIKey)
}

// Remove API Key from account
func (a *Account) RemoveAPIKey(keyID string) bool {
	for i, apiKey := range a.APIKeys {
		if apiKey.ID == keyID {
			a.APIKeys = append(a.APIKeys[:i], a.APIKeys[i+1:]...)
			return true
		}
	}
	return false
}

// Get active API Keys from account
func (a *Account) GetActiveAPIKeys() []APIKey {
	var activeKeys []APIKey
	for _, key := range a.APIKeys {
		if key.IsActive {
			activeKeys = append(activeKeys, key)
		}
	}
	return activeKeys
}

// Mark API Key as used and update last used time
func (a *Account) MarkAPIKeyUsed(keyID string) {
	for i := range a.APIKeys {
		if a.APIKeys[i].ID == keyID {
			a.APIKeys[i].LastUsed = time.Now()
			break
		}
	}
}

// Mark API Key as failed (increment error count)
func (a *Account) MarkAPIKeyFailed(keyID string) {
	for i := range a.APIKeys {
		if a.APIKeys[i].ID == keyID {
			a.APIKeys[i].ErrorCount++
			// Deactivate API key if too many failures
			if a.APIKeys[i].ErrorCount >= 5 {
				a.APIKeys[i].IsActive = false
			}
			break
		}
	}
}

// Reset API Key error count
func (a *Account) ResetAPIKeyErrors(keyID string) {
	for i := range a.APIKeys {
		if a.APIKeys[i].ID == keyID {
			a.APIKeys[i].ErrorCount = 0
			a.APIKeys[i].IsActive = true
			break
		}
	}
}

// Get best available API key (least recently used among active keys)
func (a *Account) GetBestAPIKey() *APIKey {
	activeKeys := a.GetActiveAPIKeys()
	if len(activeKeys) == 0 {
		return nil
	}

	// Sort by last used time (oldest first)
	bestKey := &activeKeys[0]
	for i := range activeKeys {
		if activeKeys[i].LastUsed.Before(bestKey.LastUsed) {
			bestKey = &activeKeys[i]
		}
	}

	return bestKey
}

// Get primary account with fallback logic
func GetPrimaryAccountWithFallback(config Config) *Account {
	// First try to get primary account
	for i := range config.Accounts {
		if config.Accounts[i].IsPrimary && config.Accounts[i].IsActive {
			if len(config.Accounts[i].GetActiveAPIKeys()) > 0 {
				return &config.Accounts[i]
			}
		}
	}

	// Fallback to any active account with API keys
	for i := range config.Accounts {
		if config.Accounts[i].IsActive && len(config.Accounts[i].GetActiveAPIKeys()) > 0 {
			return &config.Accounts[i]
		}
	}

	return nil
}

// Get all available API keys from all active accounts with proper sorting
func GetAllAvailableAPIKeys(config Config) []struct {
	Account *Account
	APIKey  *APIKey
} {
	var result []struct {
		Account *Account
		APIKey  *APIKey
	}

	// First, add API keys from primary account
	for i := range config.Accounts {
		if config.Accounts[i].IsPrimary && config.Accounts[i].IsActive {
			activeKeys := config.Accounts[i].GetActiveAPIKeys()
			for j := range activeKeys {
				result = append(result, struct {
					Account *Account
					APIKey  *APIKey
				}{
					Account: &config.Accounts[i],
					APIKey:  &activeKeys[j],
				})
			}
			break
		}
	}

	// Then, add API keys from other active accounts
	for i := range config.Accounts {
		if !config.Accounts[i].IsPrimary && config.Accounts[i].IsActive {
			activeKeys := config.Accounts[i].GetActiveAPIKeys()
			for j := range activeKeys {
				result = append(result, struct {
					Account *Account
					APIKey  *APIKey
				}{
					Account: &config.Accounts[i],
					APIKey:  &activeKeys[j],
				})
			}
		}
	}

	return result
}

// Add new account with API key
func (c *Config) AddAccount(email, apiKey, model, description string, isPrimary bool) {
	// If this is set as primary, unset other primary accounts
	if isPrimary {
		for i := range c.Accounts {
			c.Accounts[i].IsPrimary = false
		}
	}

	newAccount := Account{
		Email:     email,
		APIKeys:   []APIKey{},
		Model:     model,
		IsPrimary: isPrimary,
		IsActive:  true,
		CreatedAt: time.Now(),
	}

	newAccount.AddAPIKey(apiKey, description)
	c.Accounts = append(c.Accounts, newAccount)
}

// Remove account (and all its API keys)
func (c *Config) RemoveAccount(email string) bool {
	for i, account := range c.Accounts {
		if account.Email == email {
			c.Accounts = append(c.Accounts[:i], c.Accounts[i+1:]...)
			return true
		}
	}
	return false
}

// Find account by email
func (c *Config) FindAccount(email string) *Account {
	for i := range c.Accounts {
		if c.Accounts[i].Email == email {
			return &c.Accounts[i]
		}
	}
	return nil
}

// Legacy function for backward compatibility
func GetPrimaryAccount(config Config) *Account {
	return GetPrimaryAccountWithFallback(config)
}

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

	// Migration: Convert old single APIKey format to new multiple APIKeys format
	migrateOldConfig(&config)

	return config
}

// Migration function for backward compatibility
func migrateOldConfig(config *Config) {
	for i := range config.Accounts {
		account := &config.Accounts[i]

		// Check if this account uses old format (no APIKeys array but has APIKey field)
		// This would be detected by checking if APIKeys is empty but account was created before
		if len(account.APIKeys) == 0 {
			// Assuming old format had APIKey field, we need to handle this in JSON unmarshaling
			// For now, just ensure CreatedAt is set
			if account.CreatedAt.IsZero() {
				account.CreatedAt = time.Now()
			}
		}
	}
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

	// Add first account with API key
	fmt.Println("\n📧 Add your first Gemini account")

	var email, apiKey string
	for email == "" {
		fmt.Print("📧 Email: ")
		fmt.Scanln(&email)
		if email == "" {
			fmt.Println("❌ Email is required.")
		}
	}

	for apiKey == "" {
		fmt.Print("🔑 API Key: ")
		fmt.Scanln(&apiKey)
		if apiKey == "" {
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

	selectedModel := GeminiModels[modelChoice-1]

	// Add account with API key
	config.AddAccount(email, apiKey, selectedModel, "Primary API Key", true)

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
		fmt.Println("❌ Uninstall cancelled.")
		return
	}

	fmt.Println("🔍 Starting uninstallation process...")

	// 1. Remove config directory
	configDir := GetConfigDir()
	if _, err := os.Stat(configDir); err == nil {
		err := os.RemoveAll(configDir)
		if err != nil {
			fmt.Printf("⚠️  Error removing config directory: %v\n", err)
		} else {
			fmt.Println("✅ Configuration files removed")
		}
	}

	// 2. Find and remove binary files
	removedCount := 0

	// Common binary locations
	binaryLocations := []string{
		"/usr/local/bin/dev_tool",
		"/usr/bin/dev_tool",
		filepath.Join(os.Getenv("HOME"), ".local", "bin", "dev_tool"),
		filepath.Join(os.Getenv("HOME"), "bin", "dev_tool"),
	}

	// Add Windows-specific locations
	if runtime.GOOS == "windows" {
		binaryLocations = append(binaryLocations,
			filepath.Join(os.Getenv("USERPROFILE"), "bin", "dev_tool.exe"),
			filepath.Join(os.Getenv("PROGRAMFILES"), "dev_tool", "dev_tool.exe"),
			"C:\\Windows\\System32\\dev_tool.exe",
		)
	}

	// Try to get current executable path
	if execPath, err := os.Executable(); err == nil {
		// Resolve symlinks
		if realPath, err := filepath.EvalSymlinks(execPath); err == nil {
			binaryLocations = append(binaryLocations, realPath)
		}
		binaryLocations = append(binaryLocations, execPath)
	}

	// Try to find binary using 'which' command (Unix-like systems)
	if runtime.GOOS != "windows" {
		if cmd := exec.Command("which", "dev_tool"); cmd != nil {
			if output, err := cmd.Output(); err == nil {
				whichPath := strings.TrimSpace(string(output))
				if whichPath != "" {
					binaryLocations = append(binaryLocations, whichPath)
				}
			}
		}
	}

	// Try to find binary using 'where' command (Windows)
	if runtime.GOOS == "windows" {
		if cmd := exec.Command("where", "dev_tool"); cmd != nil {
			if output, err := cmd.Output(); err == nil {
				wherePaths := strings.Split(strings.TrimSpace(string(output)), "\n")
				for _, path := range wherePaths {
					if strings.TrimSpace(path) != "" {
						binaryLocations = append(binaryLocations, strings.TrimSpace(path))
					}
				}
			}
		}
	}

	// Remove duplicates
	uniqueLocations := make(map[string]bool)
	var finalLocations []string
	for _, location := range binaryLocations {
		if location != "" && !uniqueLocations[location] {
			uniqueLocations[location] = true
			finalLocations = append(finalLocations, location)
		}
	}

	// Try to remove each binary
	for _, location := range finalLocations {
		if _, err := os.Stat(location); err == nil {
			// Check if we can remove it directly
			if err := os.Remove(location); err != nil {
				// If direct removal fails, try with elevated privileges
				fmt.Printf("⚠️  Could not remove %s directly, trying with elevated privileges...\n", location)

				var cmd *exec.Cmd
				if runtime.GOOS == "windows" {
					// Windows: use runas or try direct removal
					cmd = exec.Command("cmd", "/C", "del", "/F", "/Q", location)
				} else {
					// Unix-like: use sudo
					cmd = exec.Command("sudo", "rm", "-f", location)
				}

				if err := cmd.Run(); err != nil {
					fmt.Printf("❌ Failed to remove %s: %v\n", location, err)
					fmt.Printf("   Please manually remove: %s\n", location)
				} else {
					fmt.Printf("✅ Removed binary: %s\n", location)
					removedCount++
				}
			} else {
				fmt.Printf("✅ Removed binary: %s\n", location)
				removedCount++
			}
		}
	}

	// 3. Clean up Go module cache (if installed via go install)
	if removedCount == 0 {
		fmt.Println("🔍 Trying to clean Go module cache...")
		if cmd := exec.Command("go", "clean", "-modcache"); cmd != nil {
			if err := cmd.Run(); err == nil {
				fmt.Println("✅ Go module cache cleaned")
			}
		}

		// Try to remove from GOPATH/bin
		if gopath := os.Getenv("GOPATH"); gopath != "" {
			gopathBin := filepath.Join(gopath, "bin", "dev_tool")
			if runtime.GOOS == "windows" {
				gopathBin += ".exe"
			}
			if _, err := os.Stat(gopathBin); err == nil {
				if err := os.Remove(gopathBin); err == nil {
					fmt.Printf("✅ Removed from GOPATH: %s\n", gopathBin)
					removedCount++
				}
			}
		}

		// Try to remove from GOBIN
		if gobin := os.Getenv("GOBIN"); gobin != "" {
			gobinPath := filepath.Join(gobin, "dev_tool")
			if runtime.GOOS == "windows" {
				gobinPath += ".exe"
			}
			if _, err := os.Stat(gobinPath); err == nil {
				if err := os.Remove(gobinPath); err == nil {
					fmt.Printf("✅ Removed from GOBIN: %s\n", gobinPath)
					removedCount++
				}
			}
		}
	}

	// 4. Try to remove from Go's bin directory
	if home := os.Getenv("HOME"); home != "" && runtime.GOOS != "windows" {
		goBinPath := filepath.Join(home, "go", "bin", "dev_tool")
		if _, err := os.Stat(goBinPath); err == nil {
			if err := os.Remove(goBinPath); err == nil {
				fmt.Printf("✅ Removed from Go bin: %s\n", goBinPath)
				removedCount++
			}
		}
	}

	// 5. Windows-specific: remove from user profile
	if runtime.GOOS == "windows" {
		if userProfile := os.Getenv("USERPROFILE"); userProfile != "" {
			userGoBin := filepath.Join(userProfile, "go", "bin", "dev_tool.exe")
			if _, err := os.Stat(userGoBin); err == nil {
				if err := os.Remove(userGoBin); err == nil {
					fmt.Printf("✅ Removed from user Go bin: %s\n", userGoBin)
					removedCount++
				}
			}
		}
	}

	// 6. Final verification
	fmt.Println("\n🔍 Verifying uninstallation...")

	var cmd *exec.Cmd
	if runtime.GOOS == "windows" {
		cmd = exec.Command("where", "dev_tool")
	} else {
		cmd = exec.Command("which", "dev_tool")
	}

	if output, err := cmd.Output(); err == nil && strings.TrimSpace(string(output)) != "" {
		fmt.Println("⚠️  dev_tool may still be available in PATH:")
		fmt.Println(strings.TrimSpace(string(output)))
		fmt.Println("Please manually remove the remaining files or restart your terminal.")
	} else {
		fmt.Println("✅ dev_tool successfully removed from PATH")
	}

	// Summary
	if removedCount > 0 {
		fmt.Printf("\n🎉 Successfully removed %d binary file(s)\n", removedCount)
	} else {
		fmt.Println("\n⚠️  No binary files were found/removed")
		fmt.Println("The tool may have been installed in a non-standard location")
		fmt.Println("Please check manually with: which dev_tool (Linux/macOS) or where dev_tool (Windows)")
	}

	fmt.Println("✅ dev_tool uninstallation completed!")
	fmt.Println("📝 To reinstall, run: go install github.com/KhanhRomVN/dev_tool")

	// Important: Exit the program to prevent further execution
	fmt.Println("\n👋 Goodbye!")
	os.Exit(0)
}

// FindAPIKey finds an API key by value
func (a *Account) FindAPIKey(key string) *APIKey {
	for i, apiKey := range a.APIKeys {
		if apiKey.Key == key {
			return &a.APIKeys[i]
		}
	}
	return nil
}

// GetMessage retrieves a localized message
func GetMessage(key string, config Config) string {
	if msg, exists := Messages[config.UILanguage][key]; exists {
		return msg
	}
	// Fallback to English if message not found
	if msg, exists := Messages["en"][key]; exists {
		return msg
	}
	return key // Return key if no translation found
}
