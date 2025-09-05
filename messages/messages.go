package messages

import (
	"dev_tool/config"
	"fmt"
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
}

var Messages = map[string]map[string]string{
	"en": {
		"welcome":              "Dev Tool - AI Git Assistant",
		"enter_api_key":        "Enter your Gemini API key",
		"add_first_account":    "Add your first Gemini account",
		"choose_model":         "Choose your preferred AI model",
		"model_1":              "Gemini 2.5 Pro - Most advanced (Recommended)",
		"model_2":              "Gemini 2.5 Flash - Fast and capable",
		"model_3":              "Gemini 2.5 Flash-Lite - Lightweight and efficient",
		"model_4":              "Gemini 2.0 Flash - Legacy model",
		"choose_ui_lang":       "Choose interface language",
		"lang_1":               "English",
		"lang_2":               "Tiếng Việt",
		"choose_commit_lang":   "Choose commit message language",
		"choose_commit_style":  "Choose commit message style",
		"choose_auto_stage":    "Enable automatic staging (git add .)? (y/N)",
		"choose_auto_push":     "Enable automatic push after commit? (y/N)",
		"invalid_choice":       "Invalid choice. Please try again.",
		"config_saved":         "Configuration saved successfully!",
		"no_changes":           "No staged changes found. Use 'git add' to stage your changes.",
		"analyzing_changes":    "Analyzing your changes...",
		"generated_msg":        "Generated commit message",
		"proceed_commit":       "Proceed with commit? (y/N)",
		"commit_cancelled":     "Commit cancelled.",
		"commit_success":       "Changes committed successfully!",
		"push_success":         "🚀 Changes pushed successfully!",
		"git_error":            "❌ Git operation failed",
		"review_error":         "❌ Code review failed",
		"settings_menu":        "⚙️  Settings Menu",
		"current_config":       "📋 Current Configuration",
		"ui_lang":              "Interface Language",
		"commit_lang":          "Commit Language",
		"commit_style":         "Commit Style",
		"auto_push":            "Auto Push",
		"auto_stage":           "Auto Stage",
		"toggle_auto_stage":    "Toggle Auto Stage",
		"enabled":              "Enabled",
		"disabled":             "Disabled",
		"select_option":        "Select an option",
		"invalid_option":       "❌ Invalid option. Please try again.",
		"save_exit":            "💾 Configuration saved successfully!",
		"reset_confirm":        "⚠️  This will reset all settings to defaults. Continue?",
		"reset_success":        "🔄 Settings reset successfully!",
		"uninstall_confirm":    "⚠️  This will completely remove dev_tool. Continue?",
		"uninstall_success":    "✅ dev_tool uninstalled successfully!",
		"back_to_menu":         "⬅️  Back to menu",
		"exit":                 "Exit",
		"account_manager":      "Account Manager",
		"add_account":          "➕ Add Account",
		"edit_account":         "✏️ Edit Account",
		"delete_account":       "🗑️ Delete Account",
		"set_primary":          "⭐ Set as Primary",
		"no_accounts":          "❌ No accounts configured",
		"account_email":        "📧 Email",
		"account_model":        "🤖 Model",
		"account_status":       "🔑 Status",
		"primary":              "⭐ Primary",
		"secondary":            "🔑 Secondary",
		"help_text":            "🛠️  Dev Tool - AI Git Assistant\n================================\n\n📚 Available Commands:\n  dev_tool              Generate AI commit message and commit\n  dev_tool --no-push    Commit without pushing to remote\n  dev_tool settings     Open settings menu\n  dev_tool --version    Show version information\n\n⚙️  Settings Menu Options:\n  Edit Configuration    Modify language, model, and preferences\n  Account Manager       Manage multiple Gemini accounts\n  Reset to Defaults     Reset all settings to initial state\n  Uninstall Tool        Completely remove dev_tool\n\n🎨 Commit Styles:\n  Conventional          feat: add user authentication\n  Emoji                 ✨ add user authentication  \n  Descriptive           Add comprehensive user authentication system\n\n🌍 Supported Languages:\n  Interface: English, Vietnamese\n  Commits: English, Vietnamese\n\n🤖 Supported Models:\n  Gemini 2.5 Pro        Most advanced model (recommended)\n  Gemini 2.5 Flash      Fast and capable\n  Gemini 2.5 Flash-Lite Lightweight and efficient\n  Gemini 2.0 Flash      Legacy model\n\n📖 For more help: https://github.com/your-repo/dev_tool",
		"edit_config":          "Edit Configuration",
		"reset_defaults":       "Reset to Defaults",
		"uninstall_tool":       "Uninstall Tool",
		"help_info":            "Help & Information",
		"options":              "Options",
		"change_ui_lang":       "Change Interface Language",
		"change_commit_lang":   "Change Commit Language",
		"update_api_key":       "Update API Key",
		"change_ai_model":      "Change AI Model",
		"change_commit_style":  "Change Commit Style",
		"toggle_auto_push":     "Toggle Auto Push",
		"save_back":            "Save & Back to Menu",
		"back_no_save":         "Back without Saving",
		"edit_options":         "Edit Options",
		"available_langs":      "Available Languages",
		"select_lang":          "Select language",
		"enter_api_key_prompt": "Enter new API key",
		"available_models":     "Available Models",
		"select_model":         "Select model",
		"available_styles":     "Available Styles",
		"select_style":         "Select style",
		"confirm_toggle":       "Do you want to",
		"enable":               "enable",
		"disable":              "disable",
		"press_enter_continue": "Press Enter to continue",
		"type_yes_confirm":     "Type 'yes' to confirm:",
		"is_currently":         "is currently",
		// New account management messages
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
	},
	"vi": {
		"welcome":              "Dev Tool - Trợ Lý Git AI",
		"enter_api_key":        "Nhập Gemini API key của bạn",
		"add_first_account":    "Thêm tài khoản Gemini đầu tiên",
		"choose_model":         "Chọn model AI ưa thích",
		"model_1":              "Gemini 2.5 Pro - Tiên tiến nhất (Khuyên dùng)",
		"model_2":              "Gemini 2.5 Flash - Nhanh và mạnh mẽ",
		"model_3":              "Gemini 2.5 Flash-Lite - Nhẹ và hiệu quả",
		"model_4":              "Gemini 2.0 Flash - Model cũ",
		"choose_ui_lang":       "Chọn ngôn ngữ giao diện",
		"lang_1":               "Tiếng Anh",
		"lang_2":               "Tiếng Việt",
		"choose_commit_lang":   "Chọn ngôn ngữ commit message",
		"choose_commit_style":  "Chọn phong cách commit message",
		"choose_auto_stage":    "Bật tự động staging (git add .)? (y/N)",
		"choose_auto_push":     "Bật tự động push sau khi commit? (y/N)",
		"invalid_choice":       "❌ Lựa chọn không hợp lệ. Vui lòng thử lại.",
		"config_saved":         "✅ Đã lưu cấu hình thành công!",
		"no_changes":           "❌ Không có thay đổi nào được staged. Dùng 'git add' để stage thay đổi.",
		"analyzing_changes":    "🔍 Đang phân tích các thay đổi của bạn...",
		"generated_msg":        "📝 Commit message đã tạo",
		"proceed_commit":       "🚀 Tiếp tục commit? (y/N)",
		"commit_cancelled":     "❌ Đã hủy commit.",
		"commit_success":       "✅ Đã commit thay đổi thành công!",
		"push_success":         "🚀 Đã push thay đổi thành công!",
		"git_error":            "❌ Thao tác git thất bại",
		"review_error":         "❌ Review code thất bại",
		"settings_menu":        "⚙️  Menu Cài Đặt",
		"current_config":       "📋 Cấu Hình Hiện Tại",
		"ui_lang":              "Ngôn Ngữ Giao Diện",
		"commit_lang":          "Ngôn Ngữ Commit",
		"commit_style":         "Phong Cách Commit",
		"auto_push":            "Tự Động Push",
		"auto_stage":           "Tự Động Stage",
		"toggle_auto_stage":    "Bật/Tắt Tự Động Stage",
		"enabled":              "Bật",
		"disabled":             "Tắt",
		"select_option":        "Chọn một tùy chọn",
		"invalid_option":       "❌ Tùy chọn không hợp lệ. Vui lòng thử lại.",
		"save_exit":            "💾 Đã lưu cấu hình thành công!",
		"reset_confirm":        "⚠️  Điều này sẽ đặt lại tất cả cài đặt về mặc định. Tiếp tục?",
		"reset_success":        "🔄 Đã đặt lại cài đặt thành công!",
		"uninstall_confirm":    "⚠️  Điều này sẽ gỡ bỏ hoàn toàn dev_tool. Tiếp tục?",
		"uninstall_success":    "✅ Đã gỡ cài đặt dev_tool thành công!",
		"back_to_menu":         "⬅️  Quay lại menu",
		"exit":                 "Thoát",
		"account_manager":      "Quản Lý Tài Khoản",
		"add_account":          "Thêm Tài Khoản",
		"edit_account":         "Sửa Tài Khoản",
		"delete_account":       "Xóa Tài Khoản",
		"set_primary":          "Đặt làm Chính",
		"no_accounts":          "Chưa có tài khoản nào",
		"account_email":        "Email",
		"account_model":        "🤖 Model",
		"account_status":       "🔑 Trạng Thái",
		"primary":              "⭐ Chính",
		"secondary":            "🔑 Phụ",
		"help_text":            "🛠️  Dev Tool - Trợ Lý Git AI\n============================\n\n📚 Lệnh Có Sẵn:\n  dev_tool              Tạo commit message AI và commit\n  dev_tool --no-push    Commit mà không push lên remote\n  dev_tool settings     Mở menu cài đặt\n  dev_tool --version    Hiển thị thông tin phiên bản\n\n⚙️  Tùy Chọn Menu Cài Đặt:\n  Chỉnh Sửa Cấu Hình    Thay đổi ngôn ngữ, model, và preferences\n  Quản Lý Tài Khoản     Quản lý nhiều tài khoản Gemini\n  Đặt Lại Mặc Định      Đặt lại tất cả cài đặt về trạng thái ban đầu\n  Gỡ Cài Đặt Tool       Gỡ bỏ hoàn toàn dev_tool\n\n🎨 Phong Cách Commit:\n  Conventional          feat: thêm xác thực người dùng\n  Emoji                 ✨ thêm xác thực người dùng\n  Descriptive           Thêm hệ thống xác thực người dùng toàn diện\n\n🌍 Ngôn Ngữ Hỗ Trợ:\n  Giao diện: Tiếng Anh, Tiếng Việt\n  Commit: Tiếng Anh, Tiếng Việt\n\n🤖 Model Hỗ Trợ:\n  Gemini 2.5 Pro        Model tiên tiến nhất (khuyên dùng)\n  Gemini 2.5 Flash      Nhanh và mạnh mẽ\n  Gemini 2.5 Flash-Lite Nhẹ và hiệu quả\n  Gemini 2.0 Flash      Model cũ\n\n📖 Để biết thêm: https://github.com/your-repo/dev_tool",
		"edit_config":          "Chỉnh Sửa Cấu Hình",
		"reset_defaults":       "Đặt Lại Mặc Định",
		"uninstall_tool":       "Gỡ Cài Đặt Tool",
		"help_info":            "Trợ Giúp & Thông Tin",
		"options":              "Tùy Chọn",
		"change_ui_lang":       "Thay Đổi Ngôn Ngữ Giao Diện",
		"change_commit_lang":   "Thay Đổi Ngôn Ngữ Commit",
		"update_api_key":       "Cập Nhật API Key",
		"change_ai_model":      "Thay Đổi Model AI",
		"change_commit_style":  "Thay Đổi Phong Cách Commit",
		"toggle_auto_push":     "Bật/Tắt Tự Động Push",
		"save_back":            "Lưu & Quay Lại Menu",
		"back_no_save":         "Quay Lại Không Lưu",
		"edit_options":         "Tùy Chọn Chỉnh Sửa",
		"available_langs":      "Ngôn Ngữ Có Sẵn",
		"select_lang":          "Chọn ngôn ngữ",
		"enter_api_key_prompt": "Nhập API key mới",
		"available_models":     "Model Có Sẵn",
		"select_model":         "Chọn model",
		"available_styles":     "Phong Cách Có Sẵn",
		"select_style":         "Chọn phong cách",
		"confirm_toggle":       "Bạn có muốn",
		"enable":               "bật",
		"disable":              "tắt",
		"press_enter_continue": "Nhấn Enter để tiếp tục",
		"type_yes_confirm":     "Gõ 'yes' để xác nhận:",
		"is_currently":         "hiện đang",
		// New account management messages
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
	},
}

func GetMessage(key string, cfg config.Config) string {
	lang := cfg.UILanguage
	if lang == "" {
		lang = "en"
	}

	if msg, ok := Messages[lang][key]; ok {
		return msg
	}

	// Fallback to English
	if msg, ok := Messages["en"][key]; ok {
		return msg
	}

	return key
}

func PrintHeader(text string, colorName string) {
	c := Colors[colorName]
	if c == nil {
		c = Colors["CYAN"]
	}

	width := max(len(text)+4, 50)
	border := strings.Repeat("=", width)

	c.Println("\n" + border)
	c.Println(CenterText(text, width))
	c.Println(border)
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
	Colors["CYAN"].Add(color.Bold).Println(banner)
}

func ShowMenuDivider() {
	Colors["DIM"].Println(strings.Repeat("-", 50))
}
