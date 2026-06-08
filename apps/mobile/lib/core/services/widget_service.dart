import 'dart:convert';

import 'package:flutter/foundation.dart';
import 'package:home_widget/home_widget.dart';

import '../models/prayer.dart';

/// Bridges the app to the native iOS home-screen / lock-screen widgets.
///
/// It writes the freshest content into the shared App Group store and asks
/// WidgetKit to reload the timelines. The widget extension reads the same keys
/// from `UserDefaults(suiteName: WidgetService.appGroupId)`.
///
/// Two widget kinds are fed:
///  • [_dailyWidgetKind]  — "دعاء اليوم" (today's du'a)
///  • [_randomWidgetKind] — "عشوائي" (random from the cached/saved pool, offline)
class WidgetService {
  WidgetService._();

  /// Must match the App Group id on both the Runner and widget-extension
  /// targets (see ios/Runner/Runner.entitlements + ios/Ad3oniWidget).
  static const appGroupId = 'group.com.ad3oni.ad3oni';

  // These match the SwiftUI `kind` strings in the widget extension.
  static const _dailyWidgetKind = 'Ad3oniDailyWidget';
  static const _randomWidgetKind = 'Ad3oniRandomWidget';

  // Shared keys (kept in one place; mirrored in Swift `SharedKeys`).
  static const _kDailyText = 'daily_text';
  static const _kDailyCategory = 'daily_category';
  static const _kDailyType = 'daily_type';
  static const _kPool = 'pool_json';
  static const _kRandomInterval = 'random_interval_minutes';

  static bool get _supported =>
      !kIsWeb && defaultTargetPlatform == TargetPlatform.iOS;

  static bool _initialized = false;

  static Future<void> ensureInitialized() async {
    if (_initialized || !_supported) return;
    await HomeWidget.setAppGroupId(appGroupId);
    _initialized = true;
  }

  /// Pushes [daily] and a [pool] of cached du'as into the shared store and
  /// reloads both widget timelines. Best-effort: any failure is swallowed so a
  /// widget hiccup can never break the app.
  static Future<void> sync({
    required Prayer? daily,
    required List<Prayer> pool,
  }) async {
    if (!_supported) return;
    try {
      await ensureInitialized();

      Map<String, String> encode(Prayer p) => {
            'text': p.text,
            'category': p.categoryName,
            'type': p.typeName,
          };

      if (daily != null) {
        final d = encode(daily);
        await HomeWidget.saveWidgetData<String>(_kDailyText, d['text']);
        await HomeWidget.saveWidgetData<String>(_kDailyCategory, d['category']);
        await HomeWidget.saveWidgetData<String>(_kDailyType, d['type']);
      }

      // De-dupe by text and cap the pool so the shared store stays small;
      // the widget rotates through whatever it finds.
      final seen = <String>{};
      final unique = pool.where((p) => seen.add(p.text)).take(25);
      final poolJson = jsonEncode(unique.map(encode).toList());
      await HomeWidget.saveWidgetData<String>(_kPool, poolJson);

      await HomeWidget.updateWidget(iOSName: _dailyWidgetKind);
      await HomeWidget.updateWidget(iOSName: _randomWidgetKind);
    } catch (_) {
      // Widgets are a nicety, never a hard dependency.
    }
  }

  /// Stores how often (in minutes) the random widget should rotate to a new
  /// du'a, then reloads its timeline so the new cadence takes effect.
  static Future<void> setRandomInterval(int minutes) async {
    if (!_supported) return;
    try {
      await ensureInitialized();
      await HomeWidget.saveWidgetData<int>(_kRandomInterval, minutes);
      await HomeWidget.updateWidget(iOSName: _randomWidgetKind);
    } catch (_) {
      // Widgets are a nicety, never a hard dependency.
    }
  }
}
