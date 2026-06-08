import 'package:flutter/foundation.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/error/failure.dart';
import '../../../core/providers.dart';
import '../../../core/repositories/prayers_repository.dart';

/// Exposes the Add form's controller. Auto-disposed so the form resets when the
/// screen is rebuilt fresh.
final addDuaControllerProvider =
    ChangeNotifierProvider.autoDispose<AddDuaController>(
  (ref) => AddDuaController(ref.watch(prayersRepositoryProvider)),
);

/// Form state + submission for adding a new du'a (created as `pending`).
/// Group/category/type are tracked by taxonomy slug.
class AddDuaController extends ChangeNotifier {
  AddDuaController(this._repo);

  final PrayersRepository _repo;

  String text = '';
  String? groupSlug;
  String? categorySlug;
  String? typeSlug;

  bool submitting = false;
  bool success = false;
  Failure? error;

  bool get canSubmit =>
      text.trim().length >= 3 && categorySlug != null && typeSlug != null;

  void setText(String value) {
    text = value;
    notifyListeners();
  }

  /// Selecting a group clears the chosen category (it must belong to the group).
  void selectGroup(String? value) {
    groupSlug = value;
    categorySlug = null;
    notifyListeners();
  }

  void selectCategory(String? value) {
    categorySlug = value;
    notifyListeners();
  }

  void selectType(String? value) {
    typeSlug = value;
    notifyListeners();
  }

  Future<void> submit() async {
    if (!canSubmit || submitting) return;
    submitting = true;
    error = null;
    notifyListeners();
    try {
      await _repo.submit(
        text: text,
        categorySlug: categorySlug,
        typeSlug: typeSlug,
      );
      success = true;
    } catch (e) {
      error = failureFrom(e);
    }
    submitting = false;
    notifyListeners();
  }

  void reset() {
    text = '';
    groupSlug = null;
    categorySlug = null;
    typeSlug = null;
    success = false;
    error = null;
    notifyListeners();
  }
}
