import 'package:flutter/animation.dart';

/// Corner radii from the brand scale.
class AppRadii {
  AppRadii._();
  static const double xs = 4;
  static const double sm = 8;
  static const double md = 12;
  static const double lg = 20;
  static const double xl = 28;
  static const double xxl = 32;
  static const double card = 20;
  static const double hero = 28;
  static const double heroLg = 32; // the daily hero / large surface radius
  static const double pill = 999;
}

/// Spacing scale: 4, 8, 12, 16, 24, 32, 48, 64.
class AppSpacing {
  AppSpacing._();
  static const double xs = 4;
  static const double sm = 8;
  static const double md = 12;
  static const double base = 16;
  static const double lg = 24;
  static const double xl = 32;
  static const double xxl = 48;
}

/// Motion durations + the brand easing curve.
class AppMotion {
  AppMotion._();
  static const Duration fast = Duration(milliseconds: 150);
  static const Duration base = Duration(milliseconds: 280);
  static const Duration slow = Duration(milliseconds: 480);
  static const Curve ease = Cubic(0.19, 1, 0.22, 1);
}
