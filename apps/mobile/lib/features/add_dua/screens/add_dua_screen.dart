import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/controllers/taxonomy_controller.dart';
import '../../../core/models/prayer_category.dart';
import '../../../core/theme/app_tokens.dart';
import '../../../core/theme/app_typography.dart';
import '../../../core/widgets/brand_select.dart';
import '../controller/add_dua_controller.dart';
import 'widgets/field_label.dart';
import 'widgets/pending_note.dart';
import 'widgets/success_view.dart';
import 'widgets/type_segmented.dart';

class AddDuaScreen extends StatelessWidget {
  const AddDuaScreen({super.key});

  @override
  Widget build(BuildContext context) => const _AddView();
}

class _AddView extends ConsumerWidget {
  const _AddView();

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final controller = ref.watch(addDuaControllerProvider);
    return Scaffold(
      appBar: AppBar(
        titleSpacing: 20,
        title: Text(
          'إضافة دعاء',
          style: AppFonts.sans(fontSize: 22, fontWeight: FontWeight.w700),
        ),
      ),
      body: controller.success ? const SuccessView() : const _FormView(),
    );
  }
}

class _FormView extends ConsumerWidget {
  const _FormView();

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final controller = ref.watch(addDuaControllerProvider);
    final tax = ref.watch(taxonomyControllerProvider);
    final scheme = Theme.of(context).colorScheme;
    final List<PrayerCategory> categories = controller.groupSlug == null
        ? const []
        : tax.categoriesForGroup(controller.groupSlug!);

    return ListView(
      padding: const EdgeInsets.fromLTRB(20, 8, 20, 28),
      children: [
        Text(
          'شاركنا دعاءً تحبّه، ونضيفه بعد المراجعة ليدعو به غيرك.',
          style: AppFonts.sans(
            fontSize: 14.5,
            height: 1.7,
            color: scheme.onSurface.withValues(alpha: 0.65),
          ),
        ),
        const SizedBox(height: AppSpacing.lg),

        const FieldLabel('نص الدعاء'),
        const SizedBox(height: AppSpacing.sm),
        TextField(
          maxLines: 4,
          textAlign: TextAlign.center,
          style: AppFonts.display(fontSize: 20, height: 1.8, color: scheme.onSurface),
          decoration: const InputDecoration(hintText: 'اكتب الدعاء هنا…'),
          onChanged: controller.setText,
        ),
        const SizedBox(height: AppSpacing.lg),

        const FieldLabel('المجموعة'),
        const SizedBox(height: AppSpacing.sm),
        BrandSelectField<String>(
          value: controller.groupSlug,
          hint: 'اختر المجموعة',
          title: 'اختر المجموعة',
          options: [
            for (final g in tax.groups)
              BrandSelectOption(value: g.slug, label: g.name),
          ],
          onChanged: controller.selectGroup,
        ),
        const SizedBox(height: AppSpacing.lg),

        const FieldLabel('التصنيف'),
        const SizedBox(height: AppSpacing.sm),
        BrandSelectField<String>(
          value: controller.categorySlug,
          enabled: controller.groupSlug != null,
          hint: controller.groupSlug == null ? 'اختر المجموعة أولاً' : 'اختر التصنيف',
          title: 'اختر التصنيف',
          options: [
            for (final c in categories)
              BrandSelectOption(value: c.slug, label: c.name),
          ],
          onChanged: controller.selectCategory,
        ),
        const SizedBox(height: AppSpacing.lg),

        const FieldLabel('النوع'),
        const SizedBox(height: AppSpacing.sm),
        TypeSegmented(
          types: tax.types,
          selectedId: controller.typeSlug,
          onSelect: controller.selectType,
        ),
        const SizedBox(height: AppSpacing.lg),

        const PendingNote(),
        const SizedBox(height: AppSpacing.lg),

        FilledButton.icon(
          onPressed: controller.canSubmit && !controller.submitting
              ? () => _submit(context, controller)
              : null,
          icon: controller.submitting
              ? const SizedBox(
                  width: 18,
                  height: 18,
                  child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white),
                )
              : const Icon(Icons.send_rounded, size: 18),
          label: const Text('أرسِل الدعاء'),
        ),
      ],
    );
  }

  Future<void> _submit(BuildContext context, AddDuaController controller) async {
    await controller.submit();
    if (!context.mounted) return;
    final failure = controller.error;
    if (failure != null) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(failure.messageAr)),
      );
    }
  }
}
