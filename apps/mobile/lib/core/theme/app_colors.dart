import 'package:flutter/material.dart';

/// Ad3oni brand colors, ported 1:1 from the brand design system.
class AppColors {
  AppColors._();

  // ---- Core brand ----
  static const royal = Color(0xFF2B0D69);
  static const royalDeep = Color(0xFF1C0847);
  static const violet = Color(0xFF6D49D6);
  static const lilac = Color(0xFFA98EE6);
  static const lilacBright = Color(0xFFB9A2EC); // lighter lilac, gradient tops
  static const night = Color(0xFF0C0626);
  static const paper = Color(0xFFFFFFFF);
  static const paperEnd = Color(0xFFF1ECFB); // paper gradient bottom (light hero)
  static const ink = Color(0xFF1A1330);
  static const neutral = Color(0xFF6B6486);

  // Night radial-gradient stops (the signature dark hero surface).
  static const nightGrad1 = Color(0xFF2C1370);
  static const nightGrad2 = Color(0xFF190B40);
  static const nightGrad3 = Color(0xFF0B0524);

  // ---- Light semantic ----
  static const lightBg = paper;
  static const lightCard = paper;
  static const lightMuted = Color(0xFFF4F1FC);
  static const lightMutedFg = neutral;
  static const lightSecondary = Color(0xFFECE6FA);
  static const lightSecondaryFg = royal;
  static const lightBorder = Color(0xFFE7E2F2);
  static const destructive = Color(0xFFD23B4E);

  // ---- Dark semantic ----
  static const darkBg = night;
  static const darkFg = Color(0xFFF3F0FB);
  static const darkCard = Color(0xFF160C34);
  static const darkMuted = Color(0xFF161033);
  static const darkMutedFg = Color(0xFFA79FC6);
  static const darkSecondary = Color(0xFF221546);
  static const darkBorder = Color(0x1FFFFFFF); // white @ 12%
  static const darkPrimary = lilac;
  static const darkDestructive = Color(0xFFFF6470);
}
