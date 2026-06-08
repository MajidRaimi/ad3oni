import 'package:flutter/material.dart';

import 'app_colors.dart';

/// Named brand gradients, so widgets reference one source of truth instead of
/// re-declaring `LinearGradient(...)` with raw colors (CLAUDE.md §8).
class AppGradients {
  AppGradients._();

  /// The lilac pill/button gradient (e.g. the «شارك» button).
  static const LinearGradient lilacButton = LinearGradient(
    begin: Alignment.topCenter,
    end: Alignment.bottomCenter,
    colors: [AppColors.lilacBright, AppColors.lilac],
  );

  /// The light "paper" hero surface (white → soft lilac).
  static const LinearGradient paper = LinearGradient(
    begin: Alignment.topCenter,
    end: Alignment.bottomCenter,
    colors: [AppColors.paper, AppColors.paperEnd],
  );

  /// The violet→lilac accent rule used beside quoted du'a text.
  static const LinearGradient accentRule = LinearGradient(
    begin: Alignment.topCenter,
    end: Alignment.bottomCenter,
    colors: [AppColors.violet, AppColors.lilac],
  );

  /// Diagonal violet→lilac fill for selected chips / active controls.
  static const LinearGradient chip = LinearGradient(
    begin: Alignment.topRight,
    end: Alignment.bottomLeft,
    colors: [AppColors.violet, AppColors.lilac],
  );
}
