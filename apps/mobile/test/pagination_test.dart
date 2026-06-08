// Verifies the كل الأدعية infinite-scroll paging in DuaSearchController.
import 'package:ad3oni/core/repositories/prayers_repository.dart';
import 'package:ad3oni/core/models/prayer.dart';
import 'package:ad3oni/features/search/controller/search_controller.dart';
import 'package:flutter_test/flutter_test.dart';

/// A repo that serves a fixed library in pages of 25, recording each request.
class _FakeRepo extends PrayersRepository {
  _FakeRepo(this.total);
  final int total;
  final List<int> requestedPages = [];

  @override
  Future<PrayerPage> search({
    String query = '',
    String? typeSlug,
    String? categorySlug,
    String? groupSlug,
    int page = 1,
    int perPage = 25,
  }) async {
    requestedPages.add(page);
    final start = (page - 1) * perPage;
    final end = (start + perPage).clamp(0, total);
    final items = [
      for (var i = start; i < end; i++)
        Prayer(id: 'p$i', text: 'دعاء $i', status: 'confirmed'),
    ];
    final totalPages = (total / perPage).ceil();
    return PrayerPage(
      items: items,
      page: page,
      totalItems: total,
      totalPages: totalPages,
    );
  }
}

void main() {
  test('first page loads, then loadMore appends until exhausted', () async {
    final repo = _FakeRepo(82); // 4 pages of 25 (last = 7)
    final c = DuaSearchController(repo);

    await c.run();
    expect(c.results.length, 25);
    expect(c.totalItems, 82);
    expect(c.hasMore, isTrue);

    await c.loadMore(); // page 2
    expect(c.results.length, 50);
    expect(c.hasMore, isTrue);

    await c.loadMore(); // page 3
    expect(c.results.length, 75);
    expect(c.hasMore, isTrue);

    await c.loadMore(); // page 4 (last, 7 items)
    expect(c.results.length, 82);
    expect(c.hasMore, isFalse);

    // No further pages are fetched once exhausted.
    await c.loadMore();
    expect(repo.requestedPages, [1, 2, 3, 4]);

    // No duplicate ids across the appended pages.
    expect(c.results.map((p) => p.id).toSet().length, 82);
  });

  test('a new query resets paging back to page 1', () async {
    final repo = _FakeRepo(82);
    final c = DuaSearchController(repo);

    await c.run();
    await c.loadMore(); // now on page 2
    expect(c.results.length, 50);

    repo.requestedPages.clear();
    c.selectType('custom'); // triggers run() again
    await Future<void>.delayed(const Duration(milliseconds: 10));

    expect(repo.requestedPages.first, 1); // restarted from page 1
    expect(c.results.length, 25);
    expect(c.hasMore, isTrue);
  });
}
