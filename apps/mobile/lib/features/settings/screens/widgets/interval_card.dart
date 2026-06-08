import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../controller/settings_controller.dart';
import 'option_card.dart';

/// Picker for how often the random home-screen widget rotates.
class IntervalCard extends ConsumerWidget {
  const IntervalCard({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final settings = ref.watch(settingsControllerProvider);
    final options = SettingsController.intervalOptions;
    return OptionCard(
      children: [
        for (var i = 0; i < options.length; i++)
          OptionRow(
            label: options[i].label,
            selected: settings.randomIntervalMinutes == options[i].minutes,
            onTap: () => settings.setRandomInterval(options[i].minutes),
            isLast: i == options.length - 1,
          ),
      ],
    );
  }
}
