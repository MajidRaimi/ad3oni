import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../../core/theme/app_tokens.dart';
import '../../../../core/theme/app_typography.dart';
import '../../controller/add_dua_controller.dart';

/// Confirmation shown after a du'a is submitted for review.
class SuccessView extends ConsumerWidget {
  const SuccessView({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final controller = ref.read(addDuaControllerProvider);
    final scheme = Theme.of(context).colorScheme;
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(AppSpacing.xl),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Container(
              width: 84,
              height: 84,
              decoration: BoxDecoration(
                color: scheme.secondary.withValues(alpha: 0.12),
                shape: BoxShape.circle,
              ),
              child: Icon(Icons.check_rounded, size: 40, color: scheme.secondary),
            ),
            const SizedBox(height: AppSpacing.lg),
            Text(
              'تم استلام دعائك',
              style: AppFonts.display(fontSize: 28, color: scheme.onSurface),
            ),
            const SizedBox(height: AppSpacing.sm),
            Text(
              'يظهر للجميع بعد المراجعة. جزاك الله خيرًا. 🤍',
              textAlign: TextAlign.center,
              style: AppFonts.sans(
                fontSize: 15,
                height: 1.7,
                color: scheme.onSurface.withValues(alpha: 0.65),
              ),
            ),
            const SizedBox(height: AppSpacing.lg),
            FilledButton(
              onPressed: controller.reset,
              child: const Text('أضِف دعاءً آخر'),
            ),
          ],
        ),
      ),
    );
  }
}
