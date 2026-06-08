import '../error/failure.dart';
import '../models/prayer.dart';
import '../network/api_client.dart';

/// One page of du'as plus the paging metadata from `Page[Prayer]`, so callers
/// can tell whether more pages remain and show the true total.
class PrayerPage {
  const PrayerPage({
    required this.items,
    required this.page,
    required this.totalItems,
    required this.totalPages,
  });

  final List<Prayer> items;
  final int page;
  final int totalItems;
  final int totalPages;

  bool get hasMore => page < totalPages;
}

/// Read/write access to du'as via the Ad3oni API (`/v1/prayers`).
///
/// Shared across features (home, search, add) since they all operate on the
/// same du'a entity. Filtering uses taxonomy *slugs*.
class PrayersRepository {
  PrayersRepository({ApiClient? client}) : _api = client ?? ApiClient.instance;

  final ApiClient _api;

  /// Runs [body], translating any thrown exception into a typed [Failure] so a
  /// raw exception never escapes the data layer (CLAUDE.md §7).
  Future<T> _guard<T>(Future<T> Function() body) async {
    try {
      return await body();
    } catch (e) {
      throw failureFrom(e);
    }
  }

  /// The featured "دعاء اليوم", chosen server-side by the `/v1/daily` endpoint
  /// (stable for the day, same for everyone). Falls back to the newest du'a if
  /// the dedicated endpoint is unavailable.
  Future<Prayer?> daily() => _guard(() async {
        try {
          final res = await _api.getJson('/v1/daily');
          if (res.isEmpty || res['id'] == null) return null;
          return Prayer.fromJson(res);
        } catch (_) {
          final res = await _api.getJson('/v1/prayers',
              query: {'page': '1', 'perPage': '1', 'sort': '-created'});
          final items = (res['items'] as List?) ?? const [];
          if (items.isEmpty) return null;
          return Prayer.fromJson(items.first as Map<String, dynamic>);
        }
      });

  /// Random du'as drawn from the whole confirmed library (client-side shuffle),
  /// de-duped and excluding [excludeId] when given. perPage is the API max, so
  /// this covers the full library while it's small.
  Future<List<Prayer>> random({int count = 2, String? excludeId}) =>
      _guard(() async {
        final res = await _api.getJson('/v1/prayers',
            query: {'perPage': '100', 'sort': '-created'});
        final items = (res['items'] as List?) ?? const [];
        final pool = items
            .map((e) => Prayer.fromJson(e as Map<String, dynamic>))
            .where((p) => p.id != excludeId)
            .toList();
        pool.shuffle();
        return pool.take(count).toList();
      });

  /// Search / browse confirmed du'as, one page at a time. With no filters it
  /// returns the most recent du'as (the "all du'as" browse list). Filters are
  /// taxonomy slugs. Returns the page items plus paging metadata so callers can
  /// implement infinite scroll.
  Future<PrayerPage> search({
    String query = '',
    String? typeSlug,
    String? categorySlug,
    String? groupSlug,
    int page = 1,
    int perPage = 25,
  }) =>
      _guard(() async {
        final res = await _api.getJson('/v1/prayers', query: {
          'q': query.trim(),
          'type': typeSlug,
          'category': categorySlug,
          'group': groupSlug,
          'page': '$page',
          'perPage': '$perPage',
          'sort': '-created',
        });
        final items = (res['items'] as List?) ?? const [];
        return PrayerPage(
          items: items
              .map((e) => Prayer.fromJson(e as Map<String, dynamic>))
              .toList(),
          page: (res['page'] as num?)?.toInt() ?? page,
          totalItems: (res['totalItems'] as num?)?.toInt() ?? items.length,
          totalPages: (res['totalPages'] as num?)?.toInt() ?? 1,
        );
      });

  /// Submit a new du'a for review (created server-side as `pending`).
  /// Only [text] is required by the API; [categorySlug] and [typeSlug] are
  /// optional and only sent when provided.
  Future<void> submit({
    required String text,
    String? categorySlug,
    String? typeSlug,
  }) =>
      _guard(() async {
        await _api.postJson('/v1/prayers', {
          'text': text.trim(),
          if (categorySlug != null && categorySlug.isNotEmpty)
            'category': categorySlug,
          if (typeSlug != null && typeSlug.isNotEmpty) 'type': typeSlug,
        });
      });
}
