<?php
session_start();

$USERNAME = 'admin';
$PASSWORD = 'password123'; // Mock only; don't use a plaintext password in production.

if (empty($_SESSION['csrf_token'])) {
    $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
}

$loggedIn = false;
$message = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $submittedToken = $_POST['csrf_token'] ?? '';

    if (!is_string($submittedToken) ||
        !hash_equals($_SESSION['csrf_token'], $submittedToken)) {
        http_response_code(403);
        $message = 'Invalid CSRF token.';
    } elseif (
        ($_POST['username'] ?? '') === $USERNAME &&
        ($_POST['password'] ?? '') === $PASSWORD
    ) {
        $message = "Login successful";
        $loggedIn = true;
        // In a real app, set an authenticated session here.
    } else {
        $message = 'Invalid username or password.';
    }
}

function e(string $value): string
{
    return htmlspecialchars($value, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}
?>

<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Mock login</title>
</head>
<body>
  <?php if (!empty($message)): ?>
    <p><?= e($message) ?></p>
  <?php endif; ?>

  <?php if (!$loggedIn): ?>
    <form method="post">
      <input
        type="hidden"
        name="csrf_token"
        value="<?= e($_SESSION['csrf_token']) ?>"
      >

      <label>
        Username
        <input name="username" required>
      </label>

      <label>
        Password
        <input type="password" name="password" required>
      </label>

      <button type="submit">Log in</button>
    </form>
  <?php endif; ?>
</body>
</html>
