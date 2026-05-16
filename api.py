<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GrimPot Login</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .login-card {
            background: rgba(20, 20, 40, 0.95);
            border-radius: 20px;
            padding: 40px;
            width: 100%;
            max-width: 450px;
            border: 1px solid #2a2a4a;
        }
        .login-card h1 {
            color: #00aaff;
            text-align: center;
            margin-bottom: 10px;
        }
        .login-card .subtitle {
            color: #aaa;
            text-align: center;
            margin-bottom: 30px;
            font-size: 14px;
        }
        .form-control {
            background: #1a1a2e;
            border: 1px solid #2a2a4a;
            color: white;
            padding: 12px;
        }
        .form-control:focus {
            background: #1a1a2e;
            color: white;
            border-color: #00aaff;
            box-shadow: none;
        }
        .btn-primary {
            background: #00aaff;
            border: none;
            width: 100%;
            padding: 12px;
            font-weight: bold;
        }
        .btn-primary:hover {
            background: #0088cc;
        }
        .error {
            color: #ff4444;
            text-align: center;
            margin-top: 15px;
        }
        .loading {
            color: #00aaff;
            text-align: center;
            margin-top: 15px;
            display: none;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="login-card">
            <h1><i class="bi bi-shield-lock"></i> GrimPot</h1>
            <div class="subtitle">Script Licensing & Key Management Platform</div>
            <form id="loginForm">
                <div class="mb-3">
                    <input type="password" class="form-control" id="apiKey" placeholder="Enter your 52-character API key" required maxlength="52">
                </div>
                <button type="submit" class="btn btn-primary">Login to Dashboard</button>
            </form>
            <div id="errorMsg" class="error"></div>
            <div id="loadingMsg" class="loading">Validating...</div>
        </div>
    </div>

    <script>
        const VALID_API_KEYS = [
            "aB3kL9mN2pQ4rS5tU6vW7xY8zA1bC2dE3fG4hJ5kL6nP7qR8sT9uV0wX",
            "XyZ123AbC456DeF789GhI0JkL1MnOp2QrSt3UvWx4YzA5BcD6EfG7HiJ8KlM9",
            "7kL2mNpQ4rS5tU6vW7xY8zA1bC2dE3fG4hJ5kL6nP7qR8sT9uV0wXyZ1Ab"
        ];

        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const apiKey = document.getElementById('apiKey').value.trim();
            
            if (apiKey.length !== 52) {
                document.getElementById('errorMsg').innerText = 'API key must be exactly 52 characters';
                return;
            }
            
            document.getElementById('loadingMsg').style.display = 'block';
            document.getElementById('errorMsg').innerText = '';
            
            setTimeout(() => {
                if (VALID_API_KEYS.includes(apiKey)) {
                    sessionStorage.setItem('grimpot_auth', 'true');
                    sessionStorage.setItem('grimpot_api_key', apiKey);
                    window.location.href = 'dashboard.html';
                } else {
                    document.getElementById('errorMsg').innerText = 'Invalid API key';
                }
                document.getElementById('loadingMsg').style.display = 'none';
            }, 500);
        });
    </script>
</body>
</html>
