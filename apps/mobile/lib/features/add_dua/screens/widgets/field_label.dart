import 'package:flutter/material.dart';

import '../../../../core/theme/app_typography.dart';

/// A bold form-field label used on the Add screen.
class FieldLabel extends StatelessWidget {
  const FieldLabel(this.text, {super.key});
  final String text;

  @override
  Widget build(BuildContext context) => Text(
        text,
        style: AppFonts.sans(
          fontSize: 15,
          fontWeight: FontWeight.w600,
          color: Theme.of(context).colorScheme.onSurface,
        ),
      );
}
