import 'package:flutter/material.dart';

import '../../../../core/theme/app_tokens.dart';
import '../../../../core/theme/app_typography.dart';

/// Note explaining that a submitted du'a appears after review.
class PendingNote extends StatelessWidget {
  const PendingNote({super.key});

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    return Container(
      padding: const EdgeInsets.all(15),
      decoration: BoxDecoration(
        color: scheme.primary.withValues(alpha: 0.04),
        borderRadius: BorderRadius.circular(AppRadii.md + 2),
        border: Border.all(color: scheme.outline),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(Icons.info_outline_rounded, size: 18, color: scheme.secondary),
          const SizedBox(width: 10),
          Expanded(
            child: Text(
              'يظهر للجميع بعد المراجعة. شكرًا لمساهمتك في نشر الخير. 🤍',
              style: AppFonts.sans(
                fontSize: 13.5,
                height: 1.6,
                color: scheme.onSurface.withValues(alpha: 0.65),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
