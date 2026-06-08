import 'package:flutter/foundation.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

/// Exposes the [ShellController] to the widget tree.
final shellControllerProvider =
    ChangeNotifierProvider<ShellController>((ref) => ShellController());

/// Tracks the active bottom-navigation tab.
class ShellController extends ChangeNotifier {
  int _index = 0;
  int get index => _index;

  void setIndex(int value) {
    if (value == _index) return;
    _index = value;
    notifyListeners();
  }
}
