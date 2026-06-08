import 'package:flutter/material.dart';

import '../theme/app_colors.dart';
import '../theme/app_tokens.dart';
import '../theme/app_typography.dart';

/// A premium pill search field: muted fill, leading icon in a soft disc, an
/// animated focus ring (violet) + glow, and a clear button when non-empty.
class BrandSearchField extends StatefulWidget {
  const BrandSearchField({
    super.key,
    required this.controller,
    required this.hint,
    required this.onChanged,
    this.onClear,
  });

  final TextEditingController controller;
  final String hint;
  final ValueChanged<String> onChanged;
  final VoidCallback? onClear;

  @override
  State<BrandSearchField> createState() => _BrandSearchFieldState();
}

class _BrandSearchFieldState extends State<BrandSearchField> {
  final _focus = FocusNode();
  bool _focused = false;

  @override
  void initState() {
    super.initState();
    _focus.addListener(() => setState(() => _focused = _focus.hasFocus));
    widget.controller.addListener(_onText);
  }

  void _onText() => setState(() {});

  @override
  void dispose() {
    _focus.removeListener(() {});
    widget.controller.removeListener(_onText);
    _focus.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    final isDark = scheme.brightness == Brightness.dark;
    final accent = isDark ? AppColors.lilac : AppColors.violet;
    final hasText = widget.controller.text.isNotEmpty;

    final fill = isDark
        ? Colors.white.withValues(alpha: 0.05)
        : AppColors.royal.withValues(alpha: 0.035);

    return AnimatedContainer(
      duration: AppMotion.fast,
      curve: AppMotion.ease,
      height: 54,
      padding: const EdgeInsets.symmetric(horizontal: 8),
      decoration: BoxDecoration(
        color: fill,
        borderRadius: BorderRadius.circular(AppRadii.pill),
        border: Border.all(
          color: _focused ? accent : scheme.outline,
          width: _focused ? 1.5 : 1,
        ),
        boxShadow: _focused
            ? [
                BoxShadow(
                  color: accent.withValues(alpha: 0.22),
                  blurRadius: 18,
                  spreadRadius: -4,
                  offset: const Offset(0, 6),
                ),
              ]
            : null,
      ),
      child: Row(
        children: [
          const SizedBox(width: 6),
          Container(
            width: 34,
            height: 34,
            decoration: BoxDecoration(
              color: accent.withValues(alpha: _focused ? 0.16 : 0.10),
              shape: BoxShape.circle,
            ),
            child: Icon(Icons.search_rounded, size: 18, color: accent),
          ),
          const SizedBox(width: 10),
          Expanded(
            child: TextField(
              controller: widget.controller,
              focusNode: _focus,
              onChanged: widget.onChanged,
              textInputAction: TextInputAction.search,
              cursorColor: accent,
              style: AppFonts.sans(fontSize: 15, color: scheme.onSurface),
              decoration: InputDecoration(
                isCollapsed: true,
                border: InputBorder.none,
                enabledBorder: InputBorder.none,
                focusedBorder: InputBorder.none,
                filled: false,
                hintText: widget.hint,
                hintStyle: AppFonts.sans(
                  fontSize: 15,
                  color: scheme.onSurface.withValues(alpha: 0.4),
                ),
              ),
            ),
          ),
          AnimatedSwitcher(
            duration: AppMotion.fast,
            transitionBuilder: (child, anim) =>
                ScaleTransition(scale: anim, child: child),
            child: hasText
                ? IconButton(
                    key: const ValueKey('clear'),
                    visualDensity: VisualDensity.compact,
                    onPressed: () {
                      widget.controller.clear();
                      widget.onChanged('');
                      widget.onClear?.call();
                    },
                    icon: Icon(Icons.close_rounded,
                        size: 18, color: scheme.onSurface.withValues(alpha: 0.5)),
                  )
                : const SizedBox(width: 8, key: ValueKey('empty')),
          ),
        ],
      ),
    );
  }
}
