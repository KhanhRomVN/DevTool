package ai

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"strings"
)

type GeminiRequest struct {
	Contents []Content `json:"contents"`
}

type Content struct {
	Parts []Part `json:"parts"`
}

type Part struct {
	Text string `json:"text"`
}

type GeminiResponse struct {
	Candidates []Candidate `json:"candidates"`
}

type Candidate struct {
	Content Content `json:"content"`
}

func GenerateCommitMessage(diffText string, apiKey string, model string, commitStyle string, commitLanguage string) (string, error) {
	if apiKey == "" {
		return "", fmt.Errorf("API key not configured")
	}

	prompt := GetCommitPrompt(commitStyle, commitLanguage, diffText)

	requestBody := GeminiRequest{
		Contents: []Content{
			{
				Parts: []Part{
					{Text: prompt},
				},
			},
		},
	}

	jsonData, err := json.Marshal(requestBody)
	if err != nil {
		return "", err
	}

	url := fmt.Sprintf("https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent?key=%s", model, apiKey)
	req, err := http.NewRequest("POST", url, bytes.NewBuffer(jsonData))
	if err != nil {
		return "", err
	}

	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return "", fmt.Errorf("API request failed with status: %s", resp.Status)
	}

	var geminiResponse GeminiResponse
	if err := json.NewDecoder(resp.Body).Decode(&geminiResponse); err != nil {
		return "", err
	}

	if len(geminiResponse.Candidates) == 0 || len(geminiResponse.Candidates[0].Content.Parts) == 0 {
		return "", fmt.Errorf("no response from AI")
	}

	message := geminiResponse.Candidates[0].Content.Parts[0].Text
	return FormatCommitMessage(message, commitStyle), nil
}

func GetCommitPrompt(commitStyle string, commitLanguage string, diffText string) string {
	commitTypes := map[string]map[string]string{
		"en": {
			"feat":      "New feature",
			"fix":       "Bug fix",
			"docs":      "Documentation",
			"style":     "Code style/formatting",
			"refactor":  "Code refactoring",
			"perf":      "Performance improvement",
			"test":      "Testing",
			"chore":     "Maintenance tasks",
			"ci":        "CI/CD configuration",
			"build":     "Build system",
			"revert":    "Revert changes",
			"security":  "Security related",
			"config":    "Configuration changes",
			"database":  "Database changes",
			"ui":        "User interface changes",
			"i18n":      "Internationalization",
			"access":    "Accessibility",
			"analytics": "Analytics tracking",
			"deprecate": "Deprecation notices",
		},
		"vi": {
			"feat":      "Tính năng mới",
			"fix":       "Sửa lỗi",
			"docs":      "Tài liệu",
			"style":     "Định dạng/kiểu code",
			"refactor":  "Tái cấu trúc code",
			"perf":      "Cải thiện hiệu năng",
			"test":      "Kiểm thử",
			"chore":     "Công việc bảo trì",
			"ci":        "Cấu hình CI/CD",
			"build":     "Hệ thống build",
			"revert":    "Hoàn tác thay đổi",
			"security":  "Liên quan bảo mật",
			"config":    "Thay đổi cấu hình",
			"database":  "Thay đổi database",
			"ui":        "Thay đổi giao diện",
			"i18n":      "Quốc tế hóa",
			"access":    "Khả năng truy cập",
			"analytics": "Theo dõi phân tích",
			"deprecate": "Thông báo không dùng nữa",
		},
	}

	langInstructions := map[string]map[string]string{
		"en": {
			"conventional": fmt.Sprintf(`
Generate a conventional commit message in English following these rules:
1. Format: type(scope): description
2. Types: %s
3. Keep title under 72 characters
4. Use imperative mood (add, fix, update, not added, fixed, updated)
5. Add 3-5 bullet points with specific details
6. No markdown formatting, keep plain text

Example format:
feat(auth): add user authentication system
- Implement login/logout functionality with JWT tokens
- Add password encryption using bcrypt with 12 rounds
- Create user session management with Redis storage
- Add email verification for new registrations
- Implement rate limiting on authentication endpoints
`, getTypeList(commitTypes["en"])),
			"emoji": fmt.Sprintf(`
Generate an emoji-style commit message in English following these rules:
1. Format: emoji description (no type prefix)
2. Use appropriate emoji for the change type:
   ✨ feat | 🐛 fix | 📚 docs | 💎 style | ♻️ refactor | ⚡ perf | 🧪 test | 🔧 chore | 👷 ci | 📦 build | ⏪ revert | 🔒 security | ⚙️ config | 🗄️ database | 🎨 ui | 🌐 i18n | ♿ access | 📊 analytics | 🗑️ deprecate
3. Keep title under 72 characters
4. Use imperative mood
5. Add 3-5 bullet points with specific details

Example format:
✨ add user authentication system
- Implement login/logout functionality with JWT tokens
- Add password encryption using bcrypt with 12 rounds  
- Create user session management with Redis storage
- Add email verification for new registrations
- Implement rate limiting on authentication endpoints
`),
			"descriptive": `
Generate a descriptive commit message in English following these rules:
1. Write a clear, descriptive title (no prefixes or emojis)
2. Capitalize first letter, no period at end
3. Keep title under 72 characters
4. Use imperative mood
5. Add 3-5 bullet points with specific details
6. Focus on what and why, not how

Example format:
Add comprehensive user authentication system with security enhancements
- Implement secure login and logout functionality using JWT tokens
- Include password encryption with bcrypt using 12 rounds for security
- Provide session management with Redis for scalability
- Add email verification process for new user registrations
- Implement rate limiting to prevent brute force attacks
`,
		},
		"vi": {
			"conventional": fmt.Sprintf(`
Tạo commit message theo quy ước conventional commits bằng tiếng Việt:
1. Định dạng: type(scope): mô tả
2. Types: %s
3. Giữ tiêu đề dưới 72 ký tự
4. Sử dụng thể mệnh lệnh (thêm, sửa, cập nhật)
5. Thêm 3-5 điểm chi tiết cụ thể
6. Không sử dụng markdown, giữ văn bản thuần

Ví dụ định dạng:
feat(auth): thêm hệ thống xác thực người dùng
- Triển khai chức năng đăng nhập/đăng xuất với JWT tokens
- Thêm mã hóa mật khẩu bằng bcrypt với 12 rounds
- Tạo quản lý phiên người dùng với Redis storage
- Thêm xác thực email cho đăng ký mới
- Triển khai rate limiting trên endpoints xác thực
`, getTypeList(commitTypes["vi"])),
			"emoji": fmt.Sprintf(`
Tạo commit message theo phong cách emoji bằng tiếng Việt:
1. Định dạng: emoji mô tả (không có tiền tố type)
2. Sử dụng emoji phù hợp:
   ✨ feat | 🐛 fix | 📚 docs | 💎 style | ♻️ refactor | ⚡ perf | 🧪 test | 🔧 chore | 👷 ci | 📦 build | ⏪ revert | 🔒 security | ⚙️ config | 🗄️ database | 🎨 ui | 🌐 i18n | ♿ access | 📊 analytics | 🗑️ deprecate
3. Giữ tiêu đề dưới 72 ký tự
4. Sử dụng thể mệnh lệnh
5. Thêm 3-5 điểm chi tiết cụ thể

Ví dụ định dạng:
✨ thêm hệ thống xác thực người dùng
- Triển khai chức năng đăng nhập/đăng xuất với JWT tokens
- Thêm mã hóa mật khẩu bằng bcrypt với 12 rounds
- Tạo quản lý phiên người dùng với Redis storage
- Thêm xác thực email cho đăng ký mới
- Triển khai rate limiting trên endpoints xác thực
`),
			"descriptive": `
Tạo commit message mô tả chi tiết bằng tiếng Việt:
1. Viết tiêu đề rõ ràng, mô tả (không có tiền tố hay emoji)
2. Viết hoa chữ cái đầu, không có dấu chấm cuối
3. Giữ tiêu đề dưới 72 ký tự  
4. Sử dụng thể mệnh lệnh
5. Thêm 3-5 điểm chi tiết cụ thể
6. Tập trung vào cái gì và tại sao, không phải cách thực hiện

Ví dụ định dạng:
Thêm hệ thống xác thực người dùng toàn diện với các cải tiến bảo mật
- Triển khai chức năng đăng nhập và đăng xuất bảo mật sử dụng JWT tokens
- Bao gồm mã hóa mật khẩu với bcrypt sử dụng 12 rounds cho bảo mật
- Cung cấp quản lý phiên với Redis để mở rộng
- Thêm quy trình xác thực email cho đăng ký người dùng mới
- Triển khai rate limiting để ngăn chặn tấn công brute force
`,
		},
	}

	template := langInstructions[commitLanguage][commitStyle]
	return fmt.Sprintf("%s\n\nNow analyze the following git diff and generate a commit message:\n\n%s", template, diffText)
}

func getTypeList(types map[string]string) string {
	keys := make([]string, 0, len(types))
	for k := range types {
		keys = append(keys, k)
	}
	return strings.Join(keys, ", ")
}

func FormatCommitMessage(message string, commitStyle string) string {
	lines := strings.Split(strings.TrimSpace(message), "\n")
	if len(lines) == 0 {
		return message
	}

	// Clean up any unwanted markdown or formatting
	cleanedLines := make([]string, 0)
	for _, line := range lines {
		// Remove markdown formatting
		line = strings.ReplaceAll(line, "**", "")
		line = strings.ReplaceAll(line, "*", "")
		line = strings.ReplaceAll(line, "`", "")
		// Remove extra spaces
		line = strings.Join(strings.Fields(line), " ")
		if line != "" {
			cleanedLines = append(cleanedLines, line)
		}
	}

	// Ensure the first line meets length requirements
	if len(cleanedLines) > 0 && len(cleanedLines[0]) > 72 {
		title := cleanedLines[0]
		if strings.Contains(title, ": ") {
			parts := strings.SplitN(title, ": ", 2)
			if len(parts) == 2 && len(parts[1]) > 50 {
				cleanedLines[0] = fmt.Sprintf("%s: %s...", parts[0], parts[1][:47])
			}
		} else if len(title) > 69 {
			cleanedLines[0] = title[:69] + "..."
		}
	}

	return strings.Join(cleanedLines, "\n")
}
