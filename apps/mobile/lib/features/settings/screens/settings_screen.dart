import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';

import '../../../core/theme/app_tokens.dart';
import '../../../core/theme/app_typography.dart';
import '../../../core/widgets/section_header.dart';
import 'widgets/interval_card.dart';
import 'widgets/theme_card.dart';

/// App settings: appearance + the random widget's rotation cadence.
class SettingsScreen extends StatelessWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final showWidgetSection =
        !kIsWeb && defaultTargetPlatform == TargetPlatform.iOS;
    final scheme = Theme.of(context).colorScheme;

    return Scaffold(
      appBar: AppBar(
        titleSpacing: 20,
        title: Text(
          'الإعدادات',
          style: AppFonts.sans(fontSize: 22, fontWeight: FontWeight.w700),
        ),
      ),
      body: ListView(
        padding: const EdgeInsets.fromLTRB(20, 16, 20, 32),
        children: [
          const SectionHeader(title: 'المظهر'),
          const SizedBox(height: AppSpacing.md),
          const ThemeCard(),
          if (showWidgetSection) ...[
            const SizedBox(height: AppSpacing.lg),
            const SectionHeader(title: 'الدعاء العشوائي'),
            const SizedBox(height: AppSpacing.sm),
            Text(
              'كم مرة يتغيّر الدعاء في ودجت الشاشة الرئيسية. قد يؤخّر النظام '
              'التحديث قليلًا للحفاظ على البطارية.',
              style: AppFonts.sans(
                fontSize: 13,
                height: 1.6,
                color: scheme.onSurface.withValues(alpha: 0.6),
              ),
            ),
            const SizedBox(height: AppSpacing.md),
            const IntervalCard(),
          ],
        ],
      ),
    );
  }
}
