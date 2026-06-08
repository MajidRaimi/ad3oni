import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:hijri/hijri_calendar.dart';

import '../controllers/saved_controller.dart';
import '../models/prayer.dart';
import '../theme/app_colors.dart';
import '../theme/app_typography.dart';
import '../utils/arabic_numbers.dart';
import '../utils/share_dua.dart';
import 'brand_wordmark.dart';
import 'meta_chips.dart';
import 'night_background.dart';

/// The signature "دعاء اليوم" hero card (brand Variant A — Quotation).
///
/// Dark mode keeps the signature night gradient; light mode uses the brand
/// "paper" surface (white→lilac) so the card sits naturally in the light UI.
class DuaHeroCard extends ConsumerWidget {
  const DuaHeroCard({super.key, required this.prayer, this.eyebrow = 'دعاء اليوم'});

  final Prayer prayer;
  final String eyebrow;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final palette = _HeroPalette(isDark);
    final saved = ref.watch(savedControllerProvider);
    final radius = BorderRadius.circular(32);

    final content = Padding(
      padding: const EdgeInsets.fromLTRB(22, 22, 22, 20),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          // top bar
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              BrandWordmark(size: 27, color: palette.wordmark),
              Icon(Icons.notifications_none_rounded, size: 21, color: palette.bell),
            ],
          ),
          const SizedBox(height: 18),
          _EyebrowPill(label: eyebrow, palette: palette),
          const SizedBox(height: 18),
          _Quote(text: prayer.text, palette: palette),
          if (prayer.sourceName.isNotEmpty) ...[
            const SizedBox(height: 12),
            Text(
              '— ${prayer.sourceName}',
              textAlign: TextAlign.center,
              style: AppFonts.sans(
                fontSize: 13,
                color: palette.accent.withValues(alpha: 0.85),
                fontWeight: FontWeight.w500,
              ),
            ),
          ],
          const SizedBox(height: 14),
          Text(
            _hijriToday(),
            style: AppFonts.mono(fontSize: 12, color: palette.date),
          ),
          const SizedBox(height: 16),
          Container(width: 54, height: 1, color: palette.divider),
          const SizedBox(height: 14),
          MetaChips(prayer: prayer, onDark: isDark),
          const SizedBox(height: 20),
          Row(
            children: [
              Expanded(child: _ShareButton(onTap: () => shareDua(prayer))),
              const SizedBox(width: 10),
              _GhostCircle(
                palette: palette,
                icon: saved.isSaved(prayer.id)
                    ? Icons.bookmark_rounded
                    : Icons.bookmark_border_rounded,
                onTap: () => saved.toggle(prayer),
              ),
            ],
          ),
        ],
      ),
    );

    if (isDark) {
      return NightBackground(liftOnDark: true, borderRadius: radius, child: content);
    }
    return _PaperSurface(borderRadius: radius, child: content);
  }

  static String _hijriToday() {
    final h = HijriCalendar.now();
    final day = toArabicDigits(h.hDay.toString());
    final year = toArabicDigits(h.hYear.toString());
    return '$day ${h.getLongMonthName()} $year هـ';
  }
}

/// Resolves every hero element's colour for the current theme.
class _HeroPalette {
  const _HeroPalette(this.isDark);
  final bool isDark;

  Color get wordmark => isDark ? Colors.white : AppColors.royal;
  Color get bell =>
      isDark ? Colors.white.withValues(alpha: 0.55) : AppColors.violet.withValues(alpha: 0.7);
  Color get accent => isDark ? AppColors.lilac : AppColors.violet;
  Color get eyebrowBg =>
      isDark ? AppColors.lilac.withValues(alpha: 0.14) : AppColors.violet.withValues(alpha: 0.08);
  Color get eyebrowBorder =>
      isDark ? AppColors.lilac.withValues(alpha: 0.28) : AppColors.violet.withValues(alpha: 0.18);
  Color get brace =>
      isDark ? AppColors.lilac.withValues(alpha: 0.45) : AppColors.violet.withValues(alpha: 0.32);
  Color get dua => isDark ? Colors.white : AppColors.ink;
  bool get duaGlow => isDark;
  Color get date =>
      isDark ? AppColors.lilac.withValues(alpha: 0.7) : AppColors.neutral;
  Color get divider =>
      isDark ? AppColors.lilac.withValues(alpha: 0.4) : AppColors.violet.withValues(alpha: 0.25);
  Color get ghostBg =>
      isDark ? Colors.white.withValues(alpha: 0.04) : Colors.transparent;
  Color get ghostBorder =>
      isDark ? Colors.white.withValues(alpha: 0.22) : AppColors.lightBorder;
  Color get ghostIcon => isDark ? Colors.white : AppColors.royal;
}

/// The brand "paper" surface used by the hero card in light mode.
class _PaperSurface extends StatelessWidget {
  const _PaperSurface({required this.child, required this.borderRadius});

  final Widget child;
  final BorderRadius borderRadius;

  @override
  Widget build(BuildContext context) {
    return DecoratedBox(
      decoration: BoxDecoration(
        borderRadius: borderRadius,
        gradient: const LinearGradient(
          begin: Alignment.topCenter,
          end: Alignment.bottomCenter,
          colors: [AppColors.paper, AppColors.paperEnd],
        ),
        border: Border.all(color: AppColors.lightBorder),
        boxShadow: [
          BoxShadow(
            color: AppColors.royal.withValues(alpha: 0.10),
            blurRadius: 40,
            offset: const Offset(0, 16),
          ),
        ],
      ),
      child: ClipRRect(
        borderRadius: borderRadius,
        child: Stack(
          children: [
            Positioned.fill(
              child: IgnorePointer(
                child: DecoratedBox(
                  decoration: BoxDecoration(
                    gradient: RadialGradient(
                      center: const Alignment(0, -0.4),
                      radius: 0.9,
                      colors: [
                        AppColors.violet.withValues(alpha: 0.06),
                        Colors.transparent,
                      ],
                    ),
                  ),
                ),
              ),
            ),
            child,
          ],
        ),
      ),
    );
  }
}

class _EyebrowPill extends StatelessWidget {
  const _EyebrowPill({required this.label, required this.palette});
  final String label;
  final _HeroPalette palette;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
      decoration: BoxDecoration(
        color: palette.eyebrowBg,
        borderRadius: BorderRadius.circular(999),
        border: Border.all(color: palette.eyebrowBorder),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(Icons.auto_awesome_rounded, size: 13, color: palette.accent),
          const SizedBox(width: 7),
          Text(
            label,
            style: AppFonts.mono(
              fontSize: 11,
              letterSpacing: 2,
              color: palette.accent,
              fontWeight: FontWeight.w500,
            ),
          ),
        ],
      ),
    );
  }
}

class _Quote extends StatelessWidget {
  const _Quote({required this.text, required this.palette});
  final String text;
  final _HeroPalette palette;

  @override
  Widget build(BuildContext context) {
    Widget brace(String ch) => Text(
          ch,
          style: AppFonts.display(fontSize: 52, height: 1, color: palette.brace),
        );

    // Braces flank the du'a inline and sit on its vertical centre, so the
    // quote reads as one balanced unit regardless of line count.
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      crossAxisAlignment: CrossAxisAlignment.center,
      children: [
        brace('{'),
        Flexible(
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 12),
            child: Text(
              text,
              textAlign: TextAlign.center,
              style: AppFonts.display(fontSize: 28, height: 1.7, color: palette.dua).copyWith(
                shadows: palette.duaGlow
                    ? [Shadow(color: AppColors.lilac.withValues(alpha: 0.3), blurRadius: 30)]
                    : null,
              ),
            ),
          ),
        ),
        brace('}'),
      ],
    );
  }
}

class _ShareButton extends StatelessWidget {
  const _ShareButton({required this.onTap});
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        height: 50,
        decoration: BoxDecoration(
          gradient: const LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [AppColors.lilacBright, AppColors.lilac],
          ),
          borderRadius: BorderRadius.circular(999),
          boxShadow: [
            BoxShadow(
              color: AppColors.lilac.withValues(alpha: 0.32),
              blurRadius: 24,
              offset: const Offset(0, 10),
            ),
          ],
        ),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.ios_share_rounded, size: 18, color: AppColors.night),
            const SizedBox(width: 8),
            Text(
              'شارك',
              style: AppFonts.sans(
                fontSize: 16,
                fontWeight: FontWeight.w700,
                color: AppColors.night,
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _GhostCircle extends StatelessWidget {
  const _GhostCircle({required this.icon, required this.onTap, required this.palette});
  final IconData icon;
  final VoidCallback onTap;
  final _HeroPalette palette;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        width: 52,
        height: 50,
        decoration: BoxDecoration(
          color: palette.ghostBg,
          borderRadius: BorderRadius.circular(999),
          border: Border.all(color: palette.ghostBorder),
        ),
        child: Icon(icon, size: 19, color: palette.ghostIcon),
      ),
    );
  }
}
