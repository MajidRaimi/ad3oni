import 'package:flutter/foundation.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../../../core/providers.dart';
import '../../../core/services/widget_service.dart';

/// Exposes the app-wide [SettingsController]; pushes the stored interval to the
/// iOS widget on creation so a fresh install stays in sync.
final settingsControllerProvider = ChangeNotifierProvider<SettingsController>(
  (ref) => SettingsController(ref.watch(sharedPreferencesProvider))
    ..syncToWidget(),
);

/// A selectable rotation interval for the random ("عشوائي") widget.
class IntervalOption {
  const IntervalOption(this.minutes, this.label);
  final int minutes;
  final String label;
}

/// App settings the user can tune. Currently the rotation interval of the
/// random home-screen widget — persisted locally *and* mirrored into the
/// shared App Group so the iOS widget extension reads the same value.
class SettingsController extends ChangeNotifier {
  SettingsController(this._prefs) {
    _randomIntervalMinutes =
        _prefs.getInt(_key) ?? defaultRandomIntervalMinutes;
  }

  static const _key = 'ad3oni.random_interval_minutes';

  /// Default matches the previous hard-coded widget behaviour (every 2 hours).
  static const int defaultRandomIntervalMinutes = 120;

  /// The intervals offered in the UI (value in minutes).
  static const List<IntervalOption> intervalOptions = [
    IntervalOption(15, 'كل ١٥ دقيقة'),
    IntervalOption(30, 'كل ٣٠ دقيقة'),
    IntervalOption(60, 'كل ساعة'),
    IntervalOption(120, 'كل ساعتين'),
    IntervalOption(360, 'كل ٦ ساعات'),
    IntervalOption(1440, 'مرة في اليوم'),
  ];

  final SharedPreferences _prefs;
  int _randomIntervalMinutes = defaultRandomIntervalMinutes;

  int get randomIntervalMinutes => _randomIntervalMinutes;

  Future<void> setRandomInterval(int minutes) async {
    if (minutes == _randomIntervalMinutes) return;
    _randomIntervalMinutes = minutes;
    notifyListeners();
    await _prefs.setInt(_key, minutes);
    await WidgetService.setRandomInterval(minutes);
  }

  /// Push the stored value to the widget on startup so a fresh install /
  /// reinstall (where the App Group store is empty) stays in sync.
  Future<void> syncToWidget() =>
      WidgetService.setRandomInterval(_randomIntervalMinutes);
}
