/// App-wide configuration constants.
class AppConfig {
  AppConfig._();

  /// Base URL of the Ad3oni API (FastAPI layer in front of PocketBase).
  /// Public, anonymous access — no auth/registration.
  static const String apiBaseUrl = 'https://api.ad3oni.com';
}
