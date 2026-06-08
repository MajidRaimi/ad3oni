import 'package:flutter/foundation.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../models/prayer_category.dart';
import '../models/prayer_group.dart';
import '../models/prayer_type.dart';
import '../providers.dart';
import '../repositories/taxonomy_repository.dart';

/// Exposes the app-wide [TaxonomyController], kicking off its load on creation.
final taxonomyControllerProvider = ChangeNotifierProvider<TaxonomyController>(
  (ref) => TaxonomyController(repository: ref.watch(taxonomyRepositoryProvider))
    ..load(),
);

/// Loads and caches the reference taxonomy (groups, categories, types) from the
/// API and exposes lookups used by the filter chips and the Add form.
class TaxonomyController extends ChangeNotifier {
  TaxonomyController({TaxonomyRepository? repository})
      : _repo = repository ?? TaxonomyRepository();

  final TaxonomyRepository _repo;

  List<PrayerGroup> groups = const [];
  List<PrayerType> types = const [];
  List<PrayerCategory> categories = const [];

  bool _loaded = false;
  bool get loaded => _loaded;

  Future<void> load() async {
    try {
      final results = await Future.wait([
        _repo.groups(),
        _repo.types(),
        _repo.categories(),
      ]);
      groups = results[0] as List<PrayerGroup>;
      types = results[1] as List<PrayerType>;
      categories = results[2] as List<PrayerCategory>;
    } catch (_) {
      // Leave whatever we have; the UI degrades to empty chips offline.
    }
    _loaded = true;
    notifyListeners();
  }

  /// Categories belonging to a group, matched by the group's slug.
  List<PrayerCategory> categoriesForGroup(String groupSlug) =>
      categories.where((c) => c.groupSlug == groupSlug).toList();
}
