// Smoke test for the Ad3oni app shell.
import 'package:ad3oni/app.dart';
import 'package:ad3oni/core/providers.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  testWidgets('App boots and renders the RTL shell', (tester) async {
    SharedPreferences.setMockInitialValues({});
    final prefs = await SharedPreferences.getInstance();

    await tester.pumpWidget(
      ProviderScope(
        overrides: [sharedPreferencesProvider.overrideWithValue(prefs)],
        child: const Ad3oniApp(),
      ),
    );
    await tester.pump();

    // The bottom navigation labels should be present.
    expect(find.text('الرئيسية'), findsOneWidget);
    expect(find.byType(MaterialApp), findsOneWidget);
  });
}
