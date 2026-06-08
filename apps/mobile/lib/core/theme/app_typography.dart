import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

/// Brand typefaces: Rakkas (display), Tajawal (body/UI), Geist Mono (numbers).
class AppFonts {
  AppFonts._();

  /// Rakkas — headings, the wordmark, and du'a text.
  static TextStyle display({
    double? fontSize,
    Color? color,
    double? height,
    FontWeight? fontWeight,
  }) =>
      GoogleFonts.getFont(
        'Rakkas',
        fontSize: fontSize,
        color: color,
        height: height,
        fontWeight: fontWeight,
      );

  /// Tajawal — UI and body text.
  static TextStyle sans({
    double? fontSize,
    Color? color,
    double? height,
    FontWeight? fontWeight,
    double? letterSpacing,
  }) =>
      GoogleFonts.getFont(
        'Tajawal',
        fontSize: fontSize,
        color: color,
        height: height,
        fontWeight: fontWeight,
        letterSpacing: letterSpacing,
      );

  /// Geist Mono — numbers, eyebrow labels, tags.
  static TextStyle mono({
    double? fontSize,
    Color? color,
    FontWeight? fontWeight,
    double? letterSpacing,
  }) =>
      GoogleFonts.getFont(
        'Geist Mono',
        fontSize: fontSize,
        color: color,
        fontWeight: fontWeight,
        letterSpacing: letterSpacing,
      );

  /// A Tajawal-based [TextTheme] tinted for the given foreground color.
  static TextTheme textTheme(TextTheme base, Color onColor) {
    return GoogleFonts.getTextTheme('Tajawal', base).apply(
      bodyColor: onColor,
      displayColor: onColor,
    );
  }
}
