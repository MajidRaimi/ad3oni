import 'package:flutter/material.dart';

import '../theme/app_colors.dart';
import '../theme/app_tokens.dart';

/// The signature Ad3oni "night" surface: a deep royal→night radial gradient
/// with a soft lilac glow. Used by the du'a hero card and widgets.
class NightBackground extends StatelessWidget {
  const NightBackground({
    super.key,
    required this.child,
    this.borderRadius,
    this.liftOnDark = false,
  });

  final Widget child;
  final BorderRadius? borderRadius;

  /// Adds a lilac border + violet glow so the card lifts off a dark page.
  final bool liftOnDark;

  @override
  Widget build(BuildContext context) {
    final radius = borderRadius ?? BorderRadius.circular(AppRadii.hero);
    return DecoratedBox(
      decoration: BoxDecoration(
        borderRadius: radius,
        gradient: const RadialGradient(
          center: Alignment(0, -1.15),
          radius: 1.25,
          colors: [AppColors.nightGrad1, AppColors.nightGrad2, AppColors.nightGrad3],
          stops: [0.0, 0.46, 1.0],
        ),
        border: liftOnDark
            ? Border.all(color: AppColors.lilac.withValues(alpha: 0.32))
            : null,
        boxShadow: liftOnDark
            ? [
                BoxShadow(
                  color: AppColors.violet.withValues(alpha: 0.30),
                  blurRadius: 56,
                  offset: const Offset(0, 22),
                ),
              ]
            : [
                BoxShadow(
                  color: AppColors.royal.withValues(alpha: 0.34),
                  blurRadius: 60,
                  offset: const Offset(0, 24),
                ),
              ],
      ),
      child: ClipRRect(
        borderRadius: radius,
        child: Stack(
          children: [
            Positioned.fill(
              child: IgnorePointer(
                child: DecoratedBox(
                  decoration: BoxDecoration(
                    gradient: RadialGradient(
                      center: const Alignment(0, 0.1),
                      radius: 0.9,
                      colors: [
                        AppColors.lilac.withValues(alpha: 0.20),
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
