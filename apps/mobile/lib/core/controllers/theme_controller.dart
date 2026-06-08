import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../providers.dart';

/// Exposes the [ThemeController] to the widget tree.
final themeControllerProvider = ChangeNotifierProvider<ThemeController>(
  (ref) => ThemeController(ref.watch(sharedPreferencesProvider)),
);

/// Holds the app [ThemeMode] and persists the user's choice.
class ThemeController extends ChangeNotifier {
  ThemeController(this._prefs) {
    _mode = _decode(_prefs.getString(_key));
  }

  static const _key = 'ad3oni.theme_mode';
  final SharedPreferences _prefs;
  ThemeMode _mode = ThemeMode.system;

  ThemeMode get mode => _mode;

  bool isDark(BuildContext context) => switch (_mode) {
        ThemeMode.dark => true,
        ThemeMode.light => false,
        ThemeMode.system =>
          MediaQuery.platformBrightnessOf(context) == Brightness.dark,
      };

  /// Toggle between light and dark based on the currently effective mode.
  Future<void> toggle(BuildContext context) async {
    await setMode(isDark(context) ? ThemeMode.light : ThemeMode.dark);
  }

  Future<void> setMode(ThemeMode mode) async {
    if (mode == _mode) return;
    _mode = mode;
    notifyListeners();
    await _prefs.setString(_key, mode.name);
  }

  ThemeMode _decode(String? raw) => switch (raw) {
        'light' => ThemeMode.light,
        'dark' => ThemeMode.dark,
        _ => ThemeMode.system,
      };
}
