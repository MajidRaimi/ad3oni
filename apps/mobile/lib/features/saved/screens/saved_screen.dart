import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/controllers/saved_controller.dart';
import '../../../core/theme/app_tokens.dart';
import '../../../core/theme/app_typography.dart';
import '../../../core/widgets/dua_card.dart';
import '../../../core/widgets/empty_state.dart';
import 'widgets/offline_note.dart';

/// المحفوظات — the user's locally-saved du'as (offline). Its own bottom-nav
/// destination; browsing all du'as lives in the كل الأدعية (search) tab.
class SavedScreen extends ConsumerWidget {
  const SavedScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final saved = ref.watch(savedControllerProvider);
    return Scaffold(
      appBar: AppBar(
        titleSpacing: 20,
        title: Text(
          'المحفوظات',
          style: AppFonts.sans(fontSize: 22, fontWeight: FontWeight.w700),
        ),
      ),
      body: saved.isEmpty
          ? const EmptyState(
              icon: Icons.bookmark_border_rounded,
              title: 'لا أدعية محفوظة بعد',
              message:
                  'احفظ الأدعية التي تحبّها لتعود إليها في أي وقت، حتى دون اتصال.',
            )
          : ListView(
              padding: const EdgeInsets.fromLTRB(20, 16, 20, 28),
              children: [
                const OfflineNote(),
                const SizedBox(height: AppSpacing.base),
                for (final prayer in saved.items) ...[
                  DuaCard(prayer: prayer),
                  const SizedBox(height: AppSpacing.md),
                ],
              ],
            ),
    );
  }
}
