import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../../core/controllers/taxonomy_controller.dart';
import '../../../../core/models/prayer_group.dart';
import '../../../../core/theme/app_typography.dart';
import '../../../search/controller/search_controller.dart';
import '../../../shell/controller/shell_controller.dart';

/// Horizontal row of taxonomy group chips. Tapping one opens the كل الأدعية
/// browse list pre-filtered by that group.
class GroupChips extends ConsumerWidget {
  const GroupChips({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final groups = ref.watch(taxonomyControllerProvider).groups;
    return SizedBox(
      height: 42,
      child: ListView.separated(
        scrollDirection: Axis.horizontal,
        itemCount: groups.length,
        separatorBuilder: (_, _) => const SizedBox(width: 9),
        itemBuilder: (context, i) => _GroupChip(group: groups[i]),
      ),
    );
  }
}

class _GroupChip extends ConsumerWidget {
  const _GroupChip({required this.group});
  final PrayerGroup group;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final scheme = Theme.of(context).colorScheme;
    return InkWell(
      borderRadius: BorderRadius.circular(999),
      onTap: () {
        ref.read(duaSearchControllerProvider).openWithGroup(group.slug);
        ref.read(shellControllerProvider).setIndex(1);
      },
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 9),
        decoration: BoxDecoration(
          color: scheme.primary.withValues(alpha: 0.04),
          borderRadius: BorderRadius.circular(999),
          border: Border.all(color: scheme.outline),
        ),
        child: Center(
          child: Text(
            group.name,
            style: AppFonts.sans(fontSize: 13.5, color: scheme.onSurface),
          ),
        ),
      ),
    );
  }
}
