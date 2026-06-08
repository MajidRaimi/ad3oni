import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../../core/controllers/theme_controller.dart';
import 'option_card.dart';

/// Appearance picker: automatic / light / dark.
class ThemeCard extends ConsumerWidget {
  const ThemeCard({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final theme = ref.watch(themeControllerProvider);
    return OptionCard(
      children: [
        OptionRow(
          label: 'تلقائي (حسب النظام)',
          selected: theme.mode == ThemeMode.system,
          onTap: () => theme.setMode(ThemeMode.system),
        ),
        OptionRow(
          label: 'فاتح',
          selected: theme.mode == ThemeMode.light,
          onTap: () => theme.setMode(ThemeMode.light),
        ),
        OptionRow(
          label: 'داكن',
          selected: theme.mode == ThemeMode.dark,
          onTap: () => theme.setMode(ThemeMode.dark),
          isLast: true,
        ),
      ],
    );
  }
}
