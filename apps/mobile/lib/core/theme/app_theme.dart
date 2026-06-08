import 'package:flutter/material.dart';

import 'app_colors.dart';
import 'app_tokens.dart';
import 'app_typography.dart';

/// Builds the light and dark [ThemeData] from the Ad3oni brand tokens.
class AppTheme {
  AppTheme._();

  static ThemeData get light => _build(Brightness.light);
  static ThemeData get dark => _build(Brightness.dark);

  static ThemeData _build(Brightness brightness) {
    final isDark = brightness == Brightness.dark;

    final scheme = ColorScheme.fromSeed(
      seedColor: AppColors.royal,
      brightness: brightness,
    ).copyWith(
      primary: isDark ? AppColors.darkPrimary : AppColors.royal,
      onPrimary: isDark ? AppColors.night : Colors.white,
      secondary: AppColors.violet,
      onSecondary: Colors.white,
      surface: isDark ? AppColors.darkBg : AppColors.lightBg,
      onSurface: isDark ? AppColors.darkFg : AppColors.ink,
      surfaceContainerHighest:
          isDark ? AppColors.darkMuted : AppColors.lightMuted,
      outline: isDark ? AppColors.darkBorder : AppColors.lightBorder,
      outlineVariant: isDark ? AppColors.darkBorder : AppColors.lightBorder,
      error: isDark ? AppColors.darkDestructive : AppColors.destructive,
    );

    final base = ThemeData(brightness: brightness, useMaterial3: true);
    final textTheme = AppFonts.textTheme(base.textTheme, scheme.onSurface);

    final cardColor = isDark ? AppColors.darkCard : AppColors.lightCard;

    return base.copyWith(
      colorScheme: scheme,
      scaffoldBackgroundColor: scheme.surface,
      textTheme: textTheme,
      canvasColor: scheme.surface,
      dividerColor: scheme.outline,
      splashFactory: InkSparkle.splashFactory,
      appBarTheme: AppBarTheme(
        backgroundColor: scheme.surface,
        surfaceTintColor: Colors.transparent,
        elevation: 0,
        scrolledUnderElevation: 0,
        centerTitle: false,
      ),
      cardTheme: CardThemeData(
        color: cardColor,
        elevation: 0,
        margin: EdgeInsets.zero,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(AppRadii.card),
          side: BorderSide(color: scheme.outline),
        ),
      ),
      chipTheme: ChipThemeData(
        backgroundColor: isDark ? AppColors.darkSecondary : AppColors.lightSecondary,
        side: BorderSide.none,
        labelStyle: AppFonts.sans(
          fontSize: 12,
          fontWeight: FontWeight.w500,
          color: isDark ? AppColors.darkFg : AppColors.royal,
        ),
        shape: const StadiumBorder(),
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: scheme.surface,
        contentPadding:
            const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
        hintStyle: AppFonts.sans(
          color: isDark ? AppColors.darkMutedFg : AppColors.lightMutedFg,
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppRadii.md + 2),
          borderSide: BorderSide(color: scheme.outline),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppRadii.md + 2),
          borderSide: const BorderSide(color: AppColors.violet, width: 1.5),
        ),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppRadii.md + 2),
          borderSide: BorderSide(color: scheme.outline),
        ),
      ),
      filledButtonTheme: FilledButtonThemeData(
        style: FilledButton.styleFrom(
          backgroundColor: scheme.primary,
          foregroundColor: scheme.onPrimary,
          minimumSize: const Size.fromHeight(52),
          textStyle: AppFonts.sans(fontSize: 16, fontWeight: FontWeight.w700),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(AppRadii.md + 4),
          ),
        ),
      ),
      navigationBarTheme: NavigationBarThemeData(
        backgroundColor: scheme.surface,
        indicatorColor: (isDark ? AppColors.lilac : AppColors.royal)
            .withValues(alpha: isDark ? 0.18 : 0.10),
        elevation: 0,
        height: 70,
        labelTextStyle: WidgetStatePropertyAll(
          AppFonts.sans(fontSize: 11, fontWeight: FontWeight.w600),
        ),
      ),
    );
  }
}
