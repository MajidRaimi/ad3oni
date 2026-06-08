import 'package:flutter/material.dart';

import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_gradients.dart';
import '../../../../core/theme/app_tokens.dart';
import '../../../../core/theme/app_typography.dart';

/// A compact filter pill that opens a bottom-sheet picker. Shows [label] when
/// nothing is chosen, or the selected option's name (filled with the brand
/// gradient) when active. The sheet includes a «الكل» row to clear the filter.
class FilterSelector extends StatelessWidget {
  const FilterSelector({
    super.key,
    required this.label,
    required this.options,
    required this.selectedId,
    required this.onChanged,
  });

  final String label;
  final List<(String, String)> options;
  final String? selectedId;

  /// Called with the chosen slug, or null to clear the filter.
  final ValueChanged<String?> onChanged;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    final isDark = scheme.brightness == Brightness.dark;

    String? selectedName;
    for (final (id, name) in options) {
      if (id == selectedId) {
        selectedName = name;
        break;
      }
    }
    final active = selectedName != null;

    return Material(
      color: Colors.transparent,
      child: InkWell(
        borderRadius: BorderRadius.circular(AppRadii.pill),
        onTap: options.isEmpty ? null : () => _open(context),
        child: AnimatedContainer(
          duration: AppMotion.fast,
          curve: AppMotion.ease,
          height: 46,
          padding: const EdgeInsets.symmetric(horizontal: 16),
          decoration: BoxDecoration(
            gradient: active ? AppGradients.chip : null,
            color: active
                ? null
                : (isDark
                    ? Colors.white.withValues(alpha: 0.04)
                    : AppColors.royal.withValues(alpha: 0.03)),
            borderRadius: BorderRadius.circular(AppRadii.pill),
            border: Border.all(color: active ? Colors.transparent : scheme.outline),
            boxShadow: active
                ? [
                    BoxShadow(
                      color: AppColors.violet.withValues(alpha: 0.28),
                      blurRadius: 14,
                      spreadRadius: -3,
                      offset: const Offset(0, 5),
                    ),
                  ]
                : null,
          ),
          child: Row(
            children: [
              Expanded(
                child: Text(
                  selectedName ?? label,
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                  style: AppFonts.sans(
                    fontSize: 14,
                    fontWeight: active ? FontWeight.w700 : FontWeight.w600,
                    color: active ? Colors.white : scheme.onSurface.withValues(alpha: 0.72),
                  ),
                ),
              ),
              const SizedBox(width: 6),
              Icon(
                Icons.keyboard_arrow_down_rounded,
                size: 18,
                color: active ? Colors.white : scheme.onSurface.withValues(alpha: 0.45),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Future<void> _open(BuildContext context) async {
    final result = await showModalBottomSheet<_Sel>(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      barrierColor: Colors.black.withValues(alpha: 0.45),
      builder: (_) => _FilterSheet(
        title: label,
        options: options,
        selectedId: selectedId,
      ),
    );
    if (result != null) onChanged(result.id);
  }
}

/// Pop wrapper so a chosen `null` ("الكل") is distinct from a dismissal.
class _Sel {
  const _Sel(this.id);
  final String? id;
}

class _FilterSheet extends StatelessWidget {
  const _FilterSheet({
    required this.title,
    required this.options,
    required this.selectedId,
  });

  final String title;
  final List<(String, String)> options;
  final String? selectedId;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    final isDark = scheme.brightness == Brightness.dark;
    final accent = isDark ? AppColors.lilac : AppColors.violet;
    final selectedText = isDark ? AppColors.lilac : AppColors.royal;

    Widget row(String name, String? id, bool isSel) => InkWell(
          onTap: () => Navigator.of(context).pop(_Sel(id)),
          child: Container(
            padding: const EdgeInsets.symmetric(horizontal: 22, vertical: 15),
            color: isSel ? accent.withValues(alpha: isDark ? 0.14 : 0.10) : null,
            child: Row(
              children: [
                Expanded(
                  child: Text(
                    name,
                    textAlign: TextAlign.right,
                    style: AppFonts.sans(
                      fontSize: 16,
                      fontWeight: isSel ? FontWeight.w700 : FontWeight.w400,
                      color: isSel ? selectedText : scheme.onSurface,
                    ),
                  ),
                ),
                if (isSel) ...[
                  const SizedBox(width: 10),
                  Icon(Icons.check_rounded, size: 20, color: accent),
                ],
              ],
            ),
          ),
        );

    return Container(
      constraints: BoxConstraints(maxHeight: MediaQuery.of(context).size.height * 0.7),
      decoration: BoxDecoration(
        color: Theme.of(context).cardTheme.color ?? scheme.surface,
        borderRadius: const BorderRadius.vertical(top: Radius.circular(AppRadii.xl)),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          const SizedBox(height: 10),
          Container(
            width: 42,
            height: 4,
            decoration: BoxDecoration(
              color: scheme.onSurface.withValues(alpha: 0.18),
              borderRadius: BorderRadius.circular(999),
            ),
          ),
          Padding(
            padding: const EdgeInsets.fromLTRB(22, 16, 22, 12),
            child: Row(
              children: [
                Expanded(
                  child: Text(
                    title,
                    style: AppFonts.sans(
                      fontSize: 17,
                      fontWeight: FontWeight.w700,
                      color: scheme.onSurface,
                    ),
                  ),
                ),
              ],
            ),
          ),
          Divider(height: 1, color: scheme.outline),
          Flexible(
            child: ListView(
              padding: const EdgeInsets.symmetric(vertical: 6),
              shrinkWrap: true,
              children: [
                row('الكل', null, selectedId == null),
                for (final (id, name) in options) row(name, id, id == selectedId),
              ],
            ),
          ),
          SizedBox(height: MediaQuery.of(context).padding.bottom + 10),
        ],
      ),
    );
  }
}
