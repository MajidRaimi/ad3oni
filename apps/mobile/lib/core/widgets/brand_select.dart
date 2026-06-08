import 'package:flutter/material.dart';

import '../theme/app_colors.dart';
import '../theme/app_tokens.dart';
import '../theme/app_typography.dart';

/// One option in a [BrandSelectField].
class BrandSelectOption<T> {
  const BrandSelectOption({required this.value, required this.label});
  final T value;
  final String label;
}

/// A modern, brand-styled select field. Tapping it opens a rounded
/// bottom-sheet picker instead of the dated Material dropdown overlay.
class BrandSelectField<T> extends StatelessWidget {
  const BrandSelectField({
    super.key,
    required this.value,
    required this.hint,
    required this.title,
    required this.options,
    required this.onChanged,
    this.enabled = true,
  });

  final T? value;
  final String hint;
  final String title;
  final List<BrandSelectOption<T>> options;
  final ValueChanged<T> onChanged;
  final bool enabled;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;

    String? selectedLabel;
    for (final o in options) {
      if (o.value == value) {
        selectedLabel = o.label;
        break;
      }
    }
    final hasValue = selectedLabel != null;
    final active = enabled && options.isNotEmpty;

    return Material(
      color: Colors.transparent,
      child: InkWell(
        borderRadius: BorderRadius.circular(AppRadii.md + 2),
        onTap: active ? () => _open(context) : null,
        child: Container(
          height: 56,
          padding: const EdgeInsets.symmetric(horizontal: 16),
          decoration: BoxDecoration(
            color: scheme.surface,
            borderRadius: BorderRadius.circular(AppRadii.md + 2),
            border: Border.all(
              color: hasValue ? scheme.primary.withValues(alpha: 0.45) : scheme.outline,
            ),
          ),
          child: Row(
            children: [
              Expanded(
                child: Text(
                  selectedLabel ?? hint,
                  textAlign: TextAlign.right,
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                  style: AppFonts.sans(
                    fontSize: 15.5,
                    fontWeight: hasValue ? FontWeight.w600 : FontWeight.w400,
                    color: hasValue
                        ? scheme.onSurface
                        : scheme.onSurface.withValues(alpha: active ? 0.45 : 0.3),
                  ),
                ),
              ),
              const SizedBox(width: 8),
              Icon(
                Icons.keyboard_arrow_down_rounded,
                color: scheme.onSurface.withValues(alpha: active ? 0.5 : 0.25),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Future<void> _open(BuildContext context) async {
    final result = await showModalBottomSheet<_Picked<T>>(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      barrierColor: Colors.black.withValues(alpha: 0.45),
      builder: (_) => _PickerSheet<T>(title: title, options: options, selected: value),
    );
    if (result != null) onChanged(result.value);
  }
}

/// Wrapper so we can distinguish "picked a value" from "dismissed" even for
/// nullable T.
class _Picked<T> {
  const _Picked(this.value);
  final T value;
}

class _PickerSheet<T> extends StatelessWidget {
  const _PickerSheet({required this.title, required this.options, required this.selected});

  final String title;
  final List<BrandSelectOption<T>> options;
  final T? selected;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    final isDark = scheme.brightness == Brightness.dark;
    final accent = isDark ? AppColors.lilac : AppColors.violet;
    final selectedText = isDark ? AppColors.lilac : AppColors.royal;

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
            child: ListView.builder(
              padding: const EdgeInsets.symmetric(vertical: 6),
              shrinkWrap: true,
              itemCount: options.length,
              itemBuilder: (context, i) {
                final o = options[i];
                final isSel = o.value == selected;
                return InkWell(
                  onTap: () => Navigator.of(context).pop(_Picked<T>(o.value)),
                  child: Container(
                    padding: const EdgeInsets.symmetric(horizontal: 22, vertical: 15),
                    color: isSel ? accent.withValues(alpha: isDark ? 0.14 : 0.10) : null,
                    child: Row(
                      children: [
                        Expanded(
                          child: Text(
                            o.label,
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
              },
            ),
          ),
          SizedBox(height: MediaQuery.of(context).padding.bottom + 10),
        ],
      ),
    );
  }
}
