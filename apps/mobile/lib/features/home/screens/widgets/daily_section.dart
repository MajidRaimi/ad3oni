import 'package:flutter/material.dart';

import '../../../../core/error/failure.dart';
import '../../../../core/state/view_state.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_gradients.dart';
import '../../../../core/theme/app_tokens.dart';
import '../../../../core/theme/app_typography.dart';
import '../../../../core/widgets/dua_hero_card.dart';
import '../../../../core/widgets/empty_state.dart';
import '../../../../core/widgets/night_background.dart';
import '../../controller/home_controller.dart';

/// The «دعاء اليوم» area of the home screen — renders loading / error / empty /
/// hero from the home controller's [ViewState].
class DailySection extends StatelessWidget {
  const DailySection({super.key, required this.state, required this.onRetry});

  final ViewState<HomeData> state;
  final VoidCallback onRetry;

  @override
  Widget build(BuildContext context) {
    return switch (state) {
      ViewLoading() => const _DailyLoadingCard(),
      ViewError(:final failure) =>
        _DailyErrorCard(failure: failure, onRetry: onRetry),
      ViewData(:final value) => value.daily == null
          ? const SizedBox(
              height: 200,
              child: EmptyState(
                icon: Icons.auto_awesome_rounded,
                title: 'لا يوجد دعاء بعد',
                message: 'سيظهر دعاء اليوم هنا بمجرد إضافة الأدعية.',
              ),
            )
          : DuaHeroCard(prayer: value.daily!),
    };
  }
}

/// Compact error card for the daily slot (the full-screen [ErrorView] is too
/// tall for this inline area). Still shows the typed failure + a retry.
class _DailyErrorCard extends StatelessWidget {
  const _DailyErrorCard({required this.failure, required this.onRetry});
  final Failure failure;
  final VoidCallback onRetry;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    return Container(
      padding: const EdgeInsets.all(AppSpacing.lg),
      decoration: BoxDecoration(
        color: Theme.of(context).cardTheme.color,
        borderRadius: BorderRadius.circular(AppRadii.card),
        border: Border.all(color: scheme.outline),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(Icons.cloud_off_rounded, color: scheme.onSurface.withValues(alpha: 0.5)),
          const SizedBox(height: 10),
          Text(
            failure.messageAr,
            textAlign: TextAlign.center,
            style: AppFonts.sans(fontSize: 14, color: scheme.onSurface.withValues(alpha: 0.7)),
          ),
          const SizedBox(height: 12),
          TextButton(onPressed: onRetry, child: const Text('إعادة المحاولة')),
        ],
      ),
    );
  }
}

/// Branded placeholder shown while the daily du'a loads.
class _DailyLoadingCard extends StatelessWidget {
  const _DailyLoadingCard();

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final radius = BorderRadius.circular(AppRadii.heroLg);
    if (isDark) {
      return NightBackground(
        liftOnDark: true,
        borderRadius: radius,
        child: const SizedBox(
          height: 240,
          child: Center(child: CircularProgressIndicator(color: AppColors.lilac)),
        ),
      );
    }
    return Container(
      height: 240,
      decoration: BoxDecoration(
        gradient: AppGradients.paper,
        borderRadius: radius,
        border: Border.all(color: AppColors.lightBorder),
      ),
      child: const Center(child: CircularProgressIndicator(color: AppColors.violet)),
    );
  }
}
