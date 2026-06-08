import 'package:flutter/material.dart';

import '../../../../core/theme/app_typography.dart';

/// The time-aware greeting at the top of the home screen.
class HomeGreeting extends StatelessWidget {
  const HomeGreeting({super.key});

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    final hour = DateTime.now().hour;
    final greeting = hour < 12 ? 'صباح الخير' : 'مساء الخير';
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          greeting,
          style: AppFonts.display(fontSize: 34, height: 1.1, color: scheme.onSurface),
        ),
        const SizedBox(height: 4),
        Text(
          'خذ لحظة، وادعُ بما في قلبك.',
          style: AppFonts.sans(
            fontSize: 15,
            color: scheme.onSurface.withValues(alpha: 0.6),
          ),
        ),
      ],
    );
  }
}
