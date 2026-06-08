import 'package:flutter/material.dart';

import '../theme/app_typography.dart';

/// The Ad3oni wordmark «ادْعُوني» set in Rakkas.
class BrandWordmark extends StatelessWidget {
  const BrandWordmark({
    super.key,
    this.size = 28,
    this.color,
    this.withHarakat = true,
  });

  final double size;
  final Color? color;
  final bool withHarakat;

  @override
  Widget build(BuildContext context) {
    return Text(
      withHarakat ? 'ادْعُوني' : 'ادعوني',
      textDirection: TextDirection.rtl,
      style: AppFonts.display(
        fontSize: size,
        height: 1,
        color: color ?? Theme.of(context).colorScheme.primary,
      ),
    );
  }
}
