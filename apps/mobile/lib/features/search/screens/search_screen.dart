import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/controllers/taxonomy_controller.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_tokens.dart';
import '../../../core/theme/app_typography.dart';
import '../../../core/widgets/brand_search_field.dart';
import '../controller/search_controller.dart';
import 'widgets/filter_selector.dart';
import 'widgets/results_list.dart';

/// «كل الأدعية» — the dedicated search / browse destination: a premium control
/// panel (search + two filter pills) above a paginated list of all confirmed
/// du'as.
class SearchScreen extends ConsumerStatefulWidget {
  const SearchScreen({super.key});

  @override
  ConsumerState<SearchScreen> createState() => _SearchScreenState();
}

class _SearchScreenState extends ConsumerState<SearchScreen> {
  final _text = TextEditingController();

  @override
  void initState() {
    super.initState();
    _text.text = ref.read(duaSearchControllerProvider).query;
  }

  @override
  void dispose() {
    _text.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final search = ref.watch(duaSearchControllerProvider);
    final tax = ref.watch(taxonomyControllerProvider);
    final scheme = Theme.of(context).colorScheme;
    final isDark = scheme.brightness == Brightness.dark;
    final accent = isDark ? AppColors.lilac : AppColors.violet;

    // Keep the field in sync if the query changed externally (e.g. cleared).
    if (_text.text != search.query) {
      _text.value = TextEditingValue(
        text: search.query,
        selection: TextSelection.collapsed(offset: search.query.length),
      );
    }

    return Scaffold(
      appBar: AppBar(
        titleSpacing: 20,
        title: Text(
          'كل الأدعية',
          style: AppFonts.sans(fontSize: 22, fontWeight: FontWeight.w700),
        ),
      ),
      body: Column(
        children: [
          // Frosted control panel: faint top glow + a hairline separating it
          // from the scrolling list.
          Container(
            padding: const EdgeInsets.fromLTRB(20, 8, 20, 18),
            decoration: BoxDecoration(
              gradient: LinearGradient(
                begin: Alignment.topCenter,
                end: Alignment.bottomCenter,
                colors: [accent.withValues(alpha: isDark ? 0.06 : 0.035), Colors.transparent],
              ),
              border: Border(bottom: BorderSide(color: scheme.outline)),
            ),
            child: Column(
              children: [
                BrandSearchField(
                  controller: _text,
                  hint: 'ابحث في كل الأدعية…',
                  onChanged: search.setQuery,
                ),
                const SizedBox(height: AppSpacing.md),
                Row(
                  children: [
                    Expanded(
                      child: FilterSelector(
                        label: 'النوع',
                        options: [for (final t in tax.types) (t.slug, t.name)],
                        selectedId: search.typeSlug,
                        onChanged: search.selectType,
                      ),
                    ),
                    const SizedBox(width: 10),
                    Expanded(
                      child: FilterSelector(
                        label: 'المجموعة',
                        options: [for (final g in tax.groups) (g.slug, g.name)],
                        selectedId: search.groupSlug,
                        onChanged: search.selectGroup,
                      ),
                    ),
                  ],
                ),
                if (search.hasActiveFilters) ...[
                  const SizedBox(height: 8),
                  Align(
                    alignment: AlignmentDirectional.centerStart,
                    child: TextButton.icon(
                      onPressed: search.clear,
                      style: TextButton.styleFrom(
                        padding: const EdgeInsets.symmetric(horizontal: 8),
                        minimumSize: const Size(0, 32),
                        foregroundColor: accent,
                      ),
                      icon: const Icon(Icons.close_rounded, size: 15),
                      label: Text(
                        'مسح التصفية',
                        style: AppFonts.sans(fontSize: 12.5, fontWeight: FontWeight.w600),
                      ),
                    ),
                  ),
                ],
              ],
            ),
          ),
          const SizedBox(height: AppSpacing.base),
          Expanded(child: ResultsList(search: search)),
        ],
      ),
    );
  }
}
