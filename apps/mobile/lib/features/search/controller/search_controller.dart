import 'dart:async';

import 'package:flutter/foundation.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/error/failure.dart';
import '../../../core/models/prayer.dart';
import '../../../core/providers.dart';
import '../../../core/repositories/prayers_repository.dart';
import '../../../core/state/view_state.dart';

/// Exposes the app-wide [DuaSearchController], loading the initial "all du'as"
/// list on creation. App-level so the Home screen can drive it.
final duaSearchControllerProvider = ChangeNotifierProvider<DuaSearchController>(
  (ref) => DuaSearchController(ref.watch(prayersRepositoryProvider))
    ..loadInitial(),
);

/// Browse + search over du'as with group/type/text filters (server-side via
/// taxonomy slugs). The result list is a [ViewState]; pagination/refresh flags
/// layer on top (CLAUDE.md §6). With no active filters it lists the most recent
/// du'as (the "all du'as" view). App-level so the Home screen can drive it.
class DuaSearchController extends ChangeNotifier {
  DuaSearchController(this._repo);

  final PrayersRepository _repo;
  Timer? _debounce;

  /// Items per page for the infinite-scroll list.
  static const int _pageSize = 25;

  // --- Query inputs (plain fields drive the query; only the result is state) ---
  String query = '';
  String? groupSlug;
  String? typeSlug;

  // --- Result state ---
  ViewState<List<Prayer>> _state = const ViewLoading();
  ViewState<List<Prayer>> get state => _state;

  /// Convenience: the loaded results (empty when not yet loaded / on error).
  List<Prayer> get results => _state.dataOrNull ?? const [];

  bool hasSearched = false;

  /// A new query is running while previous results stay on screen (dimmed).
  bool refreshing = false;

  // --- Paging state for the current query ---
  int _page = 0;
  int totalItems = 0;
  bool hasMore = false;
  bool loadingMore = false;

  bool get hasActiveFilters =>
      query.trim().isNotEmpty || groupSlug != null || typeSlug != null;

  void setQuery(String value) {
    query = value;
    notifyListeners();
    _debounce?.cancel();
    _debounce = Timer(const Duration(milliseconds: 350), run);
  }

  /// Set or clear the group filter ([slug] = null clears it).
  void selectGroup(String? slug) {
    if (groupSlug == slug) return;
    groupSlug = slug;
    notifyListeners();
    run();
  }

  /// Set or clear the type filter ([slug] = null clears it).
  void selectType(String? slug) {
    if (typeSlug == slug) return;
    typeSlug = slug;
    notifyListeners();
    run();
  }

  /// Used by the Home screen to jump into search pre-filtered by a group.
  void openWithGroup(String slug) {
    groupSlug = slug;
    query = '';
    typeSlug = null;
    notifyListeners();
    run();
  }

  /// Resets all filters and reloads the full "all du'as" list. Used by the Home
  /// screen's «عرض الكل» before switching to the كل الأدعية tab.
  void openAll() {
    query = '';
    groupSlug = null;
    typeSlug = null;
    notifyListeners();
    run();
  }

  /// Runs the current query from page 1, replacing the result list. Keeps the
  /// previous data visible (dimmed) while refreshing if we already had results.
  Future<void> run() async {
    if (_state is ViewData<List<Prayer>>) {
      refreshing = true;
    } else {
      _state = const ViewLoading();
    }
    loadingMore = false;
    notifyListeners();
    try {
      final page = await _repo.search(
        query: query,
        typeSlug: typeSlug,
        groupSlug: groupSlug,
        page: 1,
        perPage: _pageSize,
      );
      _state = ViewData(page.items);
      _page = page.page;
      totalItems = page.totalItems;
      hasMore = page.hasMore;
    } catch (e) {
      _state = ViewError(failureFrom(e));
      totalItems = 0;
      hasMore = false;
    }
    refreshing = false;
    hasSearched = true;
    notifyListeners();
  }

  /// Fetches the next page and appends it. No-op while refreshing, when there
  /// are no more pages, or before the first page has loaded.
  Future<void> loadMore() async {
    final current = _state.dataOrNull;
    if (loadingMore || refreshing || !hasMore || current == null) return;
    loadingMore = true;
    notifyListeners();

    // Snapshot the filters this request belongs to, so a query change mid-flight
    // doesn't append stale results to a different list.
    final reqQuery = query;
    final reqGroup = groupSlug;
    final reqType = typeSlug;
    final nextPage = _page + 1;
    try {
      final page = await _repo.search(
        query: reqQuery,
        typeSlug: reqType,
        groupSlug: reqGroup,
        page: nextPage,
        perPage: _pageSize,
      );
      final stillSameQuery =
          reqQuery == query && reqGroup == groupSlug && reqType == typeSlug;
      if (stillSameQuery && _state is ViewData<List<Prayer>>) {
        _state = ViewData([...current, ...page.items]);
        _page = page.page;
        totalItems = page.totalItems;
        hasMore = page.hasMore;
      }
    } catch (_) {
      // Keep what we have; the footer can offer a retry on the next scroll.
    }
    loadingMore = false;
    notifyListeners();
  }

  /// Loads the full "all du'as" list once the screen is shown.
  Future<void> loadInitial() async {
    if (hasSearched || refreshing) return;
    await run();
  }

  void clear() {
    query = '';
    groupSlug = null;
    typeSlug = null;
    notifyListeners();
    run(); // fall back to the full "all du'as" list
  }

  @override
  void dispose() {
    _debounce?.cancel();
    super.dispose();
  }
}
