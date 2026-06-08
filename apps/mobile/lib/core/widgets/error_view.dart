import 'package:flutter/material.dart';

import '../error/failure.dart';
import '../theme/app_tokens.dart';
import '../theme/app_typography.dart';

/// Renders a typed [Failure] with its Arabic message and a retry button.
///
/// The single shared way to show an error (CLAUDE.md §7) — no silent empty
/// error states.
class ErrorView extends StatelessWidget {
  const ErrorView({super.key, required this.failure, this.onRetry});

  final Failure failure;
  final VoidCallback? onRetry;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(AppSpacing.lg),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Container(
              width: 74,
              height: 74,
              decoration: BoxDecoration(
                color: scheme.error.withValues(alpha: 0.08),
                borderRadius: BorderRadius.circular(AppRadii.lg),
                border: Border.all(color: scheme.outline),
              ),
              child: Icon(Icons.cloud_off_rounded, size: 32, color: scheme.error),
            ),
            const SizedBox(height: AppSpacing.base),
            Text(
              failure.messageAr,
              textAlign: TextAlign.center,
              style: AppFonts.sans(
                fontSize: 15,
                height: 1.7,
                color: scheme.onSurface.withValues(alpha: 0.7),
              ),
            ),
            if (onRetry != null) ...[
              const SizedBox(height: AppSpacing.base),
              TextButton.icon(
                onPressed: onRetry,
                icon: const Icon(Icons.refresh_rounded, size: 18),
                label: const Text('إعادة المحاولة'),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
