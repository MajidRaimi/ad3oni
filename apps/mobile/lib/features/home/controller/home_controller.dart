import 'package:flutter/foundation.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/error/failure.dart';
import '../../../core/models/prayer.dart';
import '../../../core/providers.dart';
import '../../../core/repositories/prayers_repository.dart';
import '../../../core/state/view_state.dart';

/// Exposes the [HomeController]. Auto-disposed: it reloads fresh content when
/// the home screen is shown again after being torn down.
final homeControllerProvider =
    ChangeNotifierProvider.autoDispose<HomeController>(
  (ref) => HomeController(ref.watch(prayersRepositoryProvider)),
);

/// The home screen's content: the daily du'a + a few suggested du'as.
class HomeData {
  const HomeData({required this.daily, required this.suggested});
  final Prayer? daily;
  final List<Prayer> suggested;
}

/// Loads the home screen content as a single [ViewState].
class HomeController extends ChangeNotifier {
  HomeController(this._repo) {
    load();
  }

  final PrayersRepository _repo;

  ViewState<HomeData> _state = const ViewLoading();
  ViewState<HomeData> get state => _state;

  Future<void> load() async {
    _state = const ViewLoading();
    notifyListeners();
    try {
      final results = await Future.wait([
        _repo.daily(),
        _repo.random(count: 3),
      ]);
      final daily = results[0] as Prayer?;
      final pool = results[1] as List<Prayer>;
      // Suggested = random across all, excluding the hero du'a.
      final suggested = pool.where((p) => p.id != daily?.id).take(2).toList();
      _state = ViewData(HomeData(daily: daily, suggested: suggested));
    } catch (e) {
      _state = ViewError(failureFrom(e));
    }
    notifyListeners();
  }

  Future<void> refresh() => load();
}
