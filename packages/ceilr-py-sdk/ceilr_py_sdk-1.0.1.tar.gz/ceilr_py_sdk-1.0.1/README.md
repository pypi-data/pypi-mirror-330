# CeilR Python SDK

🚀 **CeilR SDK** is a Python library for feature access management, usage tracking, and entitlement fetching.

## 📦 Installation

Install the package in your Python environment:

```sh
pip install ceilr-py-sdk
```

## 🛠️ Setup

Initialize the SDK:

```python
from ceilr import CeilR

ceilr = CeilR("your-api-key", "customer-id")
```

## 🚀 Features

### ✅ **Check Feature Access**
```python
has_access = ceilr.check_feature("premium_feature")
print("Feature Access:", has_access)
```

### 📊 **Track Usage**
```python
ceilr.track_usage("api_calls", 1)
```

### 🔑 **Get User Entitlements**
```python
entitlements = ceilr.get_user_entitlements()
print("User Entitlements:", entitlements)
```

## 📡 Offline Support
- Requests are **queued when offline** and retried when the device is back online.

## 🛠 Configuration

You can set custom API endpoints if needed:

```python
ceilr.BASE_URL = "https://custom-api-url.com"
```

## 🔄 Updating the SDK
To update to the latest version:

```sh
pip install --upgrade ceilr-py-sdk
```

## 🤝 Contributing
1. Fork the repo
2. Create a feature branch (`git checkout -b feature-name`)
3. Commit changes (`git commit -m "Add new feature"`)
4. Push to GitHub (`git push origin feature-name`)
5. Open a Pull Request 🚀

## 📜 License
This project is licensed under the **MIT License**.

## 📞 Support
For any issues or questions, reach out via:
- **GitHub Issues**: [https://github.com/GouniManikumar12/ceilr-py-sdk/issues](https://github.com/GouniManikumar12/ceilr-py-sdk/issues)
- **Email**: support@ceilr.com

