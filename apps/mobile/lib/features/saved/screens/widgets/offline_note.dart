import 'package:flutter/material.dart';

import '../../../../core/theme/app_typography.dart';

/// Small "saved offline" caption shown above the saved du'as list.
class OfflineNote extends StatelessWidget {
  const OfflineNote({super.key});

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        Icon(Icons.wifi_off_rounded, size: 14, color: scheme.onSurface.withValues(alpha: 0.45)),
        const SizedBox(width: 6),
        Text(
          'محفوظة دون اتصال',
          style: AppFonts.mono(fontSize: 11, color: scheme.onSurface.withValues(alpha: 0.45)),
        ),
      ],
    );
  }
}
