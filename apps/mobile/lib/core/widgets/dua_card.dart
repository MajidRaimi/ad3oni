import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../controllers/saved_controller.dart';
import '../models/prayer.dart';
import '../theme/app_colors.dart';
import '../theme/app_typography.dart';
import '../utils/share_dua.dart';
import 'meta_chips.dart';

/// Compact du'a card used in lists (suggested, search results, saved).
///
/// Mirrors the brand "quotation" identity: a soft gradient surface, a faint
/// `{` watermark, a violet→lilac blockquote rule beside the du'a, a divider,
/// and the actions rendered as soft buttons.
class DuaCard extends ConsumerWidget {
  const DuaCard({super.key, required this.prayer});

  final Prayer prayer;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final scheme = Theme.of(context).colorScheme;
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final saved = ref.watch(savedControllerProvider);

    final accent = isDark ? AppColors.lilac : AppColors.violet;
    final cardColor = Theme.of(context).cardTheme.color ?? scheme.surface;
    final softTint = isDark
        ? Colors.white.withValues(alpha: 0.04)
        : AppColors.royal.withValues(alpha: 0.04);
    final radius = BorderRadius.circular(22);

    return DecoratedBox(
      decoration: BoxDecoration(
        borderRadius: radius,
        gradient: LinearGradient(
          begin: Alignment.topRight,
          end: Alignment.bottomLeft,
          colors: [cardColor, Color.alphaBlend(softTint, cardColor)],
        ),
        border: Border.all(color: scheme.outline),
        boxShadow: isDark
            ? null
            : [
                BoxShadow(
                  color: AppColors.night.withValues(alpha: 0.04),
                  blurRadius: 2,
                  offset: const Offset(0, 1),
                ),
                BoxShadow(
                  color: AppColors.royal.withValues(alpha: 0.16),
                  blurRadius: 30,
                  spreadRadius: -18,
                  offset: const Offset(0, 16),
                ),
              ],
      ),
      child: ClipRRect(
        borderRadius: radius,
        child: Stack(
          children: [
            // Signature quotation watermark, peeking from the (RTL) end corner.
            Positioned(
              left: 14,
              top: -34,
              child: Text(
                '{',
                style: AppFonts.display(
                  fontSize: 96,
                  height: 1,
                  color: accent.withValues(alpha: 0.06),
                ),
              ),
            ),
            Padding(
              padding: const EdgeInsets.fromLTRB(20, 20, 20, 15),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                mainAxisSize: MainAxisSize.min,
                children: [
                  IntrinsicHeight(
                    child: Row(
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        // Blockquote rule on the leading (RTL: right) edge.
                        Container(
                          width: 3,
                          margin: const EdgeInsets.symmetric(vertical: 2),
                          decoration: BoxDecoration(
                            borderRadius: BorderRadius.circular(999),
                            gradient: const LinearGradient(
                              begin: Alignment.topCenter,
                              end: Alignment.bottomCenter,
                              colors: [AppColors.violet, AppColors.lilac],
                            ),
                          ),
                        ),
                        const SizedBox(width: 12),
                        Expanded(
                          child: Text(
                            prayer.text,
                            textAlign: TextAlign.start,
                            style: AppFonts.display(
                              fontSize: 21,
                              height: 1.75,
                              color: scheme.onSurface,
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 14),
                  Container(height: 1, color: scheme.outline.withValues(alpha: 0.65)),
                  const SizedBox(height: 14),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Flexible(child: MetaChips(prayer: prayer)),
                      Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          _IconAction(
                            icon: saved.isSaved(prayer.id)
                                ? Icons.bookmark_rounded
                                : Icons.bookmark_border_rounded,
                            active: saved.isSaved(prayer.id),
                            onTap: () => saved.toggle(prayer),
                          ),
                          const SizedBox(width: 7),
                          _IconAction(
                            icon: Icons.ios_share_rounded,
                            onTap: () => shareDua(prayer),
                          ),
                        ],
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

/// A soft, bordered icon button. Fills with an accent tint when [active].
class _IconAction extends StatelessWidget {
  const _IconAction({required this.icon, required this.onTap, this.active = false});

  final IconData icon;
  final VoidCallback onTap;
  final bool active;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final accent = isDark ? AppColors.lilac : AppColors.violet;
    final soft = isDark
        ? Colors.white.withValues(alpha: 0.04)
        : AppColors.royal.withValues(alpha: 0.04);

    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(12),
      child: Container(
        width: 38,
        height: 38,
        decoration: BoxDecoration(
          color: active ? accent.withValues(alpha: 0.13) : soft,
          borderRadius: BorderRadius.circular(12),
          border: Border.all(
            color: active ? accent.withValues(alpha: 0.45) : scheme.outline,
          ),
        ),
        child: Icon(
          icon,
          size: 18,
          color: active ? accent : scheme.onSurface.withValues(alpha: 0.55),
        ),
      ),
    );
  }
}
