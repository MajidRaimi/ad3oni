import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'core/theme/app_theme.dart';
import 'core/controllers/theme_controller.dart';
import 'features/shell/screens/root_shell.dart';

/// Root of the Ad3oni mobile app — Arabic-first, RTL, brand-themed.
///
/// State management is Riverpod: the app is wrapped in a `ProviderScope` (see
/// `main.dart`) and controllers are read via `ref.watch` / `ref.read`.
class Ad3oniApp extends ConsumerWidget {
  const Ad3oniApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final mode = ref.watch(themeControllerProvider).mode;
    return MaterialApp(
      title: 'ادعوني',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.light,
      darkTheme: AppTheme.dark,
      themeMode: mode,
      locale: const Locale('ar'),
      supportedLocales: const [Locale('ar'), Locale('en')],
      localizationsDelegates: const [
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
      home: const RootShell(),
    );
  }
}
