import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/controllers/saved_controller.dart';
import '../../../core/controllers/theme_controller.dart';
import '../../../core/models/prayer.dart';
import '../../../core/services/widget_service.dart';
import '../../../core/state/view_state.dart';
import '../../../core/theme/app_tokens.dart';
import '../../../core/widgets/brand_wordmark.dart';
import '../../../core/widgets/dua_card.dart';
import '../../../core/widgets/section_header.dart';
import '../../search/controller/search_controller.dart';
import '../../settings/screens/settings_screen.dart';
import '../../shell/controller/shell_controller.dart';
import '../controller/home_controller.dart';
import 'widgets/daily_section.dart';
import 'widgets/group_chips.dart';
import 'widgets/home_greeting.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) => const _HomeView();
}

class _HomeView extends ConsumerStatefulWidget {
  const _HomeView();

  @override
  ConsumerState<_HomeView> createState() => _HomeViewState();
}

class _HomeViewState extends ConsumerState<_HomeView> {
  String _lastSyncSignature = '';

  @override
  void initState() {
    super.initState();
    WidgetService.ensureInitialized();
  }

  /// Keeps the iOS widgets fed with the freshest content. Runs after the frame
  /// and only when the underlying data actually changed.
  void _syncWidgets(HomeData? home, SavedController saved) {
    if (home == null) return;

    // The random widget reads from the user's saved du'as (truly offline);
    // when nothing is saved yet, fall back to today + the suggested du'as.
    final pool = <Prayer>[
      ...saved.items,
      if (saved.isEmpty) ...[
        if (home.daily != null) home.daily!,
        ...home.suggested,
      ],
    ];

    final signature = [
      home.daily?.id ?? '-',
      pool.map((p) => p.id).join(','),
    ].join('|');
    if (signature == _lastSyncSignature) return;
    _lastSyncSignature = signature;

    WidgetService.sync(daily: home.daily, pool: pool);
  }

  @override
  Widget build(BuildContext context) {
    final theme = ref.watch(themeControllerProvider);
    final controller = ref.watch(homeControllerProvider);
    final saved = ref.watch(savedControllerProvider);
    final state = controller.state;

    WidgetsBinding.instance.addPostFrameCallback(
      (_) => _syncWidgets(state.dataOrNull, saved),
    );

    return Scaffold(
      appBar: AppBar(
        titleSpacing: 20,
        title: const BrandWordmark(size: 30),
        actions: [
          IconButton(
            tooltip: 'المظهر',
            onPressed: () => theme.toggle(context),
            icon: Icon(
              theme.isDark(context)
                  ? Icons.light_mode_outlined
                  : Icons.dark_mode_outlined,
            ),
          ),
          IconButton(
            tooltip: 'الإعدادات',
            onPressed: () => Navigator.of(context).push(
              MaterialPageRoute(builder: (_) => const SettingsScreen()),
            ),
            icon: const Icon(Icons.tune_rounded),
          ),
          const SizedBox(width: 6),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: controller.refresh,
        child: ListView(
          padding: const EdgeInsets.fromLTRB(20, 8, 20, 28),
          children: [
            const HomeGreeting(),
            const SizedBox(height: AppSpacing.lg),
            DailySection(state: state, onRetry: controller.refresh),
            const SizedBox(height: AppSpacing.lg),
            if (state case ViewData(:final value)) ...[
              if (value.suggested.isNotEmpty) ...[
                SectionHeader(
                  title: 'أدعية مقترحة',
                  actionLabel: 'عرض الكل ←',
                  onAction: () {
                    ref.read(duaSearchControllerProvider).openAll();
                    ref.read(shellControllerProvider).setIndex(1);
                  },
                ),
                const SizedBox(height: AppSpacing.md),
                for (final prayer in value.suggested) ...[
                  DuaCard(prayer: prayer),
                  const SizedBox(height: AppSpacing.md),
                ],
                const SizedBox(height: AppSpacing.sm),
              ],
              const SectionHeader(title: 'تصفّح حسب الموضوع'),
              const SizedBox(height: AppSpacing.md),
              const GroupChips(),
            ],
          ],
        ),
      ),
    );
  }
}
