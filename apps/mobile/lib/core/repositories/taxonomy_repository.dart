import '../error/failure.dart';
import '../models/prayer_category.dart';
import '../models/prayer_group.dart';
import '../models/prayer_type.dart';
import '../network/api_client.dart';

/// Fetches the reference taxonomy from the API: groups, categories, types.
class TaxonomyRepository {
  TaxonomyRepository({ApiClient? client}) : _api = client ?? ApiClient.instance;

  final ApiClient _api;

  /// Maps any thrown exception to a typed [Failure] (CLAUDE.md §7).
  Future<T> _guard<T>(Future<T> Function() body) async {
    try {
      return await body();
    } catch (e) {
      throw failureFrom(e);
    }
  }

  Future<List<PrayerGroup>> groups() => _guard(() async {
        final list = await _api.getList('/v1/groups');
        return list
            .map((e) => PrayerGroup.fromJson(e as Map<String, dynamic>))
            .toList();
      });

  Future<List<PrayerType>> types() => _guard(() async {
        final list = await _api.getList('/v1/types');
        return list
            .map((e) => PrayerType.fromJson(e as Map<String, dynamic>))
            .toList();
      });

  Future<List<PrayerCategory>> categories({String? groupSlug}) =>
      _guard(() async {
        final list =
            await _api.getList('/v1/categories', query: {'group': groupSlug});
        return list
            .map((e) => PrayerCategory.fromJson(e as Map<String, dynamic>))
            .toList();
      });
}
