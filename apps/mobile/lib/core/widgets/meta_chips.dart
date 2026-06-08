import 'package:flutter/material.dart';

import '../models/prayer.dart';
import '../theme/app_colors.dart';
import '../theme/app_typography.dart';

/// The category + type pills shown on every du'a, read from the du'a itself
/// (the API expands `category`/`type` inline).
class MetaChips extends StatelessWidget {
  const MetaChips({super.key, required this.prayer, this.onDark = false});

  final Prayer prayer;
  final bool onDark;

  @override
  Widget build(BuildContext context) {
    final category = prayer.categoryName;
    final type = prayer.typeName;

    return Wrap(
      spacing: 7,
      runSpacing: 7,
      children: [
        if (category.isNotEmpty) _chip(context, category, solid: true),
        if (type.isNotEmpty) _chip(context, type, solid: false),
      ],
    );
  }

  Widget _chip(BuildContext context, String label, {required bool solid}) {
    final scheme = Theme.of(context).colorScheme;
    final isDark = scheme.brightness == Brightness.dark;
    final accent = isDark ? AppColors.lilac : AppColors.violet;

    // Outlined "type" chip — clean, no dot.
    if (!solid) {
      final fg = onDark
          ? Colors.white.withValues(alpha: 0.85)
          : scheme.onSurface.withValues(alpha: 0.6);
      final border = onDark ? AppColors.lilac.withValues(alpha: 0.30) : scheme.outline;
      return Container(
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 5),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(999),
          border: Border.all(color: border),
        ),
        child: Text(
          label,
          style: AppFonts.sans(fontSize: 12, fontWeight: FontWeight.w500, color: fg),
        ),
      );
    }

    // Solid "category" chip — soft gradient + a leading status dot.
    final Color base = onDark
        ? AppColors.lilac.withValues(alpha: 0.14)
        : (isDark ? AppColors.darkSecondary : AppColors.lightSecondary);
    final Color fg = onDark
        ? Colors.white.withValues(alpha: 0.9)
        : (isDark ? AppColors.darkFg : AppColors.royal);

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 5),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topRight,
          end: Alignment.bottomLeft,
          colors: [base, Color.alphaBlend(accent.withValues(alpha: 0.12), base)],
        ),
        borderRadius: BorderRadius.circular(999),
        border: Border.all(color: accent.withValues(alpha: 0.14)),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Container(
            width: 6,
            height: 6,
            decoration: BoxDecoration(
              color: accent,
              shape: BoxShape.circle,
              boxShadow: [
                BoxShadow(color: accent.withValues(alpha: 0.18), spreadRadius: 3),
              ],
            ),
          ),
          const SizedBox(width: 7),
          Text(
            label,
            style: AppFonts.sans(fontSize: 12, fontWeight: FontWeight.w600, color: fg),
          ),
        ],
      ),
    );
  }
}
