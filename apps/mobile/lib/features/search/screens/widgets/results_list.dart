import 'package:flutter/material.dart';

import '../../../../core/state/view_state.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_tokens.dart';
import '../../../../core/theme/app_typography.dart';
import '../../../../core/utils/arabic_numbers.dart';
import '../../../../core/widgets/dua_card.dart';
import '../../../../core/widgets/empty_state.dart';
import '../../../../core/widgets/error_view.dart';
import '../../controller/search_controller.dart';

/// The كل الأدعية results area: loading / error / empty / paginated list with a
/// count header and infinite-scroll footer. Driven by the controller's state.
class ResultsList extends StatefulWidget {
  const ResultsList({super.key, required this.search});
  final DuaSearchController search;

  @override
  State<ResultsList> createState() => _ResultsListState();
}

class _ResultsListState extends State<ResultsList> {
  final _scroll = ScrollController();

  @override
  void initState() {
    super.initState();
    _scroll.addListener(_onScroll);
  }

  @override
  void dispose() {
    _scroll.removeListener(_onScroll);
    _scroll.dispose();
    super.dispose();
  }

  /// Pre-fetch the next page once we're within ~600px of the bottom.
  void _onScroll() {
    if (!_scroll.hasClients) return;
    final remaining = _scroll.position.maxScrollExtent - _scroll.position.pixels;
    if (remaining < 600) widget.search.loadMore();
  }

  @override
  Widget build(BuildContext context) {
    final search = widget.search;
    return switch (search.state) {
      ViewLoading() =>
        const Center(child: CircularProgressIndicator(color: AppColors.violet)),
      ViewError(:final failure) =>
        ErrorView(failure: failure, onRetry: search.run),
      ViewData(:final value) =>
        value.isEmpty ? _empty(search) : _list(context, search),
    };
  }

  Widget _empty(DuaSearchController search) => EmptyState(
        icon: Icons.menu_book_rounded,
        title: search.hasActiveFilters ? 'لا نتائج' : 'لا أدعية بعد',
        message: search.hasActiveFilters
            ? 'جرّب كلمة أخرى أو غيّر التصنيف.'
            : 'ستظهر الأدعية هنا بمجرد إضافتها.',
      );

  Widget _list(BuildContext context, DuaSearchController search) {
    final results = search.results;
    final count = toArabicDigits(search.totalItems.toString());
    final scheme = Theme.of(context).colorScheme;
    final isDark = scheme.brightness == Brightness.dark;
    final accent = isDark ? AppColors.lilac : AppColors.violet;
    final mutedStyle = AppFonts.mono(
      fontSize: 12,
      color: scheme.onSurface.withValues(alpha: 0.5),
    );

    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Padding(
          padding: const EdgeInsets.fromLTRB(20, 0, 20, 12),
          child: Row(
            children: [
              Text(
                search.hasActiveFilters ? 'النتائج' : 'كل الأدعية',
                style: AppFonts.sans(
                  fontSize: 14,
                  fontWeight: FontWeight.w700,
                  color: scheme.onSurface.withValues(alpha: 0.85),
                ),
              ),
              const Spacer(),
              if (search.refreshing) ...[
                SizedBox(
                  width: 13,
                  height: 13,
                  child: CircularProgressIndicator(strokeWidth: 2, color: accent),
                ),
                const SizedBox(width: 8),
                Text('جاري التحميل…', style: mutedStyle),
              ] else
                _CountBadge(count: count, accent: accent),
            ],
          ),
        ),
        Expanded(
          child: Opacity(
            opacity: search.refreshing ? 0.45 : 1,
            child: ListView.separated(
              controller: _scroll,
              padding: const EdgeInsets.fromLTRB(20, 0, 20, 28),
              itemCount: results.length + 1, // +1 load-more footer
              separatorBuilder: (_, _) => const SizedBox(height: AppSpacing.md),
              itemBuilder: (context, i) {
                if (i < results.length) return DuaCard(prayer: results[i]);
                return _LoadMoreFooter(search: search, style: mutedStyle);
              },
            ),
          ),
        ),
      ],
    );
  }
}

/// A small pill showing the total du'a count (e.g. «٨٢ دعاء»).
class _CountBadge extends StatelessWidget {
  const _CountBadge({required this.count, required this.accent});
  final String count;
  final Color accent;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 11, vertical: 4),
      decoration: BoxDecoration(
        color: accent.withValues(alpha: 0.10),
        borderRadius: BorderRadius.circular(AppRadii.pill),
        border: Border.all(color: accent.withValues(alpha: 0.20)),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Text(
            count,
            style: AppFonts.mono(fontSize: 12.5, fontWeight: FontWeight.w700, color: accent),
          ),
          const SizedBox(width: 5),
          Text(
            'دعاء',
            style: AppFonts.sans(
              fontSize: 11.5,
              color: accent.withValues(alpha: 0.85),
            ),
          ),
        ],
      ),
    );
  }
}

/// Trailing row: a spinner while the next page loads, or an end-of-list note.
class _LoadMoreFooter extends StatelessWidget {
  const _LoadMoreFooter({required this.search, required this.style});
  final DuaSearchController search;
  final TextStyle style;

  @override
  Widget build(BuildContext context) {
    if (search.loadingMore) {
      return const Padding(
        padding: EdgeInsets.symmetric(vertical: 18),
        child: Center(
          child: SizedBox(
            width: 22,
            height: 22,
            child: CircularProgressIndicator(strokeWidth: 2.2, color: AppColors.violet),
          ),
        ),
      );
    }
    if (!search.hasMore && search.results.length > 6) {
      return Padding(
        padding: const EdgeInsets.only(top: 6, bottom: 4),
        child: Center(child: Text('— تم عرض كل الأدعية —', style: style)),
      );
    }
    return const SizedBox(height: 4);
  }
}
