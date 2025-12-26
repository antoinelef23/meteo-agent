# Security Guidelines

## Before Pushing to Git

This project is now **SAFE TO PUSH** to git repositories, as long as you follow these guidelines:

### ✅ What's Protected

- `.env` file is properly listed in `.gitignore`
- `.env.example` provides template without secrets
- All sensitive credentials are excluded from version control
- Google Cloud credentials and service account keys are properly ignored

### 🔐 Required Environment Variables

Copy `.env.example` to `.env` and fill in your actual credentials:

```bash
cp .env.example .env
```

Then edit `.env` with your real values:

- `GOOGLE_API_KEY`: Your Google Gemini API key ([generate here](https://makersuite.google.com/app/apikey))
- `WEATHERAPI_KEY`: Your WeatherAPI.com API key ([get free key here](https://www.weatherapi.com/my/))
- `DEFAULT_CITY`: Optional default city for weather queries
- `DEFAULT_COUNTRY_CODE`: Optional country code (e.g., FR, US, UK)
- `GOOGLE_CLOUD_PROJECT`: Your Google Cloud project ID (for Agent Engine deployment)
- `AGENT_ENGINE_REGION`: Google Cloud region (e.g., europe-west1)

### ⚠️ Important Security Notes

1. **NEVER commit the `.env` file** - it contains real secrets
2. **NEVER commit Google Cloud credentials** - service account keys should stay local or use ADC
3. **Rotate credentials regularly** as a security best practice
4. **Use least-privilege access** - only grant necessary API permissions
5. **Monitor API usage** - check for unauthorized access regularly

### 🔍 Pre-Push Checklist

Before pushing to any git repository, verify:

- [ ] `.env` file is NOT staged for commit
- [ ] No hardcoded API keys in source code
- [ ] No service account JSON files in the repository
- [ ] `.gitignore` includes `.env` and credential patterns
- [ ] All secrets are loaded from environment variables

### 🚨 If Credentials Are Exposed

If you accidentally commit secrets:

1. **Immediately revoke all exposed credentials**:
   - Gemini API keys: https://makersuite.google.com/app/apikey
   - WeatherAPI keys: https://www.weatherapi.com/my/
   - Google Cloud service accounts: https://console.cloud.google.com/iam-admin/serviceaccounts

2. **Remove secrets from git history**:
   ```bash
   # Use BFG Repo-Cleaner or git-filter-repo
   git filter-repo --path .env --invert-paths
   ```

3. **Generate new credentials** with fresh values

4. **Force push the cleaned repository** (coordinate with team first!)

### 📋 Recommended Tools

Consider using these tools to prevent credential leaks:

- [git-secrets](https://github.com/awslabs/git-secrets) - Prevents committing secrets
- [gitleaks](https://github.com/gitleaks/gitleaks) - Scans for hardcoded secrets
- [trufflehog](https://github.com/trufflesecurity/trufflehog) - Find secrets in git history
- [pre-commit](https://pre-commit.com/) - Git hooks for security checks

### 🛡️ Best Practices

1. **Use Application Default Credentials (ADC)** for Google Cloud authentication in production
2. **Implement secret rotation** - change credentials periodically
3. **Enable API key restrictions** - limit keys to specific APIs and origins
4. **Audit API usage logs** regularly for suspicious activity
5. **Use secret management tools** (e.g., Google Secret Manager) for production deployments

### 🌐 API Key Security

#### Gemini API Key
- Restrict to specific APIs in Google Cloud Console
- Set usage quotas to prevent abuse
- Monitor usage in the API dashboard

#### WeatherAPI Key
- Use the free tier for development
- Upgrade to paid plan with usage limits for production
- Monitor daily API call limits

---

**Status**: ✅ This project is configured securely and safe to push to git repositories.

**Last Updated**: 2025-12-19
