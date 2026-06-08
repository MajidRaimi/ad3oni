import 'dart:convert';

import 'package:flutter/foundation.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../models/prayer.dart';
import '../providers.dart';

/// Exposes the app-wide [SavedController] to the widget tree.
final savedControllerProvider = ChangeNotifierProvider<SavedController>(
  (ref) => SavedController(ref.watch(sharedPreferencesProvider)),
);

/// Holds the user's saved du'as, cached locally so they work fully offline.
///
/// Shared app-wide (the home cards and the saved screen both reflect it).
class SavedController extends ChangeNotifier {
  SavedController(this._prefs) {
    _load();
  }

  static const _key = 'ad3oni.saved_prayers';
  final SharedPreferences _prefs;

  final List<Prayer> _items = [];
  final Set<String> _ids = {};

  List<Prayer> get items => List.unmodifiable(_items.reversed);
  bool get isEmpty => _items.isEmpty;
  bool isSaved(String id) => _ids.contains(id);

  void _load() {
    final raw = _prefs.getStringList(_key) ?? const [];
    for (final entry in raw) {
      try {
        final prayer =
            Prayer.fromJson(jsonDecode(entry) as Map<String, dynamic>);
        _items.add(prayer);
        _ids.add(prayer.id);
      } catch (_) {
        // skip malformed cache entries
      }
    }
  }

  Future<void> toggle(Prayer prayer) async {
    if (_ids.remove(prayer.id)) {
      _items.removeWhere((p) => p.id == prayer.id);
    } else {
      _items.add(prayer);
      _ids.add(prayer.id);
    }
    notifyListeners();
    await _persist();
  }

  Future<void> _persist() async {
    await _prefs.setStringList(
      _key,
      _items.map((p) => jsonEncode(p.toJson())).toList(),
    );
  }
}
