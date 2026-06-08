// Verifies the random-widget interval setting renders and updates the choice.
import 'package:ad3oni/core/providers.dart';
import 'package:ad3oni/features/settings/controller/settings_controller.dart';
import 'package:ad3oni/features/settings/screens/settings_screen.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  testWidgets('random-interval setting renders and updates the choice',
      (tester) async {
    // The interval section is iOS-only; force the platform so it renders.
    // Must be reset before the test body returns (framework invariant check).
    debugDefaultTargetPlatformOverride = TargetPlatform.iOS;

    SharedPreferences.setMockInitialValues({});
    final prefs = await SharedPreferences.getInstance();

    await tester.pumpWidget(
      ProviderScope(
        overrides: [sharedPreferencesProvider.overrideWithValue(prefs)],
        child: const MaterialApp(home: SettingsScreen()),
      ),
    );
    await tester.pumpAndSettle();

    // Section header + a few interval options are on screen.
    expect(find.text('الدعاء العشوائي'), findsOneWidget);
    expect(find.text('كل ساعتين'), findsOneWidget);
    expect(find.text('كل ساعة'), findsOneWidget);
    expect(find.text('مرة في اليوم'), findsOneWidget);

    // Read the real controller the UI is driving, via the Riverpod container.
    final container = ProviderScope.containerOf(
      tester.element(find.byType(SettingsScreen)),
    );
    final settings = container.read(settingsControllerProvider);

    // Default matches the previous widget behaviour (every 2 hours).
    expect(settings.randomIntervalMinutes, 120);

    // Picking "every hour" updates the controller (and persists to prefs).
    await tester.tap(find.text('كل ساعة'));
    await tester.pumpAndSettle();
    expect(settings.randomIntervalMinutes, 60);
    expect(prefs.getInt('ad3oni.random_interval_minutes'), 60);

    debugDefaultTargetPlatformOverride = null;
  });
}
