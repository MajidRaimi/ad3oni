import 'package:flutter/material.dart';

import '../../../../core/models/prayer_type.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_tokens.dart';
import '../../../../core/theme/app_typography.dart';

/// A segmented selector for the du'a type (نبوي / قرآني / أثري / مخصص).
class TypeSegmented extends StatelessWidget {
  const TypeSegmented({
    super.key,
    required this.types,
    required this.selectedId,
    required this.onSelect,
  });

  final List<PrayerType> types;
  final String? selectedId;
  final ValueChanged<String?> onSelect;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    final isDark = scheme.brightness == Brightness.dark;
    return Row(
      children: [
        for (final t in types)
          Expanded(
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 3),
              child: GestureDetector(
                onTap: () => onSelect(t.slug),
                child: Container(
                  height: 44,
                  alignment: Alignment.center,
                  decoration: BoxDecoration(
                    color: selectedId == t.slug
                        ? (isDark ? AppColors.darkSecondary : AppColors.lightSecondary)
                        : scheme.surface,
                    borderRadius: BorderRadius.circular(AppRadii.md),
                    border: Border.all(
                      color: selectedId == t.slug ? Colors.transparent : scheme.outline,
                    ),
                  ),
                  child: Text(
                    t.name,
                    style: AppFonts.sans(
                      fontSize: 14,
                      fontWeight:
                          selectedId == t.slug ? FontWeight.w700 : FontWeight.w400,
                      color: selectedId == t.slug
                          ? (isDark ? AppColors.darkFg : AppColors.royal)
                          : scheme.onSurface.withValues(alpha: 0.6),
                    ),
                  ),
                ),
              ),
            ),
          ),
      ],
    );
  }
}
